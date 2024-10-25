import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(CODE_DIR))

from utils.db_utils import fetch_data_from_db

def add_rectangle(fig, df):
    """
    Adiciona retângulos coloridos a um gráfico para destacar faixas específicas de temperatura.

    Esta função cria dois retângulos no gráfico Plotly para destacar visualmente as áreas de temperaturas abaixo e acima de 25°C:
    - Um retângulo azul claro para representar temperaturas abaixo de 25°C (0 a 24.99).
    - Um retângulo vermelho claro para representar temperaturas entre 25°C e 35°C.

    Os retângulos se estendem horizontalmente 10 horas antes e depois dos limites mínimos e máximos da coluna `date` do DataFrame.

    Parâmetros:
    -----------
    fig : plotly.graph_objects.Figure
        O objeto de figura Plotly ao qual os retângulos serão adicionados.
    
    df : pandas.DataFrame
        DataFrame contendo a coluna `date`, que define o intervalo de exibição dos retângulos no eixo x.

    Retorno:
    --------
    plotly.graph_objects.Figure
        O objeto de figura Plotly com os retângulos adicionados.

    Notas:
    ------
    - A faixa azul claro indica temperaturas abaixo de 25°C e utiliza `RoyalBlue` para a borda e `LightSkyBlue` para o preenchimento.
    - A faixa vermelho claro indica temperaturas entre 25°C e 35°C, com `red` para a borda e `LightCoral` para o preenchimento.
    - A função expande o eixo x 10 horas para cada lado dos limites de data do DataFrame para garantir que os retângulos sejam bem visíveis.
    """
    #  initial and final position of the rectangle shifted 10 hours to the left and right
    x_0 = df['date'].min()-pd.Timedelta(hours=10)
    x_1 = df['date'].max()+pd.Timedelta(hours=10)

    #  initial and final position of the blue rectangle
    y_0 = 0
    y_1 = 24.99

    #  initial and final position of the red rectangle
    y_3 = 25
    y_4 = 35

    #  adds a blue rectangle for temperatures below 25°C
    fig.add_shape(type='rect', x0=x_0, y0=y_0, x1=x_1, y1=y_1,
                line=dict(
                    color='RoyalBlue', 
                    width=2,),
                    fillcolor='LightSkyBlue',
                    opacity=0.3)
    #  adds a red rectangle for temperatures above 25°C
    fig.add_shape(type='rect', x0=x_0, y0=y_3, x1=x_1, y1=y_4,
                line=dict(
                    color='red', 
                    width=2,),
                    fillcolor='LightCoral',
                    opacity=0.3)
    return fig 

def plot_graphs(option, graph_type):
    """
    Função para plotar gráficos de diferentes variáveis climáticas com base na 
    opção e tipo de gráfico selecionados, com rótulos de dados.

    Parâmetros:
    - option: string com a opção selecionada.
    - graph_type: string com o tipo de gráfico selecionado.
    - df: DataFrame contendo os dados do clima
    """

    query = 'SELECT * FROM processed_data'
    df = fetch_data_from_db(query)
    df = df.sort_values('date')
    #  Plotagem de gráficos
    x = 'date'
    if option == 'Temperature':
        y = 'main_temp'
        title = 'Temperature'
    elif option == 'Feels Like':
        y = 'main_feels_like'
        title = 'Feels Like'
    elif option == 'Minimum Temperature':
        y = 'main_temp_min'
        title = 'Minimum Temperature'
    elif option == 'Maximum Temperature':
        y = 'main_temp_max'
        title = 'Maximum Temperature'
    elif option == 'Humidity':
        y = 'main_humidity'
        title = 'Humidity'
    
    if graph_type == 'line':
        fig = px.line(df, x=x, y=y, title=title, text=y, template='plotly_white', markers=True, line_shape='linear')
        fig.update_yaxes(title_text=title)

        fig.update_traces(mode='lines+markers',
                          textposition='top right', 
                          marker=dict(
                              size=7, 
                              color=['blue' if y <= 25 else 'red' for y in df[y]]))

        #  adds a horizontal line at 25°C
        fig.add_shape(type='line',
                      x0=df['date'].min(), y0=25, x1=df['date'].max(), y1=25,
                      line=dict(color='white', width=2, dash='dash'))
        
        #  check if its not humidity because of the scale
        if option not in ['Humidity']:
            fig = add_rectangle(fig, df)
            

    elif graph_type == 'scatter':
        fig = px.scatter(df, x=x, y=y, title=title, text=y)

        fig.update_traces(textposition='top right',
                          marker=dict(size=10, 
                                      color=['blue' if y <= 25 else 'red' for y in df[y]]))
        
        if option not in ['Humidity']:
            fig = add_rectangle(fig, df)

    else:
        st.write('Invalid graph type')
        return
    

    st.plotly_chart(fig)

def plot_predictions(graph_type):
    query = 'SELECT * FROM weather_forecast'
    df = fetch_data_from_db(query)
    df.sort_values('date', inplace=True)

    fig = go.Figure()
    if graph_type == 'line':
        fig.add_trace(go.Scatter(x=df['date'], y=df['actual_temp'], mode='lines', name='Real Temperature', line=dict(color='blue')))
        fig.add_trace(go.Scatter (x=df['date'], y=df['predicted_temp_rf'], mode='lines', name='Random Forest', line=dict(color='red')))
        fig.add_trace(go.Scatter (x=df['date'], y=df['predicted_temp_xgb'], mode='lines', name='XGBoost', line=dict(color='green')))
    elif graph_type == 'scatter':
        fig.add_trace(go.Scatter(x=df['date'], y=df['actual_temp'], mode='markers', name='Real Temperature', marker=dict(color='blue')))
        fig.add_trace(go.Scatter (x=df['date'], y=df['predicted_temp_rf'], mode='markers', name='Random Forest', marker=dict(color='red')))
        fig.add_trace(go.Scatter (x=df['date'], y=df['predicted_temp_xgb'], mode='markers', name='XGBoost', marker=dict(color='green')))
    
    fig.update_layout(title='Temperature Predictions',
                        xaxis_title='Date',
                        yaxis_title='Temperature (°C)',
                        template='presentation'
                        )
    fig.update_traces(textposition='top right')
    return fig
