import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
from menu import menu

# Установка конфигурации страницы
st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

menu()

engine = create_engine('sqlite:///mydatabase.db')

# Заголовок
# st.title('Таблицы по рекордсменам, новичкам и вступившим в клубы 10/25/50/100')

# st.header('Вступившие в клубы пробегов')
querie = '''
SELECT     
    r.profile_link,
    r.name,
    u.finishes,
    r.time,
    r.position
FROM runners r
LEFT JOIN USERS u on r.profile_link = u.profile_link
WHERE r.run_date = (SELECT max(run_date) FROM runners) AND u.finishes IN (10, 25, 50, 100, 150)
'''

df = pd.read_sql(querie, con=engine)

# Отображаем таблицу
st.data_editor(
    df,
    column_config={
        'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
        'name': st.column_config.Column(label="Участник", width='medium'), 
        'time': st.column_config.Column(label="Время", width=''),
        'position': st.column_config.Column(label="Позиция", width=''),
        'finishes': st.column_config.Column(label="# финишей", width='m'),
        'volunteers': st.column_config.Column(label="# волонтерств", width='medium'),
        'achievements': st.column_config.Column(label="Достижения", width='large'),
    },
    hide_index=True
)

name_list = df['name'].values
out_str = ''
for name in name_list:
    out_str += f'({name.title()})\n'

st.text(out_str)

# vkid = pd.read_csv('https://docs.google.com/spreadsheets/d/10okbeu3_r-Ra40n_UihuCkhw7QxzKcV2cLdQOdl_K_E/edit?gid=1805467348#gid=1805467348/export?gid=0&format=csv')

# st.dataframe(vkid)