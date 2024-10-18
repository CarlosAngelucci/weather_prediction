import streamlit as st
import pandas as pd
import plotly.express as px

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
    
    # Ajusta posicao do rotulo de dados
    # fig.update_traces(textposition='top right')

    st.plotly_chart(fig)
