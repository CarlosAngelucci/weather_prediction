# %%
import pandas as pd
import pickle
import sys
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(CODE_DIR))

from data_processing.__pycache__.feature_engineering import feature_engineering
from data_processing.__pycache__.data_preprocessing import preprocess_data


from sklearn.preprocessing import StandardScaler
# %%

# %%
def predict_futre_rf():
    with open('/Users/kaduangelucci/Documents/Estudos/weather_prediction/RF_model.pkl', 'rb') as model_file:
        rf_model = pickle.load(model_file)
    
    with open('/Users/kaduangelucci/Documents/Estudos/weather_prediction/XGBoost_model.pkl', 'rb') as model_xgb_file:
        xgb_model = pickle.load(model_xgb_file)

    
    df = pd.read_csv('/Users/kaduangelucci/Documents/Estudos/weather_prediction/src/data/processed/consolidado.csv')
    df = feature_engineering(df)
    ultimo_registro = df.iloc[-1]

    novo_registro = {
        'Date': pd.to_datetime(ultimo_registro['Date']) + pd.DateOffset(hours=1),
        'main.temp': ultimo_registro['main.temp'],
        'main.feels_like': ultimo_registro['main.feels_like'],
        'main.temp_min': ultimo_registro['main.temp_min'],
        'main.temp_max': ultimo_registro['main.temp_max'],
        'main.humidity': ultimo_registro['main.humidity'],
        'wind.speed': ultimo_registro['wind.speed'],
        'main.temp_lag_1': ultimo_registro['main.temp'],
        'main.temp_lag_2': ultimo_registro['main.temp_lag_1'],
        'main.temp_lag_3': ultimo_registro['main.temp_lag_2'],
        'main.feels_like_lag_1': ultimo_registro['main.feels_like'],
        'main.feels_like_lag_2': ultimo_registro['main.feels_like_lag_1'],
        'main.feels_like_lag_3': ultimo_registro['main.feels_like_lag_2'],
        'main.temp_min_lag_1': ultimo_registro['main.temp_min'],
        'main.temp_min_lag_2': ultimo_registro['main.temp_min_lag_1'],
        'main.temp_min_lag_3': ultimo_registro['main.temp_min_lag_2'],
        'main.temp_max_lag_1': ultimo_registro['main.temp_max'],
        'main.temp_max_lag_2': ultimo_registro['main.temp_max_lag_1'],
        'main.temp_max_lag_3': ultimo_registro['main.temp_max_lag_2'],
        'main.humidity_lag_1': ultimo_registro['main.humidity'],
        'main.humidity_lag_2': ultimo_registro['main.humidity_lag_1'],
        'main.humidity_lag_3': ultimo_registro['main.humidity_lag_2'],
        'wind.speed_lag_1': ultimo_registro['wind.speed'],
        'wind.speed_lag_2': ultimo_registro['wind.speed_lag_1'],
        'wind.speed_lag_3': ultimo_registro['wind.speed_lag_2'],
    }
    novo_registro_df = pd.DataFrame([novo_registro])

    scaler = StandardScaler()
    X_train = scaler.fit_transform(df.drop(columns=['main.temp', 'Date'], axis=1))
    X_processado = scaler.transform(novo_registro_df.drop(columns=['Date', 'main.temp'], axis=1))

    predicao_rf = rf_model.predict(X_processado)
    predicao_xgb = xgb_model.predict(X_processado)

    #  adicionar a previsao ao dataframe de previsoes
    predicao_df = pd.DataFrame({'Date': novo_registro['Date'],
                                'Temperatura Real': 0,
                                'Temperatura Prevista por Random Forest': predicao_rf,
                                "Temperatura Prevista por XGBoost": predicao_xgb})
    try:
        df_predicoes = pd.read_csv('/Users/kaduangelucci/Documents/Estudos/weather_prediction/src/data/processed/predictions.csv')
        df_predicoes = pd.concat([df_predicoes, predicao_df])
    except FileNotFoundError:
        df_predicoes = predicao_df

    df_predicoes.to_csv('/Users/kaduangelucci/Documents/Estudos/weather_prediction/src/data/processed/predictions.csv', index=False)

    print(f"Predição do Random Forest: {predicao_rf} \nPredicao do XGBoost: {predicao_xgb}")


if __name__ == '__main__':
    predict_futre_rf()

