import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
from utils import menu, tags_table, link_to_tag, showFF, add_control, title, dict_to_text
from collections import OrderedDict as odict

# Установка конфигурации страницы
st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

menu()

engine = create_engine('sqlite:///mydatabase.db')

# Заголовок
# get last run number and date
querie = """
SELECT MAX(CAST(run_number as INT)) as run_number, MAX(run_date) as run_date
FROM runners
"""
df = pd.read_sql(querie, con=engine)
last_run = df['run_number'].values[0]
last_date = df['run_date'].values[0]


##############################################
list_name = 'Протокол'
st.header(f"{list_name} №{last_run} {last_date[:10]}")

querie = '''
SELECT 
    r.profile_link,
    r.position,
    r.name,
    r.time
FROM runners r
WHERE run_date = (
    SELECT MAX(run_date)
    FROM runners
);
'''

df = pd.read_sql(querie, con=engine)

# Отображаем таблицу
st.data_editor(
    df,
    column_config={
        'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
        'name': st.column_config.Column(label="Имя", width='medium'), 
        'time': st.column_config.Column(label="Время", width=''), 
        'position': st.column_config.Column(label="Позиция", width=''), 
    },
    hide_index=True
)

# i = 1 # button key
# add_button(list_name, df, i)

##############################################
list_name = 'Волонтеры'
st.header(list_name)


querie = '''
SELECT 
    o.profile_link,
    o.name,
    o.volunteer_role
FROM organizers o
WHERE run_date = (
    SELECT MAX(run_date)
    FROM organizers
);
'''

df = pd.read_sql(querie, con=engine)
# names = df['name'].values

# Отображаем таблицу
st.data_editor(
    df,
    column_config={
        'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
        'name': st.column_config.Column(label="Имя", width='medium'), 
        'time': st.column_config.Column(label="Время", width=''),
        'volunteer_role': st.column_config.Column(label="Роль", width=''),
    },
    hide_index=True
)

# i = i + 1 # button key
# add_button(list_name, df, i)
button = st.button("Отчет")

if button:
    engine = create_engine('sqlite:///mydatabase.db')
    querie = '''
    SELECT * 
    FROM organizers
    WHERE run_number = (SELECT MAX(CAST(run_number as INT)) 
                        FROM organizers) 
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
    st.markdown(f'''
                Количество волонтеров: {df_comb['tag'].nunique()}  
                ''')

    st.write(dict_to_text(role_dict), unsafe_allow_html=True)