import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
from streamlit import session_state as ss
from utils import menu, authentication, tags_table, link_to_tag, dict_to_text
from collections import OrderedDict as odict

# Установка конфигурации страницы
st.set_page_config(layout='wide')

menu()
authenticator, name, authentication_status, username = authentication()
# if 'session_start' not in ss:
#     ss.session_start = 1
#     st.rerun()

engine = create_engine('sqlite:///mydatabase.db')

# Заголовок
# get last run number and date
# querie = """
# SELECT MAX(CAST(run_number as INT)) as run_number, MAX(run_date) as run_date
# FROM runners
# """
# df = pd.read_sql(querie, con=engine)
# last_run = df['run_number'].values[0]
# last_date = df['run_date'].values[0]

querie = """
SELECT distinct(CAST(run_number as INT)) as run_number, substr(run_date, 1, 10) as run_date
FROM runners
ORDER BY run_number DESC
LIMIT 2
"""
df = pd.read_sql(querie, con=engine)
df["run"] = '#' + df['run_number'].astype(str) + ', ' + df['run_date']

run_select = st.selectbox("Выбрать номер забега", df["run"])
run_number = run_select.split(",")[0].replace("#", "") # извлечь только номер забега

##############################################
list_name = 'Протокол'
st.header(f"{list_name}\n\n**{run_select}**")

querie = f'''
WITH run as (
SELECT profile_link, name, time, run_date, CAST(run_number as INT) as run_number, position
FROM runners
WHERE run_number = {run_number}),
org as (
SELECT profile_link, name, run_date, CAST(run_number as INT) as run_number, GROUP_CONCAT(volunteer_role, ', ') as roles
FROM organizers 
WHERE run_number = {run_number}
GROUP BY profile_link, run_date)
SELECT profile_link, 
    name, 
    CAST(run.position AS INT) as position, 
    run.time,
    org.roles
FROM run FULL OUTER JOIN org USING (profile_link, name)
'''

df_total = pd.read_sql(querie, con=engine)

# Отображаем таблицу
st.data_editor(
    df_total,
    column_config={
        'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
        'name': st.column_config.Column(label="Имя", width='medium'), 
        'time': st.column_config.Column(label="Время", width=''), 
        'position': st.column_config.Column(label="Позиция", width=''), 
        'roles': st.column_config.Column(label="Роли", width='large'),
    },
    hide_index=True
)

# i = 1 # button key
# add_button(list_name, df, i)

# ##############################################
# list_name = 'Волонтеры'
# st.header(list_name)


# querie = f'''
# SELECT 
#     o.profile_link,
#     o.name,
#     o.volunteer_role
# FROM organizers o
# WHERE run_number = {run_number};
# '''

# df = pd.read_sql(querie, con=engine)
# # names = df['name'].values

# # Отображаем таблицу
# st.data_editor(
#     df,
#     column_config={
#         'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
#         'name': st.column_config.Column(label="Имя", width='medium'), 
#         'time': st.column_config.Column(label="Время", width=''),
#         'volunteer_role': st.column_config.Column(label="Роль", width=''),
#     },
#     hide_index=True
# )

# i = i + 1 # button key
# add_button(list_name, df, i)
if username in ['host', 'org']:
    button = st.button("Отчет")

    if button:
        engine = create_engine('sqlite:///mydatabase.db')
        #### финишеры
        querie = f'''
        SELECT * 
        FROM runners
        WHERE run_number = {run_number};
        '''
        df_run = pd.read_sql(querie, con=engine)
        
        #### волонтеры
        querie = f'''
        SELECT * 
        FROM organizers
        WHERE run_number = {run_number};
        '''

        df = pd.read_sql(querie, con=engine)
        df_tag = tags_table()
        df_comb = df.merge(df_tag[['profile_link', 'VK link', "Имя"]], on='profile_link', how='left')
        df_comb['tag'] = df_comb.apply(lambda row: link_to_tag(row['VK link'], row['name'], row['Имя']), axis=1)

        roles = df['volunteer_role'].values
        names = df_comb['tag'].values
        role_dict = odict()

        for k in range(len(roles)):
            if roles[k] in role_dict:
                role_dict[roles[k]].append(names[k])
            else:
                role_dict[roles[k]] = [names[k]]


        # Отображаем таблицу 
        st.write(f'''
                    **Отчет {run_select}**<br>
                    Количество финишеров: {len(df_run)}<br>
                    Количество волонтеров: {df_comb['tag'].nunique()}<br>
                    Количество уникальных участников: {len(df_total)}<br>
                    ''', unsafe_allow_html=True)

        st.write(dict_to_text(role_dict), unsafe_allow_html=True)