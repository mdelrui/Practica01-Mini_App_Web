import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field
from starlette.concurrency import run_in_threadpool

from auth import (
    InvalidSessionToken,
    SessionVerifierUnavailable,
    verify_session_token,
)
from services import IAError, ResumenResponse, resumir

MAX_CHARS = 5000
ORIGENES = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGENES,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
            return JSONResponse(status_code=401, content=AUTH_INVALID)

        try:
            await run_in_threadpool(verify_session_token, token)
        except InvalidSessionToken:
            return JSONResponse(status_code=401, content=AUTH_INVALID)
        except SessionVerifierUnavailable:
            return JSONResponse(status_code=503, content=AUTH_UNAVAILABLE)

    return await call_next(request)


class UserInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    text: str = Field(min_length=1, max_length=MAX_CHARS)
    main_ideas: bool = False


@app.exception_handler(IAError)
def manejar_error_ia(request: Request, exc: IAError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"codigo": exc.codigo, "mensaje": exc.mensaje}},
    )


@app.post("/resumir", response_model=ResumenResponse)
def resumir_texto(user_input: UserInput):
    return resumir(user_input.text, user_input.main_ideas)