import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
from streamlit import session_state as ss
from utils import menu, authentication, tags_table, link_to_tag, add_control

# Установка конфигурации страницы
st.set_page_config(layout='wide')

menu()
authenticator, name, authentication_status, username = authentication()
if 'session_start' not in ss:
    ss.session_start = 1
    st.rerun()

engine = create_engine('sqlite:///mydatabase.db')

# таблица тегов
df_tag = tags_table()

def title(string):
    return string.title()

def add_button(list_name, df, i):
    if len(df) != 0:
        df_comb = df.merge(df_tag[['profile_link', 'VK link', "Имя"]], on='profile_link', how='left')
        df_comb['tag'] = df_comb.apply(lambda row: link_to_tag(row['VK link'], row['name'], row['Имя']), axis=1)
        names = df_comb['tag'].values
        profiles = df_comb['profile_link'].values
        positions = df['position'].values
    else:
        names = df['name'].values
        profiles = df['profile_link'].values
        positions = df['position'].values
    add_control(last_run, list_name, names, positions, i)
    return [list_name, len(set(profiles))]

querie = """
SELECT MAX(CAST(run_number as INT)) as run_number, MAX(run_date) as run_date
FROM runners
"""
df = pd.read_sql(querie, con=engine)
last_run = df['run_number'].values[0]
last_date = df['run_date'].values[0]

st.header(f"Какие люди! #{last_run} {last_date[:10]}")

option = st.selectbox(
        "Сколько суббот не были в Петергофе",
        options=[5, 10, 20, 30],
        index=2,
        placeholder="Количество мероприятий",
        label_visibility='visible'
        )
querie = f'''
WITH 
usrs as (
    SELECT name, profile_link, cast(run_number as int) as rn, run_date, Null as position, volunteer_role
    FROM organizers
    WHERE profile_link LIKE "%userstats%" AND volunteer_role NOT LIKE "%Связи%"
    UNION ALL
    SELECT name, profile_link, cast(run_number as int) as rn, run_date, position, Null as volunteer_role
    FROM runners
    WHERE profile_link LIKE "%userstats%")
    ,
prevtimers as (
    SELECT profile_link, max(rn) as prev_rn, substr(run_date, 1, 10) as run_date
    FROM usrs
    WHERE rn != (SELECT max(rn) FROM usrs)
    GROUP BY profile_link
    )
SELECT u.profile_link, u.name, cast(position as INT) as position, volunteer_role, p.run_date, p.prev_rn, u.rn, u.rn - p.prev_rn - 1 as miss
FROM usrs u JOIN prevtimers p 
        on u.profile_link = p.profile_link
WHERE rn = (SELECT max(rn) FROM usrs) AND rn - prev_rn > {option}
Order by position
'''

df = pd.read_sql(querie, con=engine)
st.data_editor(
    df,
    column_config={
        'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
        'name': st.column_config.Column(label="Участник", width=''), 
        'position': st.column_config.Column(label="Позиция", width=''),
        'volunteer_role': st.column_config.Column(label="Роль", width=''),
        'run_date': st.column_config.Column(label="Предыдущая дата", width=''),
        'prev_rn': None, #st.column_config.Column(label="Предыдущий #", width=''),
        'rn': None, #st.column_config.Column(label="Последний #", width=''),
        'miss': st.column_config.Column(label="Пропущено", width=''),
    },
    hide_index=True
    )

if username in ['host', 'org']:
    i = 1 # button key
    new_list = add_button('Какие люди!', df, i)