from fastapi import APIRouter, Body, HTTPException

from .openrouter import obtener_resumen

router = APIRouter()


@router.post("/api/resumir")
def resumir_texto(texto: str = Body(embed=True)):
    # Limpiamos los espacios en blanco sobrantes al inicio y al final
    texto_limpio = texto.strip()

    # Comprobamos que el texto no esté vacío
    if not texto_limpio:
        raise HTTPException(status_code=400, detail="Escribe un texto para resumir.")

    # Validamos que no supere el límite permitido de caracteres
    if len(texto_limpio) > 5000:
        raise HTTPException(
            status_code=400,
            detail="El texto es demasiado largo (máximo 5000 caracteres).",
        )

    try:
        # Llamamos a la función auxiliar para generar el resumen con la IA
        resumen = obtener_resumen(texto_limpio)
    except RuntimeError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error

    # Devolvemos el resultado en formato JSON
    return {"resumen": resumen}
