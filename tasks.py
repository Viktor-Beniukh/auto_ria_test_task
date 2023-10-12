from celery import Celery

from insert_data.insert_or_update_data_to_db import insert_or_update_car_data
from settings.config import db_params, CELERY_BROKER_URL
from db_create.database import create_cars_table
from scraper import driver, get_all_info_cars

app = Celery("auto_ria_test_task", broker=CELERY_BROKER_URL)


@app.task
def insert_or_update_data_cars_to_db():
    create_cars_table(db_params)
    scraped_data = get_all_info_cars(driver)

    for data in scraped_data:
        insert_or_update_car_data(db_params, data)
