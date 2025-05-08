import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
from utils import menu

# Установка конфигурации страницы
st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

menu()

engine = create_engine('sqlite:///mydatabase.db')

# Заголовок
# st.header('Почти в крутом клубе 5 верст')

st.header('Почти 50, 100 или 150 по пробегам 5 верст')
st.markdown('Отсеяны те, у кого меньше 5 пробежек/волонтерств в Петергофе')
querie = '''
WITH Profs as (SELECT profile_link, run_date
FROM runners 
WHERE profile_link LIKE "%userstats%"
UNION ALL
SELECT profile_link, run_date
FROM organizers
WHERE profile_link LIKE "%userstats%"
),
aProfs as (SELECT profile_link, max(run_date) as last_time
FROM Profs
GROUP BY profile_link)  

SELECT u.profile_link, u.name, CAST(u.finishes as INTEGER) as "# финишей", u.peterhof_finishes_count,
substr(last_time, 1, 10) as last_time
FROM USERS u
LEFT JOIN aProfs a
ON u.profile_link = a.profile_link
WHERE ((48 <= CAST(u.finishes as INTEGER) AND CAST(u.finishes as INTEGER) <= 49) OR
       (95 <= CAST(u.finishes as INTEGER) AND CAST(u.finishes as INTEGER) <= 99) OR
       (145 <= CAST(u.finishes as INTEGER) AND CAST(u.finishes as INTEGER) <= 149))
AND u.peterhof_finishes_count > 5
ORDER BY 3 desc, 4 desc
'''

df = pd.read_sql(querie, con=engine)
st.data_editor(
    df,
    column_config={
        'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
        'name': st.column_config.Column(label="Участник", width=''), 
        'finishes': st.column_config.Column(label="# финишей", width=''),
        'volunteers': st.column_config.Column(label="# волонтерств", width=''),
        'peterhof_finishes_count': st.column_config.Column(label="# финишей Петергоф", width=''),
        'peterhof_volunteers_count': st.column_config.Column(label="# волонтерств Петергоф", width=''),
        'last_time': st.column_config.Column(label="Peterhof last-time", width=''), 
    },
    hide_index=True
    )

# st.header('Почти 50 по пробегам 5 верст')
# querie = '''
# WITH Profs as (SELECT profile_link, run_date
# FROM runners 
# WHERE profile_link LIKE "%userstats%"
# UNION ALL
# SELECT profile_link, run_date
# FROM organizers
# WHERE profile_link LIKE "%userstats%"
# ),
# aProfs as (SELECT profile_link, max(run_date) as last_time
# FROM Profs
# GROUP BY profile_link)  

# SELECT u.profile_link, u.name, u.finishes, u.peterhof_finishes_count,
# substr(last_time, 1, 10) as last_time
# FROM USERS u
# LEFT JOIN aProfs a
# ON u.profile_link = a.profile_link
# WHERE (48 <= CAST(u.finishes as INTEGER) AND CAST(u.finishes as INTEGER) <= 49) 
# AND u.peterhof_finishes_count > 5
# ORDER BY 3 desc, 4 desc
# '''
# df = pd.read_sql(querie, con=engine)
# st.data_editor(
#     df,
#     column_config={
#         'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
#         'name': st.column_config.Column(label="Участник", width=''), 
#         'finishes': st.column_config.Column(label="# финишей", width=''),
#         'volunteers': st.column_config.Column(label="# волонтерств", width=''),
#         'peterhof_finishes_count': st.column_config.Column(label="# финишей Петергоф", width=''),
#         'peterhof_volunteers_count': st.column_config.Column(label="# волонтерств Петергоф", width=''),
#         'last_time': st.column_config.Column(label="Peterhof last-time", width=''), 
#     },
#     hide_index=True
#     )

st.header('Почти 50, 100 или 150 по волонтерствам 5 верст')
querie = '''
WITH Profs as (SELECT profile_link, run_date
FROM runners 
WHERE profile_link LIKE "%userstats%"
UNION ALL
SELECT profile_link, run_date
FROM organizers
WHERE profile_link LIKE "%userstats%"
),
aProfs as (SELECT profile_link, max(run_date) as last_time
FROM Profs
GROUP BY profile_link)  

SELECT u.profile_link, u.name, CAST(u.volunteers as INTEGER) as "# волонтерств", u.peterhof_volunteers_count,
substr(last_time, 1, 10) as last_time
FROM USERS u
LEFT JOIN aProfs a
ON u.profile_link = a.profile_link
WHERE ((48 <= CAST(u.volunteers as INTEGER) AND CAST(u.volunteers as INTEGER) <= 49) OR
       (95 <= CAST(u.volunteers as INTEGER) AND CAST(u.volunteers as INTEGER) <= 99) OR
       (145 <= CAST(u.volunteers as INTEGER) AND CAST(u.volunteers as INTEGER) <= 149))
AND u.peterhof_volunteers_count > 5
ORDER BY 3 desc, 4 desc
'''

df = pd.read_sql(querie, con=engine)
st.data_editor(
    df,
    column_config={
        'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
        'name': st.column_config.Column(label="Участник", width=''), 
        'finishes': st.column_config.Column(label="# финишей", width=''),
        'volunteers': st.column_config.Column(label="# волонтерств", width=''),
        'peterhof_finishes_count': st.column_config.Column(label="# финишей Петергоф", width=''),
        'peterhof_volunteers_count': st.column_config.Column(label="# волонтерств Петергоф", width=''),
        'last_time': st.column_config.Column(label="Peterhof last-time", width=''), 
    },
    hide_index=True
    )

# st.header('Почти 50 по волонтерствам 5 верст')
# querie = '''
# WITH Profs as (SELECT profile_link, run_date
# FROM runners 
# WHERE profile_link LIKE "%userstats%"
# UNION ALL
# SELECT profile_link, run_date
# FROM organizers
# WHERE profile_link LIKE "%userstats%"
# ),
# aProfs as (SELECT profile_link, max(run_date) as last_time
# FROM Profs
# GROUP BY profile_link)  

# SELECT u.profile_link, u.name, u.volunteers, u.peterhof_volunteers_count,
# substr(last_time, 1, 10) as last_time
# FROM USERS u
# LEFT JOIN aProfs a
# ON u.profile_link = a.profile_link
# WHERE (48 <= CAST(u.volunteers as INTEGER) AND CAST(u.volunteers as INTEGER) <= 49)
# AND u.peterhof_volunteers_count > 5
# ORDER BY 3 desc, 4 desc
# '''

# df = pd.read_sql(querie, con=engine)
# st.data_editor(
#     df,
#     column_config={
#         'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
#         'name': st.column_config.Column(label="Участник", width=''), 
#         'finishes': st.column_config.Column(label="# финишей", width=''),
#         'volunteers': st.column_config.Column(label="# волонтерств", width=''),
#         'peterhof_finishes_count': st.column_config.Column(label="# финишей Петергоф", width=''),
#         'peterhof_volunteers_count': st.column_config.Column(label="# волонтерств Петергоф", width=''),
#         'last_time': st.column_config.Column(label="Peterhof last-time", width=''), 
#     },
#     hide_index=True
#     )