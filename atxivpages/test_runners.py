import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import datetime

st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

st.title('Тестирование')

engine = create_engine('sqlite:///mydatabase.db')

querie = '''
SELECT *
FROM runners

'''
df = pd.read_sql(querie, con=engine)
st.data_editor(
    df,
    # column_config={
    #     'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
    #     'name_lc': st.column_config.Column(label="Участник", width='medium'), 
    #     'time': st.column_config.Column(label="Время", width=''), 
    #     'position': st.column_config.Column(label="Позиция", width=''), 
    #     'finishes': st.column_config.Column(label="# финишей", width='medium'),
    #     'volunteers': st.column_config.Column(label="# волонтерств", width='medium'),
    #     'achievements': st.column_config.Column(label="Достижения", width='large'),
    # },
    hide_index=True
    )
