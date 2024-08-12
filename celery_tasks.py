
from celery import Celery

from settings import CELERY_BROKER_URL, CELERY_BACKEND_URL
from tasks.tasks import delete_cipher    # noqa


def launch_celery():
    """
    Старт приложения Celery с настройками RabbitMQ и задачей
    """
    celery = Celery(broker=CELERY_BROKER_URL, backend=CELERY_BACKEND_URL)
    celery.autodiscover_tasks(['tasks'])
    celery.conf.beat_schedule = {
        'delete_cipher': {
            'task': 'tasks.tasks.delete_cipher',
            'schedule': 60.0
        }
    }

    return celery


celery = launch_celery()
