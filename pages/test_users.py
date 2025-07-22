import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import datetime

st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

engine = create_engine('sqlite:///mydatabase.db')

# Заголовок
# get last run number and date
querie = """
SELECT profile_link, name FROM USERS
"""
df_users = pd.read_sql(querie, con=engine)

querie = """
SELECT distinct profile_link, name FROM runners
WHERE profile_link LIKE "%userstats%"
"""
df_runs = pd.read_sql(querie, con=engine)

querie = """
SELECT distinct profile_link, name FROM organizers
WHERE profile_link LIKE "%userstats%"
"""
df_orgs = pd.read_sql(querie, con=engine)

df_all = df_runs.merge(df_orgs, how='outer', on=['profile_link', 'name'])

st.write(f'юзеров {len(df_users)}')
st.write(f'бегунов {len(df_runs)}')
st.write(f'волонтеров {len(df_orgs)}')
st.write(f'уникальных {len(df_all)}')