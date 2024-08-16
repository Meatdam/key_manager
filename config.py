import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)


DB_USER = os.getenv('POSTGRES_USER')
DB_NAME = os.getenv('POSTGRES_DB')
DB_PASS = os.getenv('POSTGRES_PASSWORD')
DB_PORT = os.getenv('POSTGRES_PORT')
DB_HOST = os.getenv('POSTGRES_HOST')
TEST_DB_NAME = os.getenv('POSTGRES_DB_TEST')
ACCESS_TOKEN_EXPIRE_MINUTES=os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_BACKEND_URL = os.getenv('CELERY_BACKEND_URL')