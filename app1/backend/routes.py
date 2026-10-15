from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .openrouter import preguntar_ia


router = APIRouter()


class Texto(BaseModel):
    texto: str


@router.post("/api/resumir")
def resumir(datos: Texto):
    # Comprobamos que el usuario haya escrito algún texto.
    if not datos.texto.strip():
        raise HTTPException(status_code=400, detail="Escribe un texto")

    # Preparamos la pregunta para la inteligencia artificial.
    historial = [
        {
            "role": "user",
            "content": "Resume este texto de forma clara y breve:\n" + datos.texto,
        }
    ]
    respuesta = preguntar_ia(historial)

    # Avisamos si OpenRouter no devuelve ningún resumen.
    if respuesta is None:
        raise HTTPException(
            status_code=502,
            detail="No se pudo obtener el resumen",
        )

    return {"resumen": respuesta}
