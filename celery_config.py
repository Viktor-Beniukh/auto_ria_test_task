from celery import Celery
from celery.schedules import crontab

from settings.config import CELERY_BROKER_URL

app = Celery("auto_ria_test_task", broker=CELERY_BROKER_URL, include=["tasks"])

app.conf.timezone = "Europe/Kiev"

app.conf.beat_schedule = {
    "run-script-every-day": {
        "task": "tasks.insert_or_update_data_cars_to_db",
        "schedule": crontab(hour="12", minute="0"),
    },
    "backup-data-every-day": {
        "task": "tasks.backup_cars_data",
        "schedule": crontab(hour="0", minute="0"),
    },
}
