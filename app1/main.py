from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from backend.routes import router


# Creamos la aplicación principal.
app = FastAPI()
app.include_router(router)

# Servimos la versión compilada del frontend.
frontend_dist = Path(__file__).parent / "frontend" / "dist"
app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")


if __name__ == "__main__":
    # Iniciamos el servidor local.
    uvicorn.run(app, host="127.0.0.1", port=8000)
