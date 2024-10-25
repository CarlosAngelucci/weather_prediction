# %%
import requests
import pandas as pd
import os
from src.api.weather_api import fetch_weather_data, save_weather_data, consolidate_weather_data
from src.models.train_models import train_model 
from src.models.predict_future import predict_futre_rf
from src.database.insert_data import insert_predictions_data, insert_processed_data
from src.database.db_setup import connect_db
from src.utils.load_yaml_config import load_yaml_config

def main():
    # get data from api
    weather_data = fetch_weather_data()

    #  if data is fetched, save it
    if weather_data:
        save_weather_data(weather_data)
        print('Data saved successfully')
    else:
        print('Error getting data')

    #  get all csv files created and located in the raw data folder, consolidate them and save the consolidated data in the processed data folder as consolidade.csv
    consolidate_weather_data()

    #  train the model and the predictions made by the model with test data are saved in processed data folder as predictions.csv
    train_model()

    #  predict the future temperature using the trained model and save the predictions in the processed data folder as predictions.csv
    predict_futre_rf()

    #  insert the processed data in the database
    insert_processed_data()

    #  insert the predictions data in the database
    insert_predictions_data()


if __name__ == '__main__':
    main()