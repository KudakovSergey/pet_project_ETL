# 🌤 Weather ELT Pipeline with Airflow

ELT-пайплайн для сбора, загрузки, трансформации и визуализации данных о погоде из OpenWeatherMap, оркестрируемый через **Apache Airflow**.

## 🎯 Что делает

1. **Extract** — забирает текущую погоду из OpenWeatherMap по списку городов.
2. **Load** — загружает **сырые** данные в PostgreSQL (таблица `raw_weather`).
3. **Transform** — агрегирует данные **внутри PostgreSQL** в витрину `daily_weather_summary` (средняя/мин/макс температура, влажность, количество замеров за день).
4. **Orchestration** — Apache Airflow запускает пайплайн по расписанию (каждый час).
5. **Dashboard** — визуализирует данные через Streamlit.

## 🏗 Архитектура (ELT + Airflow)

```text
       ┌─────────────────────┐
       │   Apache Airflow    │
       │  (DAG: @hourly)     │
       └──────────┬──────────┘
                  │
    ┌─────────────┼─────────────┐
    ▼             ▼             ▼
┌────────┐   ┌────────┐   ┌───────────┐
│extract │──▶│  load  │──▶│ transform │
└────┬───┘   └────┬───┘   └─────┬─────┘
     │            │             │
     ▼            ▼             ▼
OpenWeather   PostgreSQL    daily_weather
   API        (raw_weather)   _summary
                                │
                                ▼
                           Streamlit
                           Dashboard

🚀 Быстрый старт

1. Клонировать репозиторий

bash
git clone https://github.com/KudakovSergey/pet_project_ELT.git
cd pet_project_ELT
2. Настроить переменные окружения

bash
cp .env.example .env
Открой .env и вставь свой API-ключ OpenWeatherMap (получить можно на openweathermap.org).

3. Запустить инфраструктуру

bash
docker-compose up -d
4. Создать базу для Airflow (один раз)

bash
docker exec -it weather_postgres psql -U postgres -c "CREATE DATABASE airflow;"
docker-compose run --rm airflow-init
5. Открыть Airflow UI

URL: http://localhost:8080
Логин: admin
Пароль: admin
Найди DAG weather_elt_pipeline, включи его (Toggle ON) и нажми ▶️ Trigger DAG.

6. Открыть дашборд

bash
streamlit run dashboard/app.py
Дашборд откроется по адресу: http://localhost:8501

📂 Структура проекта

text
weather_elt_pipeline/
├── airflow/
│   ├── dags/
│   │   ├── etl/              # копия ETL-кода для Airflow
│   │   └── weather_dag.py    # DAG для оркестрации
│   ├── logs/                 # логи Airflow
│   └── plugins/
├── dashboard/
│   └── app.py                # Streamlit-дашборд
├── etl/
│   ├── __init__.py
│   ├── extract.py            # Extract — сбор данных из API
│   ├── load.py               # Load — загрузка сырых данных в PostgreSQL
│   ├── transform.py          # Transform — агрегация в SQL
│   └── main.py               # Локальный запуск (без Airflow)
├── sql/
│   └── create_tables.sql     # DDL таблиц
├── docker-compose.yml        # PostgreSQL + Airflow
├── requirements.txt          # Зависимости
└── README.md
📊 Пример данных

Витрина daily_weather_summary:

city	date	avg_temp	min_temp	max_temp	avg_humidity	records_count
Moscow	2026-10-17	5.20	4.80	5.60	78.00	1
Kazan	2026-10-17	3.40	3.10	3.70	82.00	1
⚙️ Как работает DAG

python
t1_extract >> t2_load >> t3_transform
extract — вызывает extract_all(), возвращает данные через XCom.
load — достает данные из XCom и загружает в PostgreSQL.
transform — агрегирует данные в витрину.
Расписание: @hourly (каждый час).
Retries: 2 попытки с паузой 5 минут.
