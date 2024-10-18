# %%
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from feature_engineering import feature_engineering
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utils.load_yaml_config import load_yaml_config

processed_data_path = '/Users/kaduangelucci/Documents/Estudos/weather_prediction/src/data/processed/consolidado.csv'
consolidate_data  = pd.read_csv(processed_data_path)

yaml_config = load_yaml_config()

df = feature_engineering(consolidate_data)

def preprocess_data(df):
    target = yaml_config['target'][0]
    X = df.drop(target, axis=1)
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    return X_train, X_test, y_train, y_test
# %%
X_train, X_test, y_train, y_test = preprocess_data(df)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)