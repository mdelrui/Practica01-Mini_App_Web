from fastapi import APIRouter, HTTPException

from .models import Texto
from .openrouter import preguntar_ia


router = APIRouter()


@router.get("/")
def inicio():
    return {"mensaje": "La aplicación funciona"}


@router.post("/api/resumir")
def resumir(datos: Texto):
    if not datos.texto.strip():
        raise HTTPException(status_code=400, detail="Escribe un texto")

    historial = [
        {
            "role": "user",
            "content": "Resume este texto de forma clara y breve:\n" + datos.texto,
        }
    ]
    respuesta = preguntar_ia(historial)

    if respuesta is None:
        raise HTTPException(
            status_code=502,
            detail="No se pudo obtener el resumen",
        )

    return {"resumen": respuesta}
