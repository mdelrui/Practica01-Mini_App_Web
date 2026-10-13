from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Crea la aplicación FastAPI
app = FastAPI()

# Obtiene la clave API de OpenRouter desde las variables de entorno
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Define el modelo de datos que espera recibir el endpoint
# El usuario debe enviar un JSON con un campo "texto"
class Prompt(BaseModel):
    texto: str

# Define un endpoint POST en la ruta /chat
@app.post("/chat")
async def chat(prompt: Prompt):
    """
    Recibe un texto (prompt) del usuario y lo envía a OpenRouter
    para que un modelo de IA genere una respuesta.
    """
    
    # Prepara los encabezados de la petición HTTP
    # Authorization: indica qué usuario eres con tu clave API
    # Content-Type: especifica que enviamos JSON
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    
    # Prepara los datos que enviamos a OpenRouter
    # model: especifica qué modelo de IA usar
    # messages: el historial de conversación (aquí solo el mensaje del usuario)
    data = {
        "model": "openai/gpt-3.5-turbo",  # Puedes cambiar por otro modelo
        "messages": [
            {"role": "user", "content": prompt.texto}
        ]
    }
    
    # Hace una petición POST a la API de OpenRouter
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data
    )
    
    # Devuelve la respuesta de OpenRouter en formato JSON
    return response.json()