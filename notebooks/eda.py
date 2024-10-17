# %% 
import pandas as pd
import sys
import os 
sys.path.append(os.path.abspath(os.path.join('..', 'src')))
from data_processing.process_data import consolidate_weather_data

# %%
df = pd.read_csv('/Users/kaduangelucci/Documents/Estudos/weather_prediction/data/processed/consolidado.csv')
# %%
features_to_include = ['Date', 'name', 'main.temp', 'main.feels_like', 'main.temp_min', 'main.temp_max', 'main.pressure', 'main.humidity', 'wind.speed', 'wind.deg', 'clouds.all']
df = df[features_to_include]

dict_replace = {'name': 'Cidade', 
                'main.temp': 'temperature', 
                'main.feels_like': 'feels_like', 
                'main.temp_min': 'temperature_min', 
                'main.temp_max': 'temperature_max', 
                'main.pressure': 'pressure', 
                'main.humidity': 'humidity', 
                'wind.speed': 'wind_speed', 
                'wind.deg': 'wind_deg', 
                'clouds.all': 'clouds'}
df = df.rename(columns=dict_replace)

# %%
df.Date = pd.to_datetime(df.Date, format="%Y/%m/%d %H:%M:%S")

# %%
consolidate_weather_data()