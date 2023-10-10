import psycopg2

from config import db_params
from database import create_cars_table
from main import driver, get_all_info_cars


def insert_car_data(db_params, car_data):
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        insert_query = """
        INSERT INTO cars (url, title, price_usd, odometer, username, phone_number, image_url, images_count, car_number, car_vin)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        # Додаємо дані до запиту та вставляємо їх
        cur.execute(insert_query, (
            car_data['url'], car_data['title'], car_data['price_usd'], car_data['odometer'],
            car_data['username'], car_data['phone_number'], car_data['image_url'], car_data['image_count'],
            car_data['car_number'], car_data['car_vin']
        ))
        conn.commit()

        cur.close()
        conn.close()

        print("Data inserted successfully")

    except Exception as error:
        print(f"Error inserting data: {error}")


if __name__ == "__main__":
    create_cars_table(db_params)
    scraped_data = get_all_info_cars(driver)

    for data in scraped_data:
        insert_car_data(db_params, data)
