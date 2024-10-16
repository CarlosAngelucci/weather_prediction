import os
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join('configs', '.env'))

API_KEY = os.getenv('API_KEY')
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

def get_weather_data(city):
    params: {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Excepetion(f"Erro: {response.status_code}, {response.text}")
