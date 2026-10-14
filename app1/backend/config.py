import os
from dotenv import load_dotenv

# Cargar el archivo .env
load_dotenv()

# Obtener la clave
API_KEY = os.getenv("OPENROUTER_API_KEY")

# Dirección de la API
URL = "https://openrouter.ai/api/v1/chat/completions"

# Modelo de inteligencia artificial
MODELO = "apodex/apodex-1.1-mini:free"
