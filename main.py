# %%
import requests
import pandas as pd
import os
from src.api.weather_api import fetch_weather_data, save_weather_data
from src.data_processing.process_data import consolidate_weather_data


def main():
    weather_data = fetch_weather_data()
    if weather_data:
        save_weather_data(weather_data)
        print('Data saved successfully')
    else:
        print('Error getting data')

df = consolidate_weather_data()

if __name__ == '__main__':
    main()