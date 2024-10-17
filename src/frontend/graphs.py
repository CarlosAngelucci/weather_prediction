import streamlit as st
import pandas as pd
import plotly.express as px

def plot_graphs(option, df, graph_type):
    #  Plotagem de gráficos
    x = 'Date'
    if option == 'Temperature':
        y = 'main.temp'
        title = 'Temperature'
    elif option == 'Feels Like':
        y = 'main.feels_like'
        title = 'Feels Like'
    elif option == 'Minimum Temperature':
        y = 'main.temp_min'
        title = 'Minimum Temperature'
    elif option == 'Maximum Temperature':
        y = 'main.temp_max'
        title = 'Maximum Temperature'
    elif option == 'Humidity':
        y = 'main.humidity'
        title = 'Humidity'
    
    if graph_type == 'line':
        fig = px.line(df, x=x, y=y, title=title)
    elif graph_type == 'scatter':
        fig = px.scatter(df, x=x, y=y, title=title)
    
    else:
        st.write('Invalid graph type')
        return
    
    st.plotly_chart(fig)
        
    #     fig = px.graph_type(df, x='Date', y='main.temp', title='Temperature')
    #     st.plotly_chart(fig)

    # elif option == 'Sensação Térmica':
    #     fig = px.graph_type(df, x='Date', y='main.feels_like', title='Feels Like')
    #     st.plotly_chart(fig)

    # elif option == 'Temperatura Mínima':
    #     fig = px.graph_type(df, x='Date', y='main.temp_min', title='Minimum Temperature')
    #     st.plotly_chart(fig)

    # elif option == 'Temperatura Máxima':
    #     fig = px.graph_type(df, x='Date', y='main.temp_max', title='Maximum Temperature')
    #     st.plotly_chart(fig)

    # elif option == 'Umidade':
    #     fig = px.graph_type(df, x='Date', y='main.humidity', title='Humidity')
    #     st.plotly_chart(fig)