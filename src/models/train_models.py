# %%
import pandas as pd
import pickle

from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
from sklearn.metrics import mean_squared_error

import sys
import os
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(CODE_DIR))

from utils.load_yaml_config import load_yaml_config
from data_processing.__pycache__.data_preprocessing import preprocess_data
from data_processing.__pycache__.feature_engineering import feature_engineering

# %%
def train_model():
    config = load_yaml_config()

    # Load data
    df = pd.read_csv('/Users/kaduangelucci/Documents/Estudos/weather_prediction/src/data/processed/consolidado.csv')

    # feature engineering
    df_engineered = feature_engineering(df)

    # preprocess data
    X_train, X_test, y_train, y_test, date_col_test = preprocess_data(df_engineered)

    y_pred_rf = []
    y_pred_xgb = []

    # Train model
    for model in config['models']:
        if model == 'random_forest':
            model = RandomForestRegressor(**config['models'][model]['params'])
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_pred_rf.extend(y_pred)
            mse = mean_squared_error(y_test, y_pred)
            print(f'Model: {model} - MSE: {mse}')
            # save model
            with open('RF_model.pkl', 'wb') as file:
                pickle.dump(model, file)
            
        elif model == 'xgboost':
            model = xgb.XGBRegressor(**config['models'][model]['params'])
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_pred_xgb.extend(y_pred)
            mse = mean_squared_error(y_test, y_pred)
            print(f'Model: {model} - MSE: {mse}')
            with open('XGBoost_model.pkl', 'wb') as file:
                pickle.dump(model, file)
        else:
            print('Model not found')

        # print results
        print(f'Model: {model} - MSE: {mse}')

    y_test = pd.Series(y_test).reset_index(drop=True)
    y_pred_rf = pd.Series(y_pred_rf).reset_index(drop=True)
    y_pred_xgb = pd.Series(y_pred_xgb).reset_index(drop=True)
    if len(date_col_test) == len(y_test) == len(y_pred):
        df_final = pd.DataFrame({'Date': date_col_test.reset_index(drop=True),
                                'Temperatura Real': y_test, 
                                'Temperatura Prevista por Random Forest': y_pred_rf, 
                                'Temperatura Prevista por XGBoost': y_pred_xgb})
        df_final.to_csv('/Users/kaduangelucci/Documents/Estudos/weather_prediction/src/data/processed/predictions.csv', index=False)
    else:
        print("Erro ao criar dataframe final")
    
if __name__ == '__main__':
    train_model()