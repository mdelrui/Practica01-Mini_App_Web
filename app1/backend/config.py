import os

from dotenv import load_dotenv

# En local, cargamos el archivo .env ubicado en la carpeta app1
load_dotenv()

# Obtenemos la clave de la API desde las variables de entorno
API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODELO = "nvidia/nemotron-3.5-lightning:free"
