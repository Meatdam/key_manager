import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)

DB_URL = f"asyncpg://postgres:{os.getenv('POSTGRES_PASSWORD')}@localhost:{os.getenv('PORT')}/{os.getenv('POSTGRES_DB')}"
