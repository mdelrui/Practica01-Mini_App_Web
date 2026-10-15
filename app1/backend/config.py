import os
from pathlib import Path

from dotenv import load_dotenv


# Cargamos la clave guardada en el archivo .env.
load_dotenv(Path(__file__).with_name(".env"))

API_KEY = os.getenv("OPENROUTER_API_KEY")

# Datos de la API de OpenRouter.
URL = "https://openrouter.ai/api/v1/chat/completions"
MODELO = "liquid/lfm-2.5-2.6b:free"
