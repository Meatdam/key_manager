import os

from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv('POSTGRES_USER')
DB_NAME = os.getenv('POSTGRES_DB')
DB_PASS = os.getenv('POSTGRES_PASSWORD')
DB_PORT = os.getenv('POSTGRES_PORT')
DB_HOST = os.getenv('POSTGRES_HOST')

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_BACKEND_URL = os.getenv('CELERY_BACKEND_URL')
