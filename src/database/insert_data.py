# %%
from pathlib import Path
import pandas as pd
import yaml
import os
import sys

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(CODE_DIR))

from utils.load_yaml_config import load_yaml_config
from database.db_setup import connect_db
from database.process_data import process_data

configs = load_yaml_config()
consolidated_data_path = configs['paths']['processed_path_data']
predictions_path = configs['paths']['prediction_path_data']
# %%
def insert_processed_data():
    """
    Insere dados de um DataFrame em uma tabela PostgreSQL, verificando a duplicidade com base na data.

    Esta função lê um arquivo CSV consolidado, processa os dados com a função `process_data`, e insere os dados na tabela `processed_data` no banco de dados PostgreSQL. Antes de cada inserção, verifica se o registro com a mesma data já existe no banco. Caso contrário, os dados são inseridos em lote para otimizar o desempenho.

    Processo:
    ---------
    1. Conecta-se ao banco de dados.
    2. Lê o arquivo CSV especificado por `consolidated_data_path` em um DataFrame.
    3. Processa o DataFrame usando a função `process_data` para ajustar as colunas conforme necessário.
    4. Itera sobre as linhas do DataFrame, verificando se a data já existe na tabela `processed_data`:
       - Se a data não estiver presente, adiciona a linha à lista `new_data` para inserção posterior.
    5. Insere os registros de `new_data` na tabela `processed_data` em lote, se houver novos dados a serem inseridos.

    Parâmetros:
    -----------
    Nenhum.

    Retorno:
    --------
    None
        A função não retorna nada, apenas insere os dados no banco de dados e imprime uma mensagem de sucesso ou erro.

    Notas:
    ------
    - O arquivo CSV deve estar no caminho especificado por `consolidated_data_path`.
    - Certifique-se de que a tabela `processed_data` tenha a estrutura correspondente aos dados fornecidos pelo DataFrame.
    - Em caso de erro durante a inserção, a transação é revertida com `conn.rollback()`.
    - Uma mensagem é exibida indicando quantos novos registros foram inseridos ou que não há novos registros para inserir.
    """
    conn = connect_db()
    cursor = conn.cursor()

    df_consolidate = pd.read_csv(consolidated_data_path)
    df = process_data(df_consolidate)
    data = list(df.itertuples(index=False, name=None))

    #  list to store data that is not duplicated
    new_data = []

    for row in df.itertuples(index=False, name=None):
        #  check if date already exists in database
        cursor.execute('SELECT date FROM processed_data WHERE date = %s', (row[0],))
        #  fetch the result
        result = cursor.fetchone()
        if not result:
            new_data.append(row)
        
    if new_data:
        query = """
        INSERT INTO processed_data (
            date, visibility, timezone, id, name, 
            cod, coord_lon, coord_lat, main_temp, 
            main_feels_like, main_temp_min, main_temp_max, 
            main_pressure, main_humidity, main_sea_level, main_grnd_level, 
            wind_speed, wind_deg, rain_1h, clouds_all, 
            sys_type, sys_id, sys_country, sys_sunrise, sys_sunset
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        try:
                cursor.executemany(query, new_data)
                conn.commit()
                print(f'Data inserted successfully\n{len(new_data)} new records inserted.')
        except Exception as e:
                conn.rollback()
                print(f'Error: {str(e)}')
    else:
        print('No new records to insert.')

def insert_predictions_data():
    """
    Insere os dados de previsões de temperatura na tabela `weather_forecast` do banco de dados.

    A função lê um arquivo CSV contendo previsões de temperatura e dados reais, verifica se registros de uma determinada data já existem no banco de dados e, caso não existam, insere novos registros. 
    A inserção é feita para as previsões de temperatura geradas por dois modelos (Random Forest e XGBoost) e a temperatura real.

    Processo:
    ---------
    1. Conecta ao banco de dados.
    2. Lê o arquivo CSV que contém as previsões e dados reais de temperatura.
    3. Itera sobre as linhas do DataFrame, verificando se a data da previsão já está presente na tabela `weather_forecast`.
    4. Se a data não estiver presente, adiciona os dados à lista `new_data` para inserção posterior.
    5. Insere os dados de `new_data` em lote na tabela `weather_forecast` para otimizar o desempenho.

    Parâmetros:
    -----------
    Nenhum.

    Retorno:
    --------
    None
        A função não retorna nada, apenas insere os dados no banco de dados e imprime uma mensagem indicando o sucesso ou o erro da operação.

    Notas:
    ------
    - O arquivo CSV lido deve estar no caminho especificado por `predictions_path`.
    - As colunas do CSV devem conter as seguintes informações, na ordem: `date`, `actual_temp`, `predicted_temp_rf`, `predicted_temp_xgb`.
    - Em caso de erro durante a inserção, a transação é revertida com `conn.rollback()`.
    - A função imprime uma mensagem indicando quantos novos registros foram inseridos ou que não há novos registros para inserir.
    """

    conn = connect_db()
    cursor = conn.cursor()

    df = pd.read_csv(predictions_path)
    data = list(df.itertuples(index=False, name=None))

    # list to store data that is not duplicated
    new_data = []

    for row in df.itertuples(index=False, name=None):
        cursor.execute('SELECT date FROM weather_forecast WHERE date = %s', (row[0],))
        result = cursor.fetchone()

        if not result:
            new_data.append(row)
        
    if new_data:
        query = """
        INSERT INTO weather_forecast (
            date, actual_temp, predicted_temp_rf, predicted_temp_xgb
        ) VALUES (%s, %s, %s, %s)
    """

        try:
            cursor.executemany(query, new_data)
            conn.commit()
            print(f'Predictions inserted successfully.\n{len(new_data)} new records inserted.')
        except Exception as e:
            conn.rollback()
            print(f'Error: {str(e)}')
    else:
        print('No new records to insert.')



if __name__ == '__main__':
    insert_processed_data()
    insert_predictions_data()


