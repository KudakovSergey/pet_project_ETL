from etl.extract import extract_all
from etl.load import get_connection, create_tables, insert_weather
from etl.transform import build_daily_summary


def run_pipeline():
    print("🚀 Запуск ELT-пайплайна...")

    # 1. Extract
    print("\n📥 Шаг 1: Извлечение данных из API...")
    weather_data = extract_all()

    if not weather_data:
        print("❌ Нет данных для загрузки. Пайплайн остановлен.")
        return

    # 2. Load
    print("\n📦 Шаг 2: Загрузка данных в PostgreSQL...")
    conn = get_connection()
    try:
        create_tables(conn)
        insert_weather(conn, weather_data)

        # 3. Transform
        print("\n🔄 Шаг 3: Трансформация данных...")
        build_daily_summary(conn)
    finally:
        conn.close()

    print("\n✅ ELT-пайплайн завершён успешно!")


if __name__ == "__main__":
    run_pipeline()
