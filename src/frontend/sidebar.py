import streamlit as st
import pandas as pd
import plotly.express as px

def config_sidebar():
    #  Selecao de gráficos
    st.sidebar.title('Menu')
    page = st.sidebar.radio('Selecione a página', 
                            ["Home", "Predição"])
    
    st.sidebar.header('Select the variable to be plotted')
    option = st.sidebar.selectbox('Choose a meteorological variable', 
                                ('Temperature', 'Feels Like', 'Minimum Temperature', 'Maximum Temperature', 'Humidity'))
    
    st.sidebar.header('Select the graph type')
    graph_type = st.sidebar.selectbox('Choose a graph type', ('line', 'scatter'))

    #  criando um espaço vazio para empurar o github para o footer
    for _ in range(0, 43):
        st.sidebar.write('')

    github_logo_url = "https://cdn.pixabay.com/photo/2022/01/30/13/33/github-6980894_1280.png"  # Logo GitHub
    repo_url = "https://github.com/CarlosAngelucci/weather_prediction/tree/main" 

    st.sidebar.markdown(f"""
        <a href="{repo_url}" target="_blank">
            <img src="{github_logo_url}" alt="GitHub" style="width: 40px;"/>
            Repositório do Projeto
        </a>
                        """, unsafe_allow_html=True)
    return option, graph_type, page