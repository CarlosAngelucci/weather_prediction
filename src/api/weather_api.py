import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(os.path.join('configs', '.env'))

API_KEY = os.getenv('API_KEY')

def fetch_weather_data(lat=-22.9056, lon=-47.0608, API_KEY=API_KEY):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    # Check if the request was successful
    print("Status da resposta da API:", response.status_code)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro: {response.status_code}, {response.text}")

def save_weather_data(data, filename='Campinas'):
    now = datetime.now()
    timestamp = now.strftime("%d_%m_%Y_%H_%M_%S") # Format timestamp
    filename = f'{filename}_{timestamp}' # Add timestamp to filename
    df = pd.json_normalize(data) # Convert json to dataframe
    df['Date'] = now.strftime('%Y/%m/%d %H:%M:%S') # Add Date column
    df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d %H:%M:%S') # Convert Date column to datetime
    if not os.path.exists('data'):
        os.makedirs('data') # Create data folder if not exists
    df.to_csv(f'data/{filename}.csv', index=False) # Save data to csv file
