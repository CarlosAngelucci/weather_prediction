
# %%
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from pathlib import Path
import sys

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(CODE_DIR))
from data_processing.__pycache__.feature_engineering import feature_engineering
from utils.load_yaml_config import load_yaml_config

# %%
processed_data_path = '/Users/kaduangelucci/Documents/Estudos/weather_prediction/src/data/processed/consolidado.csv'
consolidate_data  = pd.read_csv(processed_data_path)

# %%
df = feature_engineering(consolidate_data)
# %%
def preprocess_data(df):
    yaml_config = load_yaml_config()

    date_col = df['Date']

    target = yaml_config['target'][0]
    X = df.drop(columns=[target, 'Date'], axis=1)
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    date_col_train, date_col_test = train_test_split(date_col, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    return X_train, X_test, y_train, y_test, date_col_test

