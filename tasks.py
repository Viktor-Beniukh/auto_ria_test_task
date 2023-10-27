from celery import Celery

from backup_data.backup_data_of_cars import backup_cars_data_from_db
from insert_data.insert_or_update_data_to_db import insert_or_update_data
from settings.config import CELERY_BROKER_URL


app = Celery("auto_ria_test_task", broker=CELERY_BROKER_URL)


@app.task
def insert_or_update_data_cars_to_db():
    insert_or_update_data()


@app.task
def backup_cars_data():
    backup_cars_data_from_db()
