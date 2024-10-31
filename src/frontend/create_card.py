import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import sys
import pandas as pd

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(CODE_DIR)

from database.db_setup import connect_db

conn = connect_db()
#  get the most recent register
weather_df = pd.read_sql('SELECT * FROM processed_data ORDER BY date DESC LIMIT 1', conn)
df_count = pd.read_sql('SELECT COUNT(main_temp) FROM processed_data', conn)
qty_data_collected = df_count.iloc[0,0]
last_temperature_collected = weather_df['main_temp'].iloc[-1]
feels_like = weather_df['main_feels_like'].mean()
card_values = [last_temperature_collected, qty_data_collected, feels_like]

def create_card(title, value, delta=None):
    fig = go.Figure(go.Indicator(
        mode="number+delta" if delta else "number",
        value=value,
        title={'text': title, 'font':{'size': 24}},
        delta={'reference': delta} if delta else None,
        number={'font': {'size': 40}, 'suffix': '°C' if value!=qty_data_collected else None},
        domain={'y': [0, 1], 'x': [0, 1]}
    ))
    fig.update_layout(
        height=150,
        width=100,
        margin=dict(t=5, b=5, l=5, r=5), #  reduced margins for spacing between cards
        paper_bgcolor="rgba(255, 75, 75, 0.4)",
        font=dict(color="white", size=20),
    )
    return fig

def display_cards(list_values=card_values):
    st.markdown("""
    <style>
    .card-container{
        display:flex;
        gap:20px;
        jsutify-content: space-between;
    }
    .card{
        background-color = rgba(255, 75,75,0.4);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.3);
    }
    </style>
""", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(len(list_values))
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.plotly_chart(create_card("Real Temperature", list_values[0]), use_container_width=True)
        st.markdown('<div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.plotly_chart(create_card("Points Collected", list_values[1]), use_container_width=True)
        st.markdown('<div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.plotly_chart(create_card("Feels Like", list_values[2]), use_container_width=True)
        st.markdown('<div>', unsafe_allow_html=True)

        