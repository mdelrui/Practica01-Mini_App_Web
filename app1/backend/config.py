import os
from pathlib import Path

from dotenv import load_dotenv

# Leemos la clave desde backend/.env en local.
load_dotenv(Path(__file__).with_name(".env"))

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "liquid/lfm-2.5-2.6b:free"
