# 🌤 Weather ELT Pipeline

ELT-пайплайн для сбора, загрузки и трансформации данных о погоде из OpenWeatherMap.

## 🎯 Что делает

1. **Extract** — забирает текущую погоду из OpenWeatherMap по списку городов.
2. **Load** — загружает **сырые** данные в PostgreSQL (таблица `raw_weather`).
3. **Transform** — агрегирует данные **внутри PostgreSQL** в витрину `daily_weather_summary` (средняя/мин/макс температура, влажность, количество замеров за день).
4. **Dashboard** — визуализирует данные через Streamlit.

## 🏗 Архитектура (ELT)

```
OpenWeatherMap API
        ↓
   extract.py                (Extract)
        ↓
   raw_weather               (Load — сырые данные)
        ↓
   transform.py              (Transform — SQL внутри PostgreSQL)
        ↓
   daily_weather_summary     (витрина с агрегатами)
        ↓
   Streamlit Dashboard       (визуализация)
```

## 🧠 Почему ELT, а не ETL

Этот проект реализует **ELT-подход** (Extract → Load → Transform), а не классический ETL:

| Подход | Очерёдность | Где трансформация |
|--------|-------------|-------------------|
| **ETL** | Extract → Transform → Load | Transform вне DWH (отдельный сервер) |
| **ELT** | Extract → Load → Transform | Transform внутри DWH (SQL в самой БД) |

**Почему мы используем ELT:**

- **Простота.** Не нужен отдельный ETL-сервер и `pandas` для агрегаций.
- **Скорость.** PostgreSQL делает `GROUP BY` быстрее, чем Python на больших объёмах.
- **Гибкость.** Сырые данные (`raw_weather`) остаются в БД — витрину можно пересчитать в любой момент.
- **Идемпотентность.** `ON CONFLICT DO UPDATE` позволяет запускать пайплайн многократно без дублей.
- **Современный подход.** ELT — стандарт для облачных DWH (BigQuery, Snowflake, Redshift).

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
git clone https://github.com/KudakovSergey/pet_project_ELT.git
cd pet_project_ELT
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

### 5. Запустить ELT-пайплайн

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
weather_elt_pipeline/
├── dashboard/
│   └── app.py              # Streamlit-дашборд
├── etl/
│   ├── __init__.py
│   ├── extract.py          # Extract — сбор данных из API
│   ├── load.py             # Load — загрузка сырых данных в PostgreSQL
│   ├── transform.py        # Transform — агрегация в SQL
│   └── main.py             # Оркестрация пайплайна
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
- Добавить **dbt** для декларативных трансформаций.

## 📜 Лицензия

MIT