import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    API_ID: int = os.getenv("API_ID")
    API_HASH: str = os.getenv("API_HASH")
    PHONE: str = os.getenv("PHONE")
    ALLOWED_USERS: list = list(map(int, os.getenv("ALLOWED_USERS").split(",")))
    
    DB_PATH: str = BASE_DIR / "database" / os.getenv("DB_PATH")
    