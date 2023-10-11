import psycopg2
from config import db_params
from database import create_cars_table
from scraper import driver, get_all_info_cars


def insert_or_update_car_data(db_params, car_data):
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        cur.execute("SELECT id FROM cars WHERE url = %s", (car_data["url"],))
        existing_id = cur.fetchone()

        if existing_id:
            update_query = """
            UPDATE cars
            SET title = %s, price_usd = %s, odometer = %s, username = %s, phone_number = %s,
                image_url = %s, images_count = %s, car_number = %s, car_vin = %s
            WHERE id = %s;
            """
            cur.execute(
                update_query,
                (
                    car_data["title"],
                    car_data["price_usd"],
                    car_data["odometer"],
                    car_data["username"],
                    car_data["phone_number"],
                    car_data["image_url"],
                    car_data["image_count"],
                    car_data["car_number"],
                    car_data["car_vin"],
                    existing_id[0],
                ),
            )
        else:
            insert_query = """
            INSERT INTO cars (url, title, price_usd, odometer, username, phone_number, image_url, images_count, car_number, car_vin)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cur.execute(
                insert_query,
                (
                    car_data["url"],
                    car_data["title"],
                    car_data["price_usd"],
                    car_data["odometer"],
                    car_data["username"],
                    car_data["phone_number"],
                    car_data["image_url"],
                    car_data["image_count"],
                    car_data["car_number"],
                    car_data["car_vin"],
                ),
            )

        conn.commit()
        cur.close()
        conn.close()

        print("Data inserted/updated successfully")

    except Exception as error:
        print(f"Error inserting/updating data: {error}")


if __name__ == "__main__":
    create_cars_table(db_params)
    scraped_data = get_all_info_cars(driver)

    for data in scraped_data:
        insert_or_update_car_data(db_params, data)
