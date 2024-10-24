import psycopg2
from psycopg2 import sql
from db_setup import connect_db


    # conn = connect_db()
    # cursor = conn.cursor(°)

def create_processed_data_table(conn):
    # Create a table for the processed data
    query = '''
    CREATE TABLE IF NOT EXISTS processed_data (
        date TIMESTAMP NOT NULL,
        visibility FLOAT,
        timezone INT,
        id INT,
        name VARCHAR(255),
        cod INT,
        coord_lon FLOAT,
        coord_lat FLOAT,
        main_temp FLOAT,
        main_feels_like FLOAT,
        main_temp_min FLOAT,
        main_temp_max FLOAT,
        main_pressure FLOAT,
        main_humidity FLOAT,
        main_sea_level FLOAT,
        main_grnd_level FLOAT,
        wind_speed FLOAT,
        wind_deg FLOAT,
        rain_1h FLOAT,
        clouds_all FLOAT,
        sys_type INT,
        sys_id INT,
        sys_country VARCHAR(255),
        sys_sunrise TIMESTAMP,
        sys_sunset TIMESTAMP
    );
    '''
    execute_query(conn, query, 'processed_data')

def create_predictions_table(conn):
    query = '''
    CREATE TABLE IF NOT EXISTS weather_forecast (
        prediction_id SERIAL PRIMARY KEY,
        date TIMESTAMP, 
        actual_temp FLOAT,
        predicted_temp_rf FLOAT,
        predicted_temp_xgb FLOAT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    '''
    execute_query(conn, query, "predictions")

def create_model_performance_table(conn):
    query = '''
    CREATE TABLE IF NOT EXISTS model_performance (
        performance_id SERIAL PRIMARY KEY,
        model VARCHAR(255),
        metric VARCHAR(255),
        value FLOAT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    '''
    execute_query(conn, query, "model_performance")


def execute_query(conn, query, table_name):
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()
            print(f"Table {table_name} created successfully")
    except Exception as e:
        print(f'Error creating {table_name}: {e}')

def main():
    conn = connect_db()
    if conn is not None:
        create_processed_data_table(conn)
        create_predictions_table(conn)
        create_model_performance_table(conn)
        conn.close() #  close the connection
        print("Database connetion closed.")

if __name__ == '__main__':
    main()
