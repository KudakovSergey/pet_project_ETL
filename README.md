# 🌤 Weather ETL Pipeline

ETL-пайплайн для сбора, трансформации и визуализации данных о погоде из OpenWeatherMap.

## 🎯 Что делает

1. **Extract** — забирает текущую погоду из OpenWeatherMap по списку городов.
2. **Load** — загружает сырые данные в PostgreSQL.
3. **Transform** — агрегирует данные в витрину `daily_weather_summary` (средняя/мин/макс температура, влажность, количество замеров за день).
4. **Dashboard** — визуализирует данные через Streamlit.

## 🏗 Архитектура

OpenWeatherMap API → extract.py → PostgreSQL (raw_weather)
                                       ↓
                                  transform.py
                                       ↓
                             daily_weather_summary
                                       ↓
                                  Streamlit Dashboard

## 🛠 Стек технологий

- **Python 3.10+**
- **PostgreSQL 15** (в Docker)
- **psycopg2** — драйвер PostgreSQL
- **pandas** — трансформация данных
- **Streamlit** — дашборд
- **Docker Compose** — инфраструктура

## 🚀 Быстрый старт

### 1. Клонировать репозиторий

```bash
git clone https://github.com/your_username/weather_etl_pipeline.git
cd weather_etl_pipeline
```

### 2. Установить зависимости

```bash
pip install -r requirements.txt
```

### 3. Настроить переменные окружения

```bash
cp .env.example .env
```

Открой `.env` и вставь свой API-ключ OpenWeatherMap (получить можно на [openweathermap.org](https://openweathermap.org/api)).

### 4. Поднять PostgreSQL

```bash
docker-compose up -d
```

### 5. Запустить ETL-пайплайн

```bash
python -m etl.main
```

### 6. Открыть дашборд

```bash
streamlit run dashboard/app.py
```

Дашборд откроется по адресу: [http://localhost:8501](http://localhost:8501)

## 📂 Структура проекта

```
weather_etl_pipeline/
├── dashboard/
│   └── app.py              # Streamlit-дашборд
├── etl/
│   ├── extract.py          # Сбор данных из API
│   ├── transform.py        # Агрегация данных
│   ├── load.py             # Загрузка в PostgreSQL
│   └── main.py             # Единый пайплайн
├── sql/
│   └── create_tables.sql   # DDL таблиц
├── docker-compose.yml      # PostgreSQL в Docker
├── requirements.txt        # Зависимости
└── README.md
```

## 📊 Пример данных

Витрина `daily_weather_summary`:

| city      | date       | avg_temp | min_temp | max_temp | avg_humidity | records_count |
|-----------|------------|----------|----------|----------|--------------|---------------|
| Moscow    | 2026-09-15 | 5.20     | 4.80     | 5.60     | 78.00        | 1             |
| Kazan     | 2026-09-15 | 3.40     | 3.10     | 3.70     | 82.00        | 1             |

## 💡 Возможные улучшения

- Добавить **Airflow DAG** для запуска пайплайна по расписанию.
- Расширить список городов и метрик (давление, ветер).
- Подключить **dbt** для декларативных трансформаций.
- Настроить **CI/CD** через GitHub Actions.

## 📜 Лицензия

MIT