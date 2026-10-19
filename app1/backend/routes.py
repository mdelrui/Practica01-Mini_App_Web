from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from .openrouter import OpenRouterError, resumir_con_ia

router = APIRouter()


class TextoEntrada(BaseModel):
    # Limitamos el tamaño para no enviar textos demasiado largos.
    texto: str = Field(min_length=1, max_length=5000)


@router.post("/api/resumir")
def resumir(datos: TextoEntrada):
    texto = datos.texto.strip()

    if not texto:
        raise HTTPException(status_code=400, detail="Escribe un texto para resumir.")

    try:
        resumen = resumir_con_ia(texto)
    except OpenRouterError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error

    return {"resumen": resumen}
