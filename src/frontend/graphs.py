import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def plot_graphs(option, df, graph_type):
    """
    Função para plotar gráficos de diferentes variáveis climáticas com base na 
    opção e tipo de gráfico selecionados, com rótulos de dados.

    Parâmetros:
    - option: string com a opção selecionada.
    - graph_type: string com o tipo de gráfico selecionado.
    - df: DataFrame contendo os dados do clima.
    """
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
        fig = px.line(df, x=x, y=y, title=title, text=y, template='presentation', markers=True)

        fig.update_traces(mode='lines+markers',
                          textposition='top right', 
                          marker=dict(
                              size=10, 
                              color=['blue' if y <= 25 else 'red' for y in df[y]]))
        
        fig.add_shape(type='line',
                      x0=df['Date'].min(), y0=25, x1=df['Date'].max(), y1=25,
                      line=dict(color='white', width=2, dash='dash'))

    elif graph_type == 'scatter':
        fig = px.scatter(df, x=x, y=y, title=title, text=y)

        fig.update_traces(textposition='top right',
                          marker=dict(size=10, 
                                      color=['blue' if y <= 25 else 'red' for y in df[y]]))
    
    else:
        st.write('Invalid graph type')
        return
    

    st.plotly_chart(fig)

def plot_predictions(df):
    df.sort_values('Date', inplace=True)
    fig = go.Figure()

    #  adicionar a linha de temperatura real
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Temperatura Real'], mode='lines', name='Real Temperature', line=dict(color='blue')))

    #  adicionar as previsoes da random forest
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Temperatura Prevista por Random Forest'], mode='lines', name='Random Forest', line=dict(color='red')))

    #  adicionar as previsoes da XGBoost
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Temperatura Prevista por XGBoost'], mode='lines', name='XGBoost', line=dict(color='green')))

    fig.update_layout(title='Temperature Predictions',
                        xaxis_title='Date',
                        yaxis_title='Temperature (°C)',
                        template='presentation')
    fig.update_traces(textposition='top right')
    return fig
