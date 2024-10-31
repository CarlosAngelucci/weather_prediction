import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import sys
import os
from dotenv import load_dotenv
import time

load_dotenv(os.path.join('configs', '.env'))
API_KEY = os.getenv('API_KEY')
CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(CODE_DIR)

from sidebar import config_sidebar
from graphs import plot_graphs, plot_predictions
from table import display_table, display_table_predictions
from create_card import display_cards
from database.db_setup import connect_db
from models.predict_future import predict_futre_rf
from database.insert_data import insert_predictions_data
from api.weather_api import fetch_weather_data, save_weather_data, consolidate_weather_data

conn = connect_db()
cursor = conn.cursor()

df_processed = pd.read_sql("SELECT * from processed_data", conn)
df_processed = df_processed.sort_values(by='date')
actual_temp = df_processed['main_temp'].iloc[-1]

def load_data():
    df = pd.read_csv('/Users/kaduangelucci/Documents/Estudos/weather_prediction/src/data/processed/consolidado.csv')
    return df

df = load_data()
df.Date = pd.to_datetime(df.Date, format='%Y-%m-%d %H:%M:%S')
df = df.sort_values('Date')

df_predictions = pd.read_csv('/Users/kaduangelucci/Documents/Estudos/weather_prediction/src/data/processed/predictions.csv')


#  Titulo da página


#  Titulo de aplicação
# st.title('Weather Analysis and Forecast With Machine Learning - Campinas')
st.set_page_config(page_title='Weather Analysis and Forecast With Machine Learning - Campinas',
                   page_icon=':partly_sunny:',
                   layout='wide',
                   initial_sidebar_state='expanded')

#  Sidebar - chama as configuracoes que estao no arquivo sidebar.py
option, graph_type, page = config_sidebar()

if page == 'Home' or page == None:
    st.markdown("""
    <style>
    .centered-title{
                text-align: center;
                font-size: 50px;
                color: #FF4B4B;
    }
    </style>
                """,
                unsafe_allow_html=True)
    st.markdown('<h1 class="centered-title">Weather Campinas</h1>', unsafe_allow_html=True)
    
    display_cards()
    
    #  Plotagem de gráficos - chama as configuracoes que estao no arquivo graphs.py
    plot_graphs(option=option, graph_type=graph_type)

    #  Tabela de dados
    display_table()

elif page == 'Predição':
    st.markdown("""
    <style>
    .centered-title{
                text-align: center;
                font-size: 50px;
                color: #FF4B4B;
    }
    </style>
                """,
                unsafe_allow_html=True)
    st.markdown('<h1 class="centered-title">ML Forecast - Weather Campinas.</h1>', unsafe_allow_html=True)
    st.plotly_chart(plot_predictions(graph_type=graph_type))

    #  Tabela de dados
    display_table_predictions()

