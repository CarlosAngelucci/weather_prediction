# %%
import pandas as pd
import pickle
import sys
import os
from pathlib import Path

from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
from sklearn.metrics import mean_squared_error


CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(CODE_DIR))

from utils.load_yaml_config import load_yaml_config
from data_processing.__pycache__.data_preprocessing import preprocess_data
from data_processing.__pycache__.feature_engineering import feature_engineering

# %%
def train_model():
    """
    Treina e avalia modelos de previsão de temperatura usando Random Forest e XGBoost, 
    mantendo um histórico de previsões em um arquivo CSV.

    Esta função realiza as seguintes etapas:
    
    1. Carrega os dados processados de temperatura de um arquivo CSV.
    2. Aplica engenharia de características para criar novas features a partir dos dados originais.
    3. Realiza o pré-processamento dos dados, incluindo a padronização e a divisão em conjuntos de treino e teste.
    4. Treina os modelos especificados no arquivo de configuração YAML (Random Forest e XGBoost) utilizando os dados de treino.
    5. Gera previsões a partir dos modelos treinados com os dados de teste.
    6. Calcula e imprime o erro quadrático médio (MSE) para cada modelo.
    7. Salva os modelos treinados em arquivos pickle.
    8. Cria um DataFrame contendo as temperaturas reais e previstas, juntamente com as respectivas datas.
    9. Verifica se um arquivo de previsões ('predictions.csv') já existe:
        - Se sim, lê o arquivo existente, concatena com as novas previsões e remove duplicatas.
        - Se não, cria um novo arquivo de previsões com os dados gerados.
    10. Salva o DataFrame resultante de previsões no arquivo CSV, garantindo que as previsões anteriores sejam mantidas.

    Exceções:
        - Se houver um erro ao criar o DataFrame final (por exemplo, se os tamanhos das listas de previsões ou datas não coincidirem),
          a função imprime uma mensagem de erro indicando o problema.

    Exemplo:
        train_model()
    """
    config = load_yaml_config()
    consolidated_data_path = config['paths']['processed_path_data']
    predictions_path = config['paths']['prediction_path_data']
    # Load data
    df = pd.read_csv(consolidated_data_path)

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

    # Save predictions
    y_test = pd.Series(y_test).reset_index(drop=True)
    y_pred_rf = pd.Series(y_pred_rf).reset_index(drop=True)
    y_pred_xgb = pd.Series(y_pred_xgb).reset_index(drop=True)
    if len(date_col_test) == len(y_test) == len(y_pred):
        df_new = pd.DataFrame({'Date': date_col_test.reset_index(drop=True),
                                'Temperatura Real': y_test, 
                                'Temperatura Prevista por Random Forest': y_pred_rf, 
                                'Temperatura Prevista por XGBoost': y_pred_xgb})
        df_new.to_csv(predictions_path, index=False)

        #  verificar se o arquivo ja existe
        if os.path.exists(predictions_path):
            df_existing = pd.read_csv(predictions_path)
            #  concatenar sem duplicacoes
            df_combined = pd.concat([df_existing, df_new]).drop_duplicates(subset=['Date']).reset_index(drop=True)
            df_combined.to_csv(predictions_path, index=False)
        else:
            df_new.to_csv(predictions_path, index=False)
    else:
        print("Erro ao criar dataframe final")
    
if __name__ == '__main__':
    train_model()
