import sys
from pathlib import Path


project_folder = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_folder))

from main import app

