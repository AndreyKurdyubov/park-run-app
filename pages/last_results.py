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
SELECT profile_link, name, run_date, 
    CAST(run_number as INT) as run_number, 
    CAST(position as INT) as position, 
    time,
    achievements
FROM runners
WHERE run_number = {run_number}
'''
df_run = pd.read_sql(querie, con=engine)

querie = f'''
SELECT profile_link, name, run_date, 
    CAST(run_number as INT) as run_number, 
    GROUP_CONCAT(volunteer_role, ', ') as roles
FROM organizers 
WHERE run_number = {run_number}
GROUP BY profile_link, run_date
'''
df_org = pd.read_sql(querie, con=engine)

df_results = df_run.merge(df_org, how='outer', on=['profile_link', 'name', 'run_number', 'run_date']
                  ).sort_values(by='position', ascending=True)

# Отображаем таблицу
st.data_editor(
    df_results,
    column_config={
        'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
        'name': st.column_config.Column(label="Участник", width='medium'), 
        'roles': st.column_config.Column(label="Роли", width='large'),
        'position': st.column_config.Column(label="Позиция", width=''),
        'time': st.column_config.Column(label="Время", width=''),
        'run_date': None,
        'run_number': None,
        'achievements': st.column_config.Column(label="Достижение", width='medium'),
    },
    hide_index=True
)

# i = 1 # button key
# add_button(list_name, df, i)

if username in ['host', 'org']:
    button = st.button("Отчет")

    if button:
        engine = create_engine('sqlite:///mydatabase.db')
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
        st.write(f'''**Отчет {run_select}**<br>
                     Количество финишеров: {df_results['position'].max():.0f}<br>
                     Количество волонтеров: {df_comb['tag'].nunique()}<br>
                     Количество уникальных участников: {len(df_results)}
                    ''', unsafe_allow_html=True)
        st.write(dict_to_text(role_dict), unsafe_allow_html=True)