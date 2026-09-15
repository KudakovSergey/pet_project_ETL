import os
import psycopg2
from dotenv import load_dotenv
from etl.extract import extract_all

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}


def get_connection():
    """Создаёт подключение к PostgreSQL."""
    return psycopg2.connect(**DB_CONFIG)


def create_tables(conn):
    """Создаёт таблицы, если их нет."""
    with conn.cursor() as cur:
        with open("sql/create_tables.sql", "r", encoding="utf-8") as f:
            cur.execute(f.read())
    conn.commit()
    print("✅ Таблицы созданы (или уже существуют)")


def insert_weather(conn, weather_data: list[dict]):
    """Вставляет сырые данные о погоде в raw_weather."""
    insert_query = """
        INSERT INTO raw_weather 
            (city, temperature, feels_like, humidity, pressure, wind_speed, description, dt)
        VALUES (%s, %s, %s, %s, %s, %s, %s, to_timestamp(%s))
    """
    with conn.cursor() as cur:
        for item in weather_data:
            cur.execute(insert_query, (
                item["name"],
                item["main"]["temp"],
                item["main"]["feels_like"],
                item["main"]["humidity"],
                item["main"]["pressure"],
                item["wind"]["speed"],
                item["weather"][0]["description"],
                item["dt"],
            ))
    conn.commit()
    print(f"✅ Загружено {len(weather_data)} записей в raw_weather")


def main():
    weather_data = extract_all()

    conn = get_connection()
    try:
        create_tables(conn)
        insert_weather(conn, weather_data)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
