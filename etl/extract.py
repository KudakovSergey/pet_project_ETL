import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

CITIES = ["Moscow", "Saint Petersburg", "Novosibirsk", "Yekaterinburg", "Kazan"]

def fetch_weather(city: str) -> dict:
    """Забирает текущую погоду для одного города."""
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru"
    }
    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

def extract_all() -> list[dict]:
    """Забирает погоду по всем городам."""
    results = []
    for city in CITIES:
        try:
            data = fetch_weather(city)
            results.append(data)
            print(f"✅ {city}: {data['main']['temp']}°C")
        except Exception as e:
            print(f"❌ Ошибка для {city}: {e}")
    return results

if __name__ == "__main__":
    data = extract_all()
    print(f"Всего получено: {len(data)} записей")
