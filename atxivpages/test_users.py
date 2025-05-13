import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import datetime

st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

engine = create_engine('sqlite:///mydatabase.db')

querie = '''
SELECT * FROM USERS
'''
df = pd.read_sql(querie, con=engine)
st.data_editor(
    df,
    # column_config={
    #     'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
    #     'name': st.column_config.Column(label="Участник", width=''), 
    #     'finishes': st.column_config.Column(label="# финишей", width=''),
    #     'volunteers': st.column_config.Column(label="# волонтерств", width=''),
    #     'peterhof_finishes_count': st.column_config.Column(label="# финишей Петергоф", width=''),
    #     'peterhof_volunteers_count': st.column_config.Column(label="# волонтерств Петергоф", width=''),
    #     'last_time': st.column_config.Column(label="Peterhof last-time", width=''), 
    # },
    # hide_index=True
    )
