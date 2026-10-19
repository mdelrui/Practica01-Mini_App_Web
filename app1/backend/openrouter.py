import requests
from .config import API_KEY, URL, MODELO


class OpenRouterError(Exception):
    """Error controlado al solicitar un resumen a OpenRouter."""


def preguntar_ia(historial):
    if not API_KEY:
        raise OpenRouterError(
            "Falta configurar la variable OPENROUTER_API_KEY."
        )

    cabeceras = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    datos = {
        "model": MODELO,
        "messages": historial,
    }

    try:
        respuesta = requests.post(
            URL,
            headers=cabeceras,
            json=datos,
            timeout=(5, 30),
        )
        respuesta.raise_for_status()
        resultado = respuesta.json()

        contenido = resultado["choices"][0]["message"]["content"]

        if not isinstance(contenido, str) or not contenido.strip():
            raise OpenRouterError(
                "OpenRouter ha devuelto un resumen vacío o inválido."
            )

        return contenido.strip()

    except requests.RequestException as exc:
        raise OpenRouterError(
            "No se ha podido conectar correctamente con OpenRouter."
        ) from exc

    except (ValueError, KeyError, IndexError, TypeError) as exc:
        raise OpenRouterError(
            "OpenRouter ha devuelto una respuesta con un formato inesperado."
        ) from exc
