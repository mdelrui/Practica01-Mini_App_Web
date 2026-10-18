from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from .openrouter import OpenRouterError, preguntar_ia


router = APIRouter()


class Texto(BaseModel):
    texto: str = Field(max_length=5000)


@router.post("/api/resumir")
def resumir(datos: Texto):
    texto = datos.texto.strip()

    if not texto:
        raise HTTPException(
            status_code=400,
            detail="Escribe un texto para resumir.",
        )

    historial = [
        {
            "role": "user",
            "content": (
                "Resume el siguiente texto de forma clara y breve:\n\n"
                + texto
            ),
        }
    ]

    try:
        resumen = preguntar_ia(historial)
    except OpenRouterError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    return {"resumen": resumen}
