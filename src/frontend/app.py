import streamlit as st
import pandas as pd
import plotly.express as px
from sidebar import config_sidebar
from graphs import plot_graphs, plot_predictions
from table import display_table, display_table_predictions

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

    #  Plotagem de gráficos - chama as configuracoes que estao no arquivo graphs.py
    st.plotly_chart(plot_predictions(graph_type=graph_type))

    #  Tabela de dados
    display_table_predictions()

