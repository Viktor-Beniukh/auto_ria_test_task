import time

import psycopg2

from settings.config import db_params
from db_create.database import create_cars_table
from scraper import _driver, get_all_info_cars


def insert_or_update_car_data(car_data):
    try:

        with psycopg2.connect(**db_params) as conn, conn.cursor() as cur:
            cur.execute("SELECT id FROM cars WHERE url = %s", (car_data["url"],))
            existing_id = cur.fetchone()

            field_values = {
                "title": car_data["title"],
                "price_usd": car_data["price_usd"],
                "odometer": car_data["odometer"],
                "username": car_data["username"],
                "phone_number": car_data["phone_number"],
                "image_url": car_data["image_url"],
                "images_count": car_data["image_count"],
                "car_number": car_data["car_number"],
                "car_vin": car_data["car_vin"]
            }

            if existing_id:
                update_query = """
                UPDATE cars
                SET title = %(title)s, price_usd = %(price_usd)s, odometer = %(odometer)s, 
                    username = %(username)s, phone_number = %(phone_number)s, image_url = %(image_url)s, 
                    images_count = %(images_count)s, car_number = %(car_number)s, car_vin = %(car_vin)s
                WHERE id = %(id)s;
                """
                field_values["id"] = existing_id[0]
                cur.execute(update_query, field_values)
            else:
                insert_query = """
                INSERT INTO cars (url, title, price_usd, odometer, username, phone_number, image_url, images_count, car_number, car_vin)
                VALUES (%(url)s, %(title)s, %(price_usd)s, %(odometer)s, %(username)s, %(phone_number)s, %(image_url)s, %(images_count)s, %(car_number)s, %(car_vin)s);
                """
                field_values["url"] = car_data["url"]
                cur.execute(insert_query, field_values)

            conn.commit()
        print("Data inserted/updated successfully")
    except Exception as error:
        print(f"Error inserting/updating data: {error}")


def insert_or_update_data():
    create_cars_table()
    scraped_data = get_all_info_cars(_driver)

    for data in scraped_data:
        insert_or_update_car_data(data)


if __name__ == "__main__":
    start_time = time.time()

    insert_or_update_data()
    _driver.quit()

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Script run time: {execution_time} second")
