import streamlit as st
import pandas as pd
import plotly.express as px
from sidebar import config_sidebar
from graphs import plot_graphs
from table import display_table

def load_data():
    df = pd.read_csv('/Users/kaduangelucci/Documents/Estudos/weather_prediction/data/processed/consolidado.csv')
    return df

df = load_data()
df.Date = pd.to_datetime(df.Date, format='%Y-%m-%d %H:%M:%S')
df = df.sort_values('Date')

#  Titulo da página
st.set_page_config(page_title='ML Forecast - Weather Campinas', layout='wide')

#  Titulo de aplicação
st.title('Weather Analysis and Forecast With Machine Learning - Campinas')

#  Sidebar - chama as configuracoes que estao no arquivo sidebar.py
option, graph_type = config_sidebar()

#  Plotagem de gráficos - chama as configuracoes que estao no arquivo graphs.py
plot_graphs(option=option, df=df, graph_type=graph_type)


#  Tabela de dados
display_table(df)

