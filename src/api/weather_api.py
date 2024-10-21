# %%
import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
import yaml
from pathlib import Path
import sys

load_dotenv(os.path.join('configs', '.env'))

API_KEY = os.getenv('API_KEY')

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(CODE_DIR))

from utils.load_yaml_config import load_yaml_config

configs = load_yaml_config()

data_path = "/Users/kaduangelucci/Documents/Estudos/weather_prediction/src/data/raw"
data_path_processed = configs['paths']['processed_path_data']
predictions_path = configs['paths']['prediction_path_data']

# data_path_processed = "/Users/kaduangelucci/Documents/Estudos/weather_prediction/src/data/processed"
# predictions_path = "/Users/kaduangelucci/Documents/Estudos/weather_prediction/src/data/predictions/predictions.csv"  # Caminho do arquivo de previsões

# %%

def fetch_weather_data(lat=-22.9056, lon=-47.0608, API_KEY=API_KEY):
    """
    Faz uma solicitação à API do OpenWeather para buscar dados meteorológicos de uma localização específica.

    Esta função envia uma requisição HTTP para a API OpenWeather, utilizando as coordenadas geográficas (latitude e longitude) e uma chave de API, retornando os dados meteorológicos no formato JSON se a solicitação for bem-sucedida.

    Parâmetros:
    - lat (float): Latitude da localização para a qual os dados meteorológicos serão buscados. O valor padrão é -22.9056 (Campinas, SP).
    - lon (float): Longitude da localização para a qual os dados meteorológicos serão buscados. O valor padrão é -47.0608 (Campinas, SP).
    - API_KEY (str): Chave da API do OpenWeather necessária para autenticar a requisição.

    Retorna:
    - dict: Dados meteorológicos retornados pela API, no formato JSON.

    Exceções:
    - Gera uma exceção se a requisição não for bem-sucedida, exibindo o código de erro HTTP e a mensagem de erro.
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    # Check if the request was successful
    print("Status da resposta da API:", response.status_code)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro: {response.status_code}, {response.text}")

def save_weather_data(data, filename='Campinas'):
    """
    Salva os dados meteorológicos em um arquivo CSV, com um nome de arquivo único baseado na data e hora atuais.

    Esta função faz o seguinte:
    1. Converte os dados meteorológicos fornecidos (em formato JSON) em um DataFrame pandas.
    2. Adiciona uma coluna 'Date' ao DataFrame, com a data e hora atuais.
    3. Salva o DataFrame em um arquivo CSV, nomeado com um prefixo fornecido e um carimbo de data/hora único.

    Parâmetros:
    - data (dict): Dados meteorológicos em formato JSON retornados pela API.
    - filename (str, opcional): O prefixo do nome do arquivo CSV. O padrão é 'Campinas'. Um carimbo de data/hora será adicionado ao nome do arquivo para garantir unicidade.

    Retorna:
    - None: A função salva o arquivo no caminho especificado e não retorna nada.

    Exemplo de uso:
        weather_data = fetch_weather_data()
        save_weather_data(weather_data, filename='Campinas')
    """
    now = datetime.now() # Get current date and time
    timestamp = now.strftime("%d_%m_%Y_%H_%M_%S") # Format timestamp
    filename = f'{filename}_{timestamp}' # Add timestamp to filename

    df = pd.json_normalize(data) # Convert json to dataframe
    df['Date'] = now.strftime('%Y/%m/%d %H:%M:%S') # Add Date column
    df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d %H:%M:%S') # Convert Date column to datetime

    df.to_csv(data_path + f'/{filename}.csv', index=False) # Save data to csv file

def consolidate_weather_data(data_folder=data_path):
    """
    Consolida os dados meteorológicos de múltiplos arquivos CSV em um único DataFrame e atualiza previsões pendentes.

    Esta função realiza as seguintes etapas:
    1. Carrega todos os arquivos CSV presentes no diretório especificado.
    2. Concatena os dados em um único DataFrame.
    3. Converte as colunas relevantes para o tipo de dado `float`, caso necessário.
    4. Ordena o DataFrame pela coluna 'Date'.
    5. Salva o DataFrame consolidado em um arquivo CSV no diretório processado.
    6. Chama a função `update_values_predicted` para atualizar previsões pendentes com os valores reais de temperatura.
    7. Retorna o DataFrame consolidado.

    Parâmetros:
    - data_folder (str, opcional): Caminho para a pasta contendo os arquivos CSV. O padrão é `data_path`.

    Retorno:
    - pd.DataFrame: O DataFrame consolidado contendo os dados de todos os arquivos CSV.

    Exemplo de uso:
        consolidated_df = consolidate_weather_data(data_folder='path/to/data')
    """
    files = os.listdir(data_folder)  # Get all files in data folder
    dfs = []  # Create an empty list to store the dataframes
    for file in files: # Loop through the files
        if file.endswith('.csv'):   # Check if the file is a csv file
            df = pd.read_csv(os.path.join(data_folder, file)) # Read the csv file
            dfs.append(df)  # Append the dataframe to the list
    
    df = pd.concat(dfs) # Concatenate all dataframes in the list
   
    for col in ['main.temp', 'main.feels_like', 'main.temp_min', 'main.temp_max', 
                'main.pressure', 'main.humidity', 'wind.speed', 'wind.deg', 'clouds.all']:  # turn temperature columns into float if they are not already
        if df[col].dtype != float:
            df[col] = df[col].astype(float)
    
    # sort values by Date
    df = df.sort_values('Date').reset_index(drop=True)

    # df.to_csv(os.path.join(data_path_processed, 'consolidado.csv'), index=False)
    df.to_csv(os.path.join(data_path_processed), index=False)

    update_values_predicted(df) # Update pending predictions with real values
    return df     # Return the concatenated dataframe


def update_values_predicted(new_data, tolerance_minutes=50):
    """
    Atualiza os valores reais de temperatura no arquivo de previsões com base nos novos dados coletados.

    Esta função faz o seguinte:
    1. Verifica se o arquivo de previsões existe. Caso contrário, exibe uma mensagem de erro.
    2. Carrega o arquivo de previsões, buscando por entradas pendentes onde o valor real da temperatura ainda não foi registrado (ou seja, onde o campo 'Temperatura Real' é 0).
    3. Converte a coluna 'Date' dos novos dados (`new_data`) para o formato de data e hora (datetime) para garantir que as comparações de tempo sejam feitas corretamente.
    4. Para cada previsão pendente, calcula a diferença de tempo (em segundos) entre o horário da previsão e os horários dos novos dados fornecidos.
    5. Seleciona o valor real de temperatura mais próximo da previsão, desde que a diferença de tempo esteja dentro de um intervalo definido por `tolerance_minutes` (padrão: 50 minutos).
    6. Atualiza o valor real no arquivo de previsões com base nos dados correspondentes mais próximos.
    7. Salva o arquivo de previsões atualizado com as novas informações.

    Parâmetros:
    - new_data: DataFrame contendo os novos dados coletados (de uma API ou outra fonte) que serão usados para atualizar as previsões.
    - tolerance_minutes: Número de minutos de tolerância para a diferença entre o horário da previsão e o horário dos novos dados reais. O valor padrão é 50 minutos.

    Exceções:
    - Se o arquivo de previsões não for encontrado, uma mensagem de erro será exibida e o processo será interrompido.
    """
    if os.path.exists(predictions_path):
        df_predictions = pd.read_csv(predictions_path)
        df_predictions['Date'] = pd.to_datetime(df_predictions['Date'])

        #  Procura previeos pendentes onde o valor real e NaN
        df_pending = df_predictions[df_predictions['Temperatura Real'] == 0]

        #  Atualiza o valor real com base na correspondencia de data/hora
        for idx, row in df_pending.iterrows():
            predicted_time = row['Date']

            new_data['Date'] = pd.to_datetime(new_data['Date'], format='%Y-%m-%d %H:%M:%S')

            if not isinstance(predicted_time, pd.Timestamp):
                predicted_time = pd.to_datetime(predicted_time)

            #  calcula a diferenca de tempo entre a previsao e os novos dados reais
            new_data['time_diff'] = new_data['Date'].apply(lambda x: abs((predicted_time - x).total_seconds()))

            #  seleciona o vaor real mais peoximo com base na diferenca de tempo
            closest_match = new_data[new_data['time_diff'] <= tolerance_minutes * 60].nsmallest(1, 'time_diff')

            if not closest_match.empty:
                df_predictions.at[idx, 'Temperatura Real'] = closest_match['main.temp'].iloc[0]
            

        #  salvar o arquivo atualizado
        df_predictions.to_csv(predictions_path, index=False)
    else:
        print("Arquivo de previsoes nao encontrado")