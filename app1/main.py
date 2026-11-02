from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.routes import router

# Creamos la aplicación FastAPI y registramos las rutas de la API
app = FastAPI(title="Resumidor de textos")
app.include_router(router)

# En local, servimos los archivos del frontend si ya está compilado en la carpeta dist
carpeta_frontend = Path(__file__).parent / "frontend" / "dist"
if carpeta_frontend.exists():
    app.mount("/", StaticFiles(directory=carpeta_frontend, html=True), name="frontend")

# Punto de entrada para arrancar el servidor en local
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
