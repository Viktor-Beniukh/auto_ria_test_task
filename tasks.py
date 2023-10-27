from celery import Celery

from backup_data.backup_data_of_cars import backup_cars_data_from_db
from insert_data.insert_or_update_data_to_db import insert_or_update_car_data
from settings.config import CELERY_BROKER_URL

from db_create.database import create_cars_table
from scraper import _driver, get_all_info_cars

app = Celery("auto_ria_test_task", broker=CELERY_BROKER_URL)


@app.task
def insert_or_update_data_cars_to_db():
    create_cars_table()
    scraped_data = get_all_info_cars(_driver)

    for data in scraped_data:
        insert_or_update_car_data(data)


@app.task
def backup_cars_data():
    backup_cars_data_from_db()
