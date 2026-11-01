import pytest
import requests

from .. import openrouter


class RespuestaFalsa:
    def raise_for_status(self):
        pass

    def json(self):
        return {"choices": [{"message": {"content": "Resumen válido"}}]}


def test_obtener_resumen_devuelve_el_contenido(monkeypatch):
    monkeypatch.setattr(openrouter, "API_KEY", "clave-de-prueba")
    monkeypatch.setattr(openrouter.requests, "post", lambda *args, **kwargs: RespuestaFalsa())

    resultado = openrouter.obtener_resumen("Texto original")

    assert resultado == "Resumen válido"


def test_obtener_resumen_envia_la_peticion_correcta(monkeypatch):
    monkeypatch.setattr(openrouter, "API_KEY", "clave-de-prueba")
    peticion = {}

    def post_falso(url, **kwargs):
        peticion["url"] = url
        peticion.update(kwargs)
        return RespuestaFalsa()

    monkeypatch.setattr(openrouter.requests, "post", post_falso)

    openrouter.obtener_resumen("Texto original")

    assert peticion["headers"]["Authorization"] == "Bearer clave-de-prueba"
    assert peticion["json"]["messages"][0]["content"].endswith("Texto original")
    assert peticion["timeout"] == (5, 30)


def test_obtener_resumen_falla_sin_clave(monkeypatch):
    monkeypatch.setattr(openrouter, "API_KEY", None)

    with pytest.raises(RuntimeError, match="Falta configurar"):
        openrouter.obtener_resumen("Texto")


def test_obtener_resumen_falla_si_la_respuesta_esta_vacia(monkeypatch):
    class RespuestaVacia(RespuestaFalsa):
        def json(self):
            return {"choices": [{"message": {"content": "  "}}]}

    monkeypatch.setattr(openrouter, "API_KEY", "clave-de-prueba")
    monkeypatch.setattr(openrouter.requests, "post", lambda *args, **kwargs: RespuestaVacia())

    with pytest.raises(RuntimeError, match="resumen vacío"):
        openrouter.obtener_resumen("Texto")


def test_obtener_resumen_falla_por_timeout(monkeypatch):
    monkeypatch.setattr(openrouter, "API_KEY", "clave-de-prueba")

    def simular_timeout(*args, **kwargs):
        raise requests.Timeout("Tardó demasiado")

    monkeypatch.setattr(openrouter.requests, "post", simular_timeout)

    with pytest.raises(TimeoutError, match="tardó demasiado"):
        openrouter.obtener_resumen("Texto")


def test_obtener_resumen_falla_por_error_de_red(monkeypatch):
    monkeypatch.setattr(openrouter, "API_KEY", "clave-de-prueba")

    def simular_error_red(*args, **kwargs):
        raise requests.ConnectionError("Fallo de conexión")

    monkeypatch.setattr(openrouter.requests, "post", simular_error_red)

    with pytest.raises(RuntimeError, match="No se pudo obtener"):
        openrouter.obtener_resumen("Texto")


def test_obtener_resumen_falla_si_falta_el_contenido(monkeypatch):
    class RespuestaIncorrecta(RespuestaFalsa):
        def json(self):
            return {"choices": []}

    monkeypatch.setattr(openrouter, "API_KEY", "clave-de-prueba")
    monkeypatch.setattr(openrouter.requests, "post", lambda *args, **kwargs: RespuestaIncorrecta())

    with pytest.raises(RuntimeError, match="No se pudo obtener"):
        openrouter.obtener_resumen("Texto")
