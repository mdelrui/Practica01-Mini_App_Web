import os

from enum import Enum
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from models import UserInput

from auth import (
    InvalidSessionToken,
    SessionVerifierUnavailable,
    verify_session_token,
)
from services import IAError, ResumenResponse, resumir

ORIGENES = [
    origen.strip()
    for origen in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173"
    ).split(',')
    if origen.strip()
]

app = FastAPI(title="ResumidorIA API")


@app.get("/health", tags=["operaciones"])
def health_check():
    """Endpoint de salud para comprobar que el proceso FastAPI responde."""
    return {"status": "ok"}
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGENES,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def attach_cors_headers(response: JSONResponse, request: Request) -> JSONResponse:
    origin = request.headers.get("origin")
    if origin:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Vary"] = "Origin"
    elif ORIGENES:
        response.headers["Access-Control-Allow-Origin"] = ORIGENES[0]
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


AUTH_INVALID = {
    "error": {
        "codigo": "AUTH_INVALID",
        "mensaje": "Autenticación requerida o sesión no válida.",
    }
}
AUTH_UNAVAILABLE = {
    "error": {
        "codigo": "AUTH_UNAVAILABLE",
        "mensaje": "No se pudo verificar la sesión temporalmente. Inténtalo más tarde.",
    }
}


@app.middleware("http")
async def verificar_sesion(request: Request, call_next):
    if request.method == "POST" and request.url.path == "/resumir":
        authorization = request.headers.get("authorization", "")
        scheme, separator, token = authorization.partition(" ")
        if (
            scheme.lower() != "bearer"
            or not separator
            or not token
            or token != token.strip()
            or any(character.isspace() for character in token)
        ):
            return attach_cors_headers(
                JSONResponse(status_code=401, content=AUTH_INVALID),
                request,
            )

        try:
            await run_in_threadpool(verify_session_token, token)
        except InvalidSessionToken:
            return attach_cors_headers(
                JSONResponse(status_code=401, content=AUTH_INVALID),
                request,
            )
        except SessionVerifierUnavailable:
            return attach_cors_headers(
                JSONResponse(status_code=503, content=AUTH_UNAVAILABLE),
                request,
            )

    return await call_next(request)




@app.exception_handler(IAError)
def manejar_error_ia(request: Request, exc: IAError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"codigo": exc.codigo, "mensaje": exc.mensaje}},
    )


@app.post("/resumir", response_model=ResumenResponse, response_model_exclude_none=True)
def resumir_texto(user_input: UserInput):
    return resumir(user_input.text, user_input.main_ideas, user_input.glossary, user_input.summary_length)