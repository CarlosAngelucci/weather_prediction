import pyodbc
import pandas as pd
from pathlib import Path
import os 
import sys

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(CODE_DIR))

from database.db_setup import connect_db

def fetch_data_from_db(query):
    conn = connect_db()
    df = pd.read_sql(query, conn)
    conn.close()
    return df