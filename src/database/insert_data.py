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

def insert_processed_data():
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
            print('Data already exists in the database')
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

if __name__ == '__main__':
    insert_processed_data()


