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
from datetime import datetime

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
                print(f'>>>>>>>>Data inserted successfully\n{len(new_data)} new records inserted.<<<<<<<<<')
        except Exception as e:
                conn.rollback()
                print(f'>>>>>>>Error: {str(e)}')
    else:
        print('>>>>>>>>>No new records to insert.<<<<<<<<')

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
            print(f'>>>>>>>>Predictions inserted successfully.<<<<<<<<\n>>>>>>>>{len(new_data)} new records inserted.<<<<<<<<')
        except Exception as e:
            conn.rollback()
            print(f'Error: {str(e)}')
    else:
        print('>>>>>>>>>No new records to insert.<<<<<<<<<')
    
    insert_real_values()

def insert_real_values():
    """
    Insere o valor da última temperatura real na tabela `weather_forecast`, correspondendo à última data presente
    na tabela de previsões.

    A função realiza os seguintes passos:
        1. Conecta ao banco de dados usando `connect_db()`.
        2. Carrega os dados das tabelas `processed_data` e `weather_forecast`.
        3. Obtém o valor da última temperatura real (`main_temp`) de `processed_data`.
        4. Obtém a última data de previsão de `weather_forecast`.
        5. Atualiza a tabela `weather_forecast`, definindo o valor `actual_temp` na última linha com o valor da 
           temperatura real correspondente.
    
    Exceções:
        Caso ocorra algum erro durante a execução do comando SQL, a transação é revertida e uma mensagem de erro é exibida.
    
    Dependências:
        - A função `connect_db()` deve retornar uma conexão válida com o banco de dados.
        - As tabelas `processed_data` e `weather_forecast` devem existir e conter as colunas `main_temp` e `date`, 
          respectivamente.
    
    Retorno:
        Nenhum valor de retorno. Exibe uma mensagem de sucesso se a operação foi bem-sucedida ou uma mensagem de erro 
        em caso de falha.

    """

    conn = connect_db()
    cursor = conn.cursor()

    # get the last processed data and predictions
    df = pd.read_sql('SELECT * from processed_data', conn)
    df = df.sort_values(by='date')
    df_predictions = pd.read_sql('SELECT * from weather_forecast', conn)
    df_predictions = df_predictions.sort_values(by='date')

    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    time_now = pd.to_datetime(time_now)

    # get the last real temperature from processed data
    real_temp = float(df['main_temp'].iloc[-1])
    # get the last date from predictions table
    last_date = df_predictions['date'].iloc[-2]

    #  check if the last date is less than the current time (it means that it is time to insert the real temperature)
    delta_time = time_now > last_date
    #  update the last row of the predictions table with the real temperature
    query = """
    UPDATE weather_forecast
    SET actual_temp = %s
    WHERE date = %s
    """
    if df_predictions['actual_temp'].iloc[-2] == 0 and delta_time:
        try:
            cursor.execute(query, (real_temp, last_date))
            conn.commit()
            print('>>>>>>>>>Real temperature inserted successfull.<<<<<<<<<<')
        except Exception as e:
            conn.rollback()
            print(f'Error: {str(e)}')
    else:
        print('>>>>>>>>>Real temperature already inserted.<<<<<<<<<<')

if __name__ == '__main__':
    insert_processed_data()
    insert_predictions_data()

# %%
# conn = connect_db()
# cursor = conn.cursor()
# # %%
# df = pd.read_sql('SELECT * from processed_data', conn)
# df = df.sort_values(by='date')
# df['main_temp'].iloc[-1]

# # %%
# df_forecast = pd.read_sql('SELECT * from weather_forecast', conn)
# df_forecast = df_forecast.sort_values(by='date')
# df_forecast['actual_temp'].iloc[-3]

# # %%
# datetime_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# datetime_now

# # %% 
# last_date = df_forecast['date'].iloc[-2]
# last_date

# # %%
# delta_time = pd.to_datetime(datetime_now) > last_date
# delta_time


# # %%
# condition = df_forecast['actual_temp'].iloc[-2] == 0 and delta_time
# condition