import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import datetime

st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

st.title('Тестироваие')

engine = create_engine('sqlite:///mydatabase.db')

st.header('Рекорды в Петергофе М')

querie = '''
SELECT ROW_NUMBER() OVER (ORDER BY min(time)) as num, profile_link, name, min(time) as лучшее,
time(CAST(AVG(strftime('%s', time)) AS INTEGER), 'unixepoch') as среднее
FROM runners
WHERE age_group LIKE "%М%"
GROUP BY profile_link
ORDER BY 1
'''
df = pd.read_sql(querie, con=engine)
st.data_editor(
    df,
    column_config={
        'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
        # 'name_lc': st.column_config.Column(label="Участник", width='medium'), 
        # 'time': st.column_config.Column(label="Время", width=''), 
        # 'position': st.column_config.Column(label="Позиция", width=''), 
        # 'finishes': st.column_config.Column(label="# финишей", width='medium'),
        # 'volunteers': st.column_config.Column(label="# волонтерств", width='medium'),
        # 'achievements': st.column_config.Column(label="Достижения", width='large'),
    },
    hide_index=True
    )

st.header('Рекорды в Петергофе Ж')

querie = '''
SELECT ROW_NUMBER() OVER (ORDER BY min(time)) as num, profile_link, name, min(time) as лучшее,
time(CAST(AVG(strftime('%s', time)) AS INTEGER), 'unixepoch') as среднее
FROM runners
WHERE age_group LIKE "%Ж%"
GROUP BY profile_link
ORDER BY 1
'''
df = pd.read_sql(querie, con=engine)
st.data_editor(
    df,
    column_config={
        'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
        # 'name_lc': st.column_config.Column(label="Участник", width='medium'), 
        # 'time': st.column_config.Column(label="Время", width=''), 
        # 'position': st.column_config.Column(label="Позиция", width=''), 
        # 'finishes': st.column_config.Column(label="# финишей", width='medium'),
        # 'volunteers': st.column_config.Column(label="# волонтерств", width='medium'),
        # 'achievements': st.column_config.Column(label="Достижения", width='large'),
    },
    hide_index=True
    )

st.header('Среднее время М и Ж')

querie = '''
WITH gender as (select substr(age_group, 1, 1) as пол, time
FROM runners
WHERE age_group LIKE "%Ж%" or age_group LIKE "%М%")
SELECT пол, min(time) as лучшее,
time(CAST(AVG(strftime('%s', time)) AS INTEGER), 'unixepoch') as среднее,
count(*) AS финишей
FROM gender
GROUP BY пол
ORDER BY 2
'''
df = pd.read_sql(querie, con=engine)
st.data_editor(
    df,
    # column_config={
    #     'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
        # 'name_lc': st.column_config.Column(label="Участник", width='medium'), 
        # 'time': st.column_config.Column(label="Время", width=''), 
        # 'position': st.column_config.Column(label="Позиция", width=''), 
        # 'finishes': st.column_config.Column(label="# финишей", width='medium'),
        # 'volunteers': st.column_config.Column(label="# волонтерств", width='medium'),
        # 'achievements': st.column_config.Column(label="Достижения", width='large'),
    # },
    hide_index=True
    )

st.header('Общее среднее время МЖ')

querie = '''
SELECT
time(CAST(AVG(strftime('%s', time)) AS INTEGER), 'unixepoch') as среднее,
count(*) AS финишей
FROM runners
'''
df = pd.read_sql(querie, con=engine)
st.data_editor(
    df,
    # column_config={
    #     'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
        # 'name_lc': st.column_config.Column(label="Участник", width='medium'), 
        # 'time': st.column_config.Column(label="Время", width=''), 
        # 'position': st.column_config.Column(label="Позиция", width=''), 
        # 'finishes': st.column_config.Column(label="# финишей", width='medium'),
        # 'volunteers': st.column_config.Column(label="# волонтерств", width='medium'),
        # 'achievements': st.column_config.Column(label="Достижения", width='large'),
    # },
    # hide_index=True
    )

st.write("")