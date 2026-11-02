import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from .. import routes
from ..routes import TextoEntrada, resumir_texto


def test_peticion_valida(monkeypatch):
    monkeypatch.setattr(routes, "obtener_resumen", lambda texto: "Resumen simulado")

    entrada = TextoEntrada(texto="Texto de prueba válido")

    assert resumir_texto(entrada) == {"resumen": "Resumen simulado"}


def test_entrada_vacia_falla():
    with pytest.raises(ValidationError):
        TextoEntrada(texto="")


def test_entrada_solo_espacios_falla():
    entrada = TextoEntrada(texto="    ")

    with pytest.raises(HTTPException) as fallo:
        resumir_texto(entrada)

    assert fallo.value.status_code == 400
    assert "Escribe un texto" in fallo.value.detail


def test_limite_longitud_superado():
    with pytest.raises(ValidationError):
        TextoEntrada(texto="a" * 5001)


def test_limite_longitud_permitido():
    entrada = TextoEntrada(texto="a" * 5000)
    assert len(entrada.texto) == 5000


def test_el_texto_se_limpia_antes_de_enviarlo(monkeypatch):
    textos_recibidos = []
    monkeypatch.setattr(routes, "obtener_resumen", lambda texto: textos_recibidos.append(texto) or "Resumen")

    resumir_texto(TextoEntrada(texto="  Texto válido  "))

    assert textos_recibidos == ["Texto válido"]


def test_fallo_del_proveedor(monkeypatch):
    def simular_caida(texto):
        raise RuntimeError("No se pudo obtener un resumen válido de OpenRouter.")

    monkeypatch.setattr(routes, "obtener_resumen", simular_caida)

    with pytest.raises(HTTPException) as fallo:
        resumir_texto(TextoEntrada(texto="Texto válido"))

    assert fallo.value.status_code == 502
    assert "OpenRouter" in fallo.value.detail


def test_timeout_del_proveedor(monkeypatch):
    def simular_espera(texto):
        raise TimeoutError("El proveedor tardó demasiado en responder.")

    monkeypatch.setattr(routes, "obtener_resumen", simular_espera)

    with pytest.raises(HTTPException) as fallo:
        resumir_texto(TextoEntrada(texto="Texto válido"))

    assert fallo.value.status_code == 504
    assert "tardó demasiado" in fallo.value.detail
