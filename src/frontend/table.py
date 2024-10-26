# %%∫
import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path
import sys

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(CODE_DIR))

from database.db_setup import connect_db


# %%
def display_table():
    conn = connect_db()
    cursor = conn.cursor()
    df = pd.read_sql('SELECT * FROM processed_data', conn)

    column_names = {
        'date': 'Date',
        'main_temp': 'Temperature',
        'main_feels_like': 'Feels Like',
        'main_temp_min': 'Minimum Temperature',
        'main_temp_max': 'Maximum Temperature',
        'main_pressure': 'Pressure',
        'main_humidity': 'Humidity',
        'wind_speed': 'Wind Speed',
        'wind_deg': 'Wind Degree',
        'clouds_all': 'Clouds'
    }
    features = ['Date', 'Temperature', 'Feels Like', 'Minimum Temperature', 'Maximum Temperature', 'Pressure', 'Humidity', 'Wind Speed', 'Wind Degree', 'Clouds']
    df.rename(columns=column_names, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df = df.sort_values('Date')
    df.drop_duplicates(subset='Date', keep='first', inplace=True, ignore_index=True)

    st.markdown("""
    <style>
    .center-table{
                display: flex;
                justify-content: center;
                }            
                </style>
                """,unsafe_allow_html=True)
    st.markdown('<div class="center-table>', unsafe_allow_html=True)
    st.dataframe(df[features], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def display_table_predictions():
    conn = connect_db()
    cursor = conn.cursor()
    df = pd.read_sql('SELECT * FROM weather_forecast', conn)

    column_names = {
        'date': 'Date',
        'actual_temp': 'Real Temperature',
        'predicted_temp_rf': 'Predicted Temperature by Random Forest',
        'predicted_temp_xgb': 'Predicted Temperature by XGBoost'
    }
    features = ['Date', 'Real Temperature', 'Predicted Temperature by Random Forest', 'Predicted Temperature by XGBoost']
    df.rename(columns=column_names, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df = df.sort_values('Date')
    df.drop_duplicates(subset='Date', keep='first', inplace=True, ignore_index=True)

    st.markdown("""
    <style>
    .center-table{
                display: flex;
                justify-content: center;
                }            
                </style>
                """,unsafe_allow_html=True)
    st.markdown('<div class="center-table>', unsafe_allow_html=True)
    st.dataframe(df[features], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
