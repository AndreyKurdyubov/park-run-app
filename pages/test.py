import pandas as pd
from sqlalchemy import create_engine
import streamlit as st

st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

st.title('Тестирование')

engine = create_engine('sqlite:///mydatabase.db')

querie = '''
SELECT count(distinct profile_link)
FROM organizers
'''
df = pd.read_sql(querie, con=engine)

# Отображаем таблицу 
st.data_editor(
    df,
    column_config={
        'profile_link': st.column_config.LinkColumn(),
    },
    hide_index=True
)