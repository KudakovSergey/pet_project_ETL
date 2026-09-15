-- Таблица для сырых данных о погоде
CREATE TABLE IF NOT EXISTS raw_weather (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    temperature NUMERIC(5, 2),
    feels_like NUMERIC(5, 2),
    humidity INT,
    pressure INT,
    wind_speed NUMERIC(5, 2),
    description VARCHAR(255),
    dt TIMESTAMP NOT NULL,
    loaded_at TIMESTAMP DEFAULT NOW()
);

-- Таблица для агрегированных данных (витрина)
CREATE TABLE IF NOT EXISTS daily_weather_summary (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    avg_temp NUMERIC(5, 2),
    min_temp NUMERIC(5, 2),
    max_temp NUMERIC(5, 2),
    avg_humidity NUMERIC(5, 2),
    records_count INT,
    UNIQUE (city, date)
);
