import psycopg2

from config import db_params


def create_cars_table(db_params):
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS cars (
            id serial PRIMARY KEY,
            url VARCHAR(255),
            title VARCHAR(255),
            price_usd INT,
            odometer INT,
            username VARCHAR(255),
            phone_number VARCHAR(255),
            image_url VARCHAR(255),
            images_count INT,
            car_number VARCHAR(255),
            car_vin VARCHAR(255),
            datetime_found TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        cur.execute(create_table_query)
        conn.commit()

        cur.close()
        conn.close()

        print("Table 'cars' created successfully")

    except Exception as error:
        print(f"Error creating table: {error}")


if __name__ == "__main__":
    create_cars_table(db_params)
