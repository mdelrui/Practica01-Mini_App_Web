import requests

from .config import API_KEY, API_URL, MODEL


class OpenRouterError(Exception):
    """Error sencillo al pedir un resumen a OpenRouter."""


def resumir_con_ia(texto: str) -> str:
    # Comprobamos que la clave esté configurada.
    if not API_KEY:
        raise OpenRouterError("Falta configurar OPENROUTER_API_KEY.")

    datos = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": "Resume este texto de forma clara y breve:\n\n" + texto,
            }
        ],
    }
    cabeceras = {
        "Authorization": f"******",
        "Content-Type": "application/json",
    }

    try:
        respuesta = requests.post(
            API_URL, headers=cabeceras, json=datos, timeout=30
        )
        respuesta.raise_for_status()
        contenido = respuesta.json()["choices"][0]["message"]["content"]
    except requests.RequestException as error:
        raise OpenRouterError("No se pudo conectar con OpenRouter.") from error
    except (ValueError, KeyError, IndexError, TypeError) as error:
        raise OpenRouterError("La respuesta de OpenRouter no es válida.") from error

    if not isinstance(contenido, str) or not contenido.strip():
        raise OpenRouterError("OpenRouter devolvió un resumen vacío.")

    return contenido.strip()
