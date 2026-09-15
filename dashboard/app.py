import os
import psycopg2
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}


@st.cache_data(ttl=60)
def load_data():
    """Загружает витрину daily_weather_summary."""
    conn = psycopg2.connect(**DB_CONFIG)
    query = """
        SELECT city, date, avg_temp, min_temp, max_temp, avg_humidity, records_count
        FROM daily_weather_summary
        ORDER BY date DESC, city
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df


st.set_page_config(page_title="Weather ETL Dashboard", layout="wide")
st.title("🌤 Weather ETL Dashboard")
st.caption("Данные из OpenWeatherMap, загруженные через ETL-пайплайн")

df = load_data()

if df.empty:
    st.warning("Нет данных. Запустите ETL-пайплайн: `python -m etl.main`")
    st.stop()

# --- Фильтр по городам ---
cities = sorted(df["city"].unique())
selected_cities = st.multiselect("Выберите города", cities, default=cities)
filtered = df[df["city"].isin(selected_cities)]

# --- Метрики ---
col1, col2, col3 = st.columns(3)
col1.metric("Городов", filtered["city"].nunique())
col2.metric("Дней с данными", filtered["date"].nunique())
col3.metric("Средняя температура", f"{filtered['avg_temp'].mean():.2f}°C")

# --- График ---
st.subheader("📈 Средняя температура по дням")
chart_data = filtered.pivot_table(
    index="date", columns="city", values="avg_temp"
).sort_index()
st.line_chart(chart_data)

# --- Таблица ---
st.subheader("📋 Детальные данные")
st.dataframe(filtered, use_container_width=True)
