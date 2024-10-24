# %%
import pandas as pd
from pathlib import Path
import yaml
import os
import sys


CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(CODE_DIR))

from utils.load_yaml_config import load_yaml_config

configs = load_yaml_config()
consolidated_data_path = configs['paths']['processed_path_data']

# %%
def process_data(df):
    """
Processa os dados de um DataFrame de clima para adequá-los ao formato esperado pela tabela no banco de dados.

Esta função seleciona e renomeia colunas específicas de um DataFrame para corresponder à estrutura da tabela 
`processed_data` no banco de dados. 
Ela também converte as colunas de horário do nascer e pôr do sol (`sys_sunrise` e `sys_sunset`) de segundos desde a 
época Unix para um formato de data e hora (`timestamp`), que será adequado para inserção no banco de dados.

Parâmetros:
-----------
df : pandas.DataFrame
    O DataFrame contendo os dados brutos do arquivo CSV.

Processo:
---------
1. Seleciona as colunas relevantes que estão presentes no banco de dados.
2. Renomeia as colunas do DataFrame para corresponder aos nomes das colunas no banco de dados.
3. Converte as colunas `sys_sunrise` e `sys_sunset` para o formato `datetime` (de segundos Unix para timestamps).
4. Reorganiza as colunas do DataFrame para que correspondam à ordem esperada na tabela do banco de dados.
5. Retorna o DataFrame processado pronto para inserção.

Retorno:
--------
pandas.DataFrame
    Um DataFrame com as colunas selecionadas, renomeadas e reordenadas de acordo com o esquema do banco de dados.

Notas:
------
- As colunas `sys_sunrise` e `sys_sunset` são convertidas de segundos Unix para timestamps utilizando `pd.to_datetime` com a unidade de segundos.
- Certifique-se de que as colunas renomeadas correspondam exatamente às colunas na tabela do banco de dados.
"""
    #  select databse present columns
    processed_df = df[['visibility', 'timezone','id', 'name', 
                'cod', 'coord.lon', 'coord.lat', 'main.temp', 
                'main.feels_like', 'main.temp_min', 'main.temp_max', 
                'main.pressure', 'main.humidity', 'main.sea_level', 'main.grnd_level', 
                'wind.speed', 'wind.deg', 'rain.1h', 'clouds.all', 'sys.type', 'sys.id', 
                'sys.country', 'sys.sunrise', 'sys.sunset', 'Date']]
    
    #  rename columns
    processed_df.columns = ['visibility', 'timezone','id', 'name', 
                            'cod', 'coord_lon', 'coord_lat', 'main_temp', 
                            'main_feels_like', 'main_temp_min', 'main_temp_max', 
                            'main_pressure', 'main_humidity', 'main_sea_level', 'main_grnd_level', 
                            'wind_speed', 'wind_deg', 'rain_1h', 'clouds_all', 'sys_type', 'sys_id', 
                            'sys_country', 'sys_sunrise', 'sys_sunset', 'date']
    processed_df['sys_sunrise'] = pd.to_datetime(processed_df['sys_sunrise'], unit='s')
    processed_df['sys_sunset'] = pd.to_datetime(processed_df['sys_sunset'], unit='s')
    #  reorder columns to match database schema
    processed_df = processed_df[['date', 'visibility', 'timezone','id', 'name', 
                                 'cod', 'coord_lon', 'coord_lat', 'main_temp', 
                                 'main_feels_like', 'main_temp_min', 'main_temp_max', 
                                 'main_pressure', 'main_humidity', 'main_sea_level', 'main_grnd_level', 
                                 'wind_speed', 'wind_deg', 'rain_1h', 'clouds_all', 'sys_type', 'sys_id', 
                                 'sys_country', 'sys_sunrise', 'sys_sunset']]
    
    return processed_df

