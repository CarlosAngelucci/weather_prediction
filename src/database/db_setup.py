# %%
import psycopg2
from dotenv import load_dotenv
import os


load_dotenv(os.path.join('configs', '.env'))

DB_PASSWORD = os.getenv('DB_PASSWORD')

def connect_db():
    try:
        conn = psycopg2.connect(
            dbname='weather_data',
            user='kadu',
            password=DB_PASSWORD,
            host='localhost',
            port='5432'
        )
        cursor = conn.cursor()
        # Executa uma query de teste
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print(f"Você está conectado ao PostgreSQL: {record}\n")
        return conn
    except Exception as e:
        print(f'Error: {e}')


# %% 
connect_db()