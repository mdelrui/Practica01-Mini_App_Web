import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path(__file__).with_name(".env"))

API_KEY = os.getenv("OPENROUTER_API_KEY")

URL = "https://openrouter.ai/api/v1/chat/completions"

MODELO = "liquid/lfm-2.5-2.6b:free"
