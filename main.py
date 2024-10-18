# %%
import requests
import pandas as pd
import os
from src.api.weather_api import fetch_weather_data, save_weather_data, consolidate_weather_data
from src.models.train_models import train_model 
from src.models.predict_future import predict_futre_rf

def main():
    weather_data = fetch_weather_data()
    if weather_data:
        save_weather_data(weather_data)
        print('Data saved successfully')
    else:
        print('Error getting data')

    consolidate_weather_data()

    train_model()
    predict_futre_rf()

if __name__ == '__main__':
    main()