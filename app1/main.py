from fastapi import FastAPI

from backend.routes import router

# Esta es la aplicación principal del backend.
app = FastAPI(title="Resumidor de textos")
app.include_router(router)


@app.get("/")
def inicio():
    # Ruta sencilla para comprobar que la API funciona.
    return {"estado": "ok", "documentacion": "/docs"}
