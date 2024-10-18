import pandas as pd
import streamlit as st
import plotly.express as px

def display_table(df):
    column_names = {
        'Date': 'Date',
        'main.temp': 'Temperature',
        'main.feels_like': 'Feels Like',
        'main.temp_min': 'Minimum Temperature',
        'main.temp_max': 'Maximum Temperature',
        'main.pressure': 'Pressure',
        'main.humidity': 'Humidity',
        'wind.speed': 'Wind Speed',
        'wind.deg': 'Wind Degree',
        'clouds.all': 'Clouds'
    }
    features = ['Date', 'Temperature', 'Feels Like', 'Minimum Temperature', 'Maximum Temperature', 'Pressure', 'Humidity', 'Wind Speed', 'Wind Degree', 'Clouds']
    df.rename(columns=column_names, inplace=True)
    df.reset_index(drop=True, inplace=True)
    st.write(df[features])
