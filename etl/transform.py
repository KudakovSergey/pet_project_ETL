import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def build_daily_summary(conn):
    """Агрегирует сырые данные в daily_weather_summary."""
    query = """
        INSERT INTO daily_weather_summary 
            (city, date, avg_temp, min_temp, max_temp, avg_humidity, records_count)
        SELECT 
            city,
            DATE(dt) AS date,
            ROUND(AVG(temperature)::numeric, 2) AS avg_temp,
            MIN(temperature) AS min_temp,
            MAX(temperature) AS max_temp,
            ROUND(AVG(humidity)::numeric, 2) AS avg_humidity,
            COUNT(*) AS records_count
        FROM raw_weather
        GROUP BY city, DATE(dt)
        ON CONFLICT (city, date) DO UPDATE SET
            avg_temp = EXCLUDED.avg_temp,
            min_temp = EXCLUDED.min_temp,
            max_temp = EXCLUDED.max_temp,
            avg_humidity = EXCLUDED.avg_humidity,
            records_count = EXCLUDED.records_count;
    """
    with conn.cursor() as cur:
        cur.execute(query)
    conn.commit()
    print("✅ Витрина daily_weather_summary обновлена")


def main():
    conn = get_connection()
    try:
        build_daily_summary(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
