# %% 
import pandas as pd
import sys
import os 

from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[0]
sys.path.append(str(CODE_DIR))

from src.utils.load_yaml_config import load_yaml_config
from src.data_processing.__pycache__.feature_engineering import feature_engineering
from src.data_processing.__pycache__.data_preprocessing import preprocess_data


# %%

# %%
df = pd.read_csv('/Users/kaduangelucci/Documents/Estudos/weather_prediction/src/data/processed/consolidado.csv')
df.head()

# %%
df_engineered = feature_engineering(df)
df_final = preprocess_data(df_engineered)
df_engineered.head()