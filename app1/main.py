from fastapi import FastAPI
from backend.routes import router

app = FastAPI(title="Mini App Web API")

app.include_router(router)

@app.get("/")
def health_check():
    return {"status": "ok", "docs": "/docs"}
