import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

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