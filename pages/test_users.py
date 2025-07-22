import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import datetime

st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

engine = create_engine('sqlite:///mydatabase.db')

# Заголовок
# get last run number and date
querie = """
SELECT * FROM USERS
"""
df = pd.read_sql(querie, con=engine)
st.write(len(df))
