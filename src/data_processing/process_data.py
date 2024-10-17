import pandas as pd
from datetime import datetime
import sys
import os
import json

# sys.path.append(os.path.abspath(os.path.join('..', 'data')))

data_path = "/Users/kaduangelucci/Documents/Estudos/weather_prediction/data"

def consolidate_weather_data(data_folder=data_path):
    # Get all files in data folder
    files = os.listdir(data_folder)
    # Create an empty list to store the dataframes
    dfs = []
    # Loop through the files
    for file in files:
        # Check if the file is a csv file
        if file.endswith('.csv'):
            # Read the csv file
            df = pd.read_csv(os.path.join(data_folder, file))
            # Append the dataframe to the list
            dfs.append(df)
    # Concatenate all dataframes in the list
    df = pd.concat(dfs)
    # turn temperature columns into float if they are not already
    for col in ['main.temp', 'main.feels_like', 'main.temp_min', 'main.temp_max', 'main.pressure', 'main.humidity', 'wind.speed', 'wind.deg', 'clouds.all']:
        if df[col].dtype != float:
            df[col] = df[col].astype(float)
    # se a coluna date estiver usando - trocar para /

    # Return the concatenated dataframe
    df.to_csv(os.path.join(data_folder, 'processed', 'consolidado.csv'), index=False)
    return df