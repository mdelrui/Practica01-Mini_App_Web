import requests

from .config import API_KEY, API_URL, MODELO


def obtener_resumen(texto: str) -> str:
    # Verificamos si existe la clave de la API configurada
    if not API_KEY:
        raise RuntimeError("Falta configurar OPENROUTER_API_KEY.")

    # Estructura del mensaje para enviar a la IA de OpenRouter
    cuerpo_peticion = {
        "model": MODELO,
        "messages": [
            {
                "role": "user",
                "content": (
                    "Resume el siguiente texto de forma clara y breve. "
                    "Usa solo la información del texto y devuelve únicamente el resumen:\n\n"
                    + texto
                ),
            }
        ],
    }

    try:
        # Realizamos la petición HTTP POST a OpenRouter
        respuesta = requests.post(
            API_URL,
            headers = {"Authorization": f"Bearer {API_KEY}"},
            json=cuerpo_peticion,
            timeout=(5, 30),
        )
        respuesta.raise_for_status()
         # Extraemos el resumen de la respuesta recibida
        datos = respuesta.json()
        resumen = datos["choices"][0]["message"]["content"]
    except requests.Timeout as error:
        raise TimeoutError("El proveedor tardó demasiado en responder.") from error
    except (requests.RequestException, KeyError, IndexError, TypeError, ValueError) as error:
        raise RuntimeError("No se pudo obtener un resumen válido de OpenRouter.") from error

    if not isinstance(resumen, str) or not resumen.strip():
        raise RuntimeError("OpenRouter devolvió un resumen vacío.")

    return resumen.strip()
