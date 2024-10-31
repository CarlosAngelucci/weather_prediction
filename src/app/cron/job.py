# %%
import requests
import pandas as pd
import os
from pathlib import Path
import sys
import warnings

CODE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(CODE_DIR))

from api.weather_api import fetch_weather_data, save_weather_data, consolidate_weather_data
from models.train_models import train_model 
from models.predict_future import predict_futre_rf
from database.insert_data import insert_predictions_data, insert_processed_data
from database.db_setup import connect_db
from utils.load_yaml_config import load_yaml_config
# %%
def main():

    #  read the predictions table from the database to make later checks
    conn = connect_db()
    warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy")
    df_predictions = pd.read_sql_query('SELECT * FROM weather_forecast', conn)
    df_predictions = df_predictions.sort_values(by='date', ascending=True)
    
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
    #  but first check if the last real temperature was inserted in the predictions table, if not, the predictions will not be made
    if df_predictions['actual_temp'].iloc[-1] != 0:
        predict_futre_rf()
        print('>>>>>>>>>>Prediction made successfully..<<<<<<<<<<')
    else:
        print('>>>>>>>>>>Real temperature not inserted yet in previous prediction. Predictions will not be made.<<<<<<<<<<')

    #  insert the processed data in the database
    insert_processed_data()

    #  insert the predictions data in the database
    insert_predictions_data()


if __name__ == '__main__':
    main()

# # %%
# ============== DEBUG ================
# conn = connect_db()
# cursor = conn.cursor()

# df = pd.read_sql_query('SELECT * FROM weather_forecast', conn)
# df = df.sort_values(by='date', ascending=True)

# last_temp = df['actual_temp'].iloc[-1]
# last_temp