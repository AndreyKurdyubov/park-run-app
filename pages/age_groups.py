import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
from menu import menu

# Установка конфигурации страницы
st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

menu()

engine = create_engine('sqlite:///mydatabase.db')

# Заголовок
st.header('Возрастные группы все')
st.markdown('Берется актуальная (по последней пробежке) группа для каждого бегуна')

querie = '''
WITH max_ag as (
SELECT profile_link, MAX(age_group) as ag
FROM runners
GROUP BY profile_link)
SELECT ag as "Группа", count(ag) as "# участников", 
        sum(CAST(peterhof_volunteers_count as int)) as "# олонтерств Петергоф",
        sum(CAST(peterhof_finishes_count as int)) as "# пробежек Петергоф"
FROM max_ag
LEFT JOIN USERS u 
    ON max_ag.profile_link = u.profile_link
WHERE ag != ""
GROUP BY ag
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
    hide_index=True
    )

st.header('Возрастные группы 10, 10-14 и 15-19')
# st.markdown('Отсеяны те, у кого меньше 5 пробежек/волонтерств в Петергофе')

querie = '''
WITH max_ag as (
SELECT profile_link, MAX(age_group) as ag
FROM runners
GROUP BY profile_link)
SELECT ag as "Группа", count(ag) as "# участников", 
        sum(CAST(peterhof_finishes_count as int)) as "# пробежек Петергоф",
        sum(CAST(peterhof_volunteers_count as int)) as "# волонтерств Петергоф"
FROM max_ag
LEFT JOIN USERS u 
    ON max_ag.profile_link = u.profile_link
WHERE ag LIKE "%10%" OR ag LIKE "%15%"
GROUP BY ag
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
    hide_index=True
    )

st.header('Старты с наибольшим количеством детей до 19 лет')
st.markdown('Здесь не учитывается, что возрастная группа участников для давних стартов была другая')

querie = '''
WITH aProfs as (SELECT profile_link, run_date, run_number, finisher, volunteer
    FROM runners 
    WHERE profile_link LIKE "%userstats%"
    UNION ALL
    SELECT profile_link, run_date, run_number, finisher, volunteer
    FROM organizers
    WHERE profile_link LIKE "%userstats%"
    ),
max_ag as (
SELECT profile_link, MAX(age_group) as ag
FROM runners
GROUP BY profile_link)

SELECT substr(run_date, 1, 10) as date, CAST(run_number as int) as "#run", 
finisher as "#финишей", 
volunteer as "#волонтерств", 
count(ag) as "# детей"
FROM aProfs a
LEFT JOIN max_ag 
    ON max_ag.profile_link = a.profile_link
WHERE ag LIKE "%10%" OR ag LIKE "%15%"
GROUP BY run_number
ORDER BY 5 desc
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
    hide_index=True
    )


