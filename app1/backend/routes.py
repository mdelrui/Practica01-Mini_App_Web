from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from .openrouter import obtener_resumen

router = APIRouter()


class TextoEntrada(BaseModel):
    texto: str = Field(min_length=1, max_length=5000)


@router.post("/api/resumir")
def resumir_texto(entrada: TextoEntrada):
    # Limpiamos los espacios en blanco sobrantes al inicio y al final
    texto_limpio = entrada.texto.strip()

    # Comprobamos que el texto no esté vacío
    if not texto_limpio:
        raise HTTPException(status_code=400, detail="Escribe un texto para resumir.")
    try:
        resumen = obtener_resumen(texto_limpio)
    except TimeoutError as error:
        raise HTTPException(status_code=504, detail=str(error)) from error
    except RuntimeError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error

    return {"resumen": resumen}
