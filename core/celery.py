# celery -A core.celery beat для запуска бита
# celery flower -A core.celery --address=0.0.0.0 --port=5557 для проверки статуса тасков
# celery -A core.celery worker --concurrency 2 -l info -n main -Q clearing_database аналог на селери
import os

from celery import Celery  # type: ignore

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
celery_app = Celery("core")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()

celery_app.conf.beat_schedule = {
    "say-hello": {"task": "shortenurl.tasks.say_hello", "schedule": 10.0},
}
