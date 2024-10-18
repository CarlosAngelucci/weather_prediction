import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(os.path.join('configs', '.env'))

API_KEY = os.getenv('API_KEY')

data_path = "/Users/kaduangelucci/Documents/Estudos/weather_prediction/src/data/raw"
data_path_processed = "/Users/kaduangelucci/Documents/Estudos/weather_prediction/src/data/processed"

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
    now = datetime.now() # Get current date and time
    timestamp = now.strftime("%d_%m_%Y_%H_%M_%S") # Format timestamp
    filename = f'{filename}_{timestamp}' # Add timestamp to filename

    df = pd.json_normalize(data) # Convert json to dataframe
    df['Date'] = now.strftime('%Y/%m/%d %H:%M:%S') # Add Date column
    df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d %H:%M:%S') # Convert Date column to datetime

    df.to_csv(data_path + f'/{filename}.csv', index=False) # Save data to csv file


def consolidate_weather_data(data_folder=data_path):
    files = os.listdir(data_folder)  # Get all files in data folder
    dfs = []  # Create an empty list to store the dataframes
    for file in files: # Loop through the files
        if file.endswith('.csv'):   # Check if the file is a csv file
            df = pd.read_csv(os.path.join(data_folder, file)) # Read the csv file
            dfs.append(df)  # Append the dataframe to the list
    
    df = pd.concat(dfs) # Concatenate all dataframes in the list
   
    for col in ['main.temp', 'main.feels_like', 'main.temp_min', 'main.temp_max', 
                'main.pressure', 'main.humidity', 'wind.speed', 'wind.deg', 'clouds.all']:  # turn temperature columns into float if they are not already
        if df[col].dtype != float:
            df[col] = df[col].astype(float)
    
    # sort values by Date
    df = df.sort_values('Date').reset_index(drop=True)

    df.to_csv(os.path.join(data_path_processed, 'consolidado.csv'), index=False)
    return df     # Return the concatenated dataframe
