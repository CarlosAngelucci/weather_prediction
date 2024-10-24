from pathlib import Path
import pandas as pd
import yaml
import os
import sys

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(CODE_DIR))

from utils.load_yaml_config import load_yaml_config
from db_setup import connect_db
from process_data import process_data

configs = load_yaml_config()
consolidated_data_path = configs['paths']['processed_path_data']
predictions_path = configs['paths']['prediction_path_data']

def insert_processed_data():
    """
Insere dados de um DataFrame em uma tabela PostgreSQL, verificando a duplicidade com base na data.

Esta função lê um arquivo CSV consolidado, processa os dados com a função `process_data`, e insere os dados na tabela `processed_data` no banco de dados PostgreSQL. Antes de cada inserção, verifica se o registro com a mesma data já existe no banco. Se o registro existir, ele é ignorado. Caso contrário, os dados são inseridos. A função utiliza o método `executemany` para inserir várias linhas de uma vez.

Parâmetros:
-----------
None.

Processo:
---------
1. Conexão com o banco de dados é estabelecida.
2. O arquivo CSV especificado por `consolidated_data_path` é lido em um DataFrame.
3. O DataFrame é processado pela função `process_data` para ajustar as colunas.
4. Uma lista de tuplas é criada a partir dos dados do DataFrame.
5. Para cada linha de dados:
   - A data é verificada no banco de dados.
   - Se a data já existir, o registro é ignorado.
   - Caso contrário, os dados são inseridos na tabela `processed_data`.
6. Se a inserção for bem-sucedida, a transação é confirmada (commit); caso contrário, é feito um rollback.

Exceções:
---------
- Caso ocorra algum erro durante a execução da consulta SQL, a transação é revertida (rollback) e a mensagem de erro é exibida.

Retorno:
--------
Nenhum.

Notas:
------
- O código utiliza `%s` como placeholders para os valores na query SQL.
- Certifique-se de que a tabela `processed_data` no banco de dados tenha a estrutura correspondente aos dados fornecidos.
"""
    conn = connect_db()
    cursor = conn.cursor()

    df_consolidate = pd.read_csv(consolidated_data_path)
    df = process_data(df_consolidate)
    data = list(df.itertuples(index=False, name=None))

    for row in df.itertuples(index=False, name=None):
        #  check if date already exists in database
        cursor.execute('SELECT date FROM processed_data WHERE date = %s', (row[0],))
        #  fetch the result
        result = cursor.fetchone()
        if result:
            continue
        else:
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
                cursor.executemany(query, data)
                conn.commit()
                print('Data inserted successfully')
            except Exception as e:
                conn.rollback()
                print(f'Error: {str(e)}')

def insert_predictions_data():
    """
Insere os dados de previsões de temperatura na tabela `weather_forecast` do banco de dados.

A função lê um arquivo CSV contendo previsões de temperatura e dados reais, verifica se os registros de uma determinada data já existem no banco de dados e, se não existirem, insere esses novos registros. 
A inserção é feita para as previsões de temperatura geradas por dois modelos (Random Forest e XGBoost) e a temperatura real.

Processo:
---------
1. Conecta ao banco de dados.
2. Lê o arquivo CSV que contém as previsões e dados reais de temperatura.
3. Itera sobre as linhas do DataFrame, verificando se a data da previsão já está presente na tabela `weather_forecast`.
4. Se a data não estiver presente, insere os dados correspondentes de temperatura real e previsões.
5. Garante que a inserção ocorre em lote para eficiência.

Parâmetros:
-----------
Nenhum.

Retorno:
--------
None
    A função não retorna nada. Apenas insere os dados no banco de dados e imprime uma mensagem de sucesso ou erro.

Notas:
------
- O arquivo CSV lido deve estar no caminho especificado por `predictions_path`.
- As colunas do CSV devem conter as seguintes informações, em ordem: `date`, `actual_temp`, `predicted_temp_rf`, e `predicted_temp_xgb`.
- Se ocorrer um erro durante a inserção, a operação será revertida com `conn.rollback()`.
"""

    conn = connect_db()
    cursor = conn.cursor()

    df = pd.read_csv(predictions_path)
    data = list(df.itertuples(index=False, name=None))

    for row in df.itertuples(index=False, name=None):
        cursor.execute('SELECT date FROM weather_forecast WHERE date = %s', (row[0],))
        result = cursor.fetchone()

        if result:
            continue
        else:
            query = """
            INSERT INTO weather_forecast (
                date, actual_temp, predicted_temp_rf, predicted_temp_xgb
            ) VALUES (%s, %s, %s, %s)
            """

            try:
                cursor.executemany(query, data)
                conn.commit()
                print('Predictions inserted successfully')
            except Exception as e:
                conn.rollback()
                print(f'Error: {str(e)}')



if __name__ == '__main__':
    insert_processed_data()
    insert_predictions_data()


