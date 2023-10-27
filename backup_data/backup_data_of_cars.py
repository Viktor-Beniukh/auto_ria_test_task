import psycopg2
import os
from settings.config import db_params


def backup_cars_data_from_db():
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        cur.execute("SELECT * FROM cars")
        rows = cur.fetchall()

        current_dir = os.path.dirname(__file__)

        project_root = os.path.abspath(os.path.join(current_dir, os.pardir))
        dumps_dir = os.path.join(project_root, "dumps")

        if not os.path.exists(dumps_dir):
            os.makedirs(dumps_dir)

        with open(os.path.join(dumps_dir, "cars_data.csv"), "w", newline="", encoding="utf-8") as file:
            for row in rows:
                file.write(",".join(str(value) for value in row) + "\n")

        cur.close()
        conn.close()

        print(f"Data from 'cars' table backed up successfully to '{dumps_dir}/cars_data.csv'")

    except Exception as error:
        print(f"Error backing up data: {error}")


if __name__ == "__main__":
    backup_cars_data_from_db()
