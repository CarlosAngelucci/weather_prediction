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
    st.title('Weather Campinas')
    
    #  Plotagem de gráficos - chama as configuracoes que estao no arquivo graphs.py
    plot_graphs(option=option, df=df, graph_type=graph_type)

    #  Tabela de dados
    display_table(df)

elif page == 'Predição':
    st.title('ML Forecast - Weather Campinas.')

    #  Plotagem de gráficos - chama as configuracoes que estao no arquivo graphs.py
    st.plotly_chart(plot_predictions(df_predictions, graph_type=graph_type))

    #  Tabela de dados
    display_table_predictions(df_predictions)

