import streamlit as st
import pandas as pd
import plotly.express as px

def load_data():
    df = pd.read_csv('/Users/kaduangelucci/Documents/Estudos/weather_prediction/data/processed/consolidado.csv')
    return df

df = load_data()
df.Date = pd.to_datetime(df.Date, format='%Y-%m-%d %H:%M:%S')

#  Titulo da página
st.set_page_config(page_title='ML Forecast - Weather Campinas', layout='wide')

#  Titulo de aplicação
st.title('Weather Analysis and Forecast With Machine Learning - Campinas')

#  Selecao de gráficos
st.sidebar.header('Select the chart type')
option = st.sidebar.selectbox('Choose a chart type', 
                              ('Temperatura', 'Sensação Térmica', 'Temperatura Mínima', 'Temperatura Máxima', 'Umidade'))


#  Plotagem de gráficos
if option == 'Temperatura':
    fig = px.scatter(df, x='Date', y='main.temp', title='Temperature')
    st.plotly_chart(fig)

elif option == 'Sensação Térmica':
    fig = px.scatter(df, x='Date', y='main.feels_like', title='Feels Like')
    st.plotly_chart(fig)

elif option == 'Temperatura Mínima':
    fig = px.scatter(df, x='Date', y='main.temp_min', title='Minimum Temperature')
    st.plotly_chart(fig)

elif option == 'Temperatura Máxima':
    fig = px.scatter(df, x='Date', y='main.temp_max', title='Maximum Temperature')
    st.plotly_chart(fig)

elif option == 'Umidade':
    fig = px.scatter(df, x='Date', y='main.humidity', title='Humidity')
    st.plotly_chart(fig)
