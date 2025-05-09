import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
from utils import menu, authentication, tags_table, link_to_tag, add_control

# Установка конфигурации страницы
st.set_page_config(layout='wide')

menu()
authenticator, name, authentication_status, username = authentication()

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

# Заголовок
# get last run number and date
querie = """
SELECT MAX(CAST(run_number as INT)) as run_number, MAX(run_date) as run_date
FROM runners
"""
df = pd.read_sql(querie, con=engine)
last_run = df['run_number'].values[0]
last_date = df['run_date'].values[0]

st.title('Рекорды, новички, клубы 10/25/50/100')
st.header(f"№{last_run} {last_date[:10]}")
##############################################
tables_summary = []
list_name = 'Рекорды'
st.header(list_name)

querie = '''
SELECT 
    r.profile_link,
    r.name,
    r.position,
    r.time,
    u.second_time,
    time(-strftime('%s', r.time) + strftime('%s', u.second_time), 'unixepoch' ) as dif
    --finishes,
    --volunteers,
    --achievements
FROM runners r
LEFT JOIN users u on u.profile_link = r.profile_link
WHERE (
achievements LIKE '%Личный рекорд!%' 
)
AND run_date = (
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
        'name': st.column_config.Column(label="Участник", width='medium'), 
        'time': st.column_config.Column(label="Рекорд", width=''), 
        'second_time': st.column_config.Column(label="Экс-рекорд", width=''), 
        'position': st.column_config.Column(label="Позиция", width=''), 
        'finishes': st.column_config.Column(label="# финишей", width='medium'),
        'volunteers': st.column_config.Column(label="# волонтерств", width='medium'),
        'achievements': st.column_config.Column(label="Достижения", width='large'),
    },
    hide_index=True
)

if username in ['host', 'org']:
    i = 1 # button key
    new_list = add_button(list_name, df, i)
    tables_summary.append(new_list)

##############################################
list_name = 'Первый финиш на 5 верст'
st.header(list_name)


querie = '''
SELECT 
    r.profile_link,
    r.name,
    r.position,
    r.time
    --u.second_time
    --finishes,
    --volunteers,
    --achievements
FROM runners r
LEFT JOIN users u on u.profile_link = r.profile_link
WHERE (
achievements LIKE '%Первый финиш на 5 вёрст%'
)
AND run_date = (
    SELECT MAX(run_date)
    FROM runners
);
'''

df = pd.read_sql(querie, con=engine)
# names = df['name'].values

# Отображаем таблицу
st.data_editor(
    df,
    column_config={
        'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
        'name': st.column_config.Column(label="Участник", width='medium'), 
        'time': st.column_config.Column(label="Время", width=''),
        'position': st.column_config.Column(label="Позиция", width=''), 
        'finishes': st.column_config.Column(label="# финишей", width='medium'),
        'volunteers': st.column_config.Column(label="# волонтерств", width='medium'),
        'achievements': st.column_config.Column(label="Достижения", width='large'),
    },
    hide_index=True
)

if username in ['host', 'org']:
    i = i + 1 # button key
    new_list = add_button(list_name, df, i)
    tables_summary.append(new_list)

##############################################
list_name = 'Первый финиш в Петергофе'
st.header(list_name)

querie = '''
SELECT 
    profile_link,
    name,
    time, 
    position,
    finishes
    --volunteers,
    --achievements
FROM runners
WHERE (
achievements LIKE '%Первый финиш на Петергоф%'
)
AND run_date = (
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
        'name': st.column_config.Column(label="Участник", width='medium'), 
        'time': st.column_config.Column(label="Время", width=''),
        'position': st.column_config.Column(label="Позиция", width=''), 
        'finishes': st.column_config.Column(label="# финишей", width='medium'),
        'volunteers': st.column_config.Column(label="# волонтерств", width='medium'),
        'achievements': st.column_config.Column(label="Достижения", width='large'),
    },
    hide_index=True
)

if username in ['host', 'org']:
    i = i + 1 # button key
    new_list = add_button(list_name, df, i)
    tables_summary.append(new_list)

##############################################
list_name = 'Первое волонтерство на 5 верст'
st.header(list_name)

querie = '''
WITH runner AS (
    SELECT 
        profile_link,
        time,
        run_date,
        position
    FROM runners
    WHERE run_date = (SELECT MAX(run_date) FROM runners)
    --WHERE substr(run_date, 1, 10) = "2025-01-04"
    )
SELECT 
    o.profile_link,
    o.name,
    r.time,
    r.position
FROM organizers o
LEFT JOIN runner r 
    ON r.profile_link = o.profile_link
WHERE volunteers = "1 волонтёрство"
AND o.run_date = (
    SELECT MAX(run_date)
    FROM organizers
);
'''

df = pd.read_sql(querie, con=engine)

# Отображаем таблицу
st.data_editor(
    df,
    column_config={
        'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
        'name': st.column_config.Column(label="Участник", width='medium'), 
        # 'finishes': st.column_config.Column(label="# финишей", width='medium'),
        # 'volunteers': st.column_config.Column(label="# волонтерств", width='medium'),
        # 'achievements': st.column_config.Column(label="Достижения", width='large'),
        'time': st.column_config.Column(label="Время", width=''),
        'position': st.column_config.Column(label="Позиция", width=''),
    },
    hide_index=True
)

if username in ['host', 'org']:
    i = i + 1 # button key
    new_list = add_button(list_name, df, i)
    tables_summary.append(new_list)

##############################################
list_name = 'Первое волонтерство в Петергофе'
st.header(list_name)

querie = '''
WITH runner AS (
    SELECT 
        profile_link,
        time,
        run_date,
        position
    FROM runners
    WHERE run_date = (SELECT MAX(run_date) FROM runners)
    --WHERE substr(run_date, 1, 10) = "2025-01-04"
    )
SELECT 
    u.profile_link, 
    u.name, 
    u.volunteers, 
    r.time,
    r.position
FROM organizers o
JOIN users u on u.profile_link = o.profile_link
LEFT JOIN runner r ON r.profile_link = o.profile_link
WHERE u.peterhof_volunteers_count = 1 
AND o.run_date = (
    SELECT MAX(o1.run_date)
    FROM organizers o1)
AND NOT o.volunteers = "1 волонтёрство"
;
'''

df = pd.read_sql(querie, con=engine)

# Отображаем таблицу
st.data_editor(
    df,
    column_config={
        'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
        'name': st.column_config.Column(label="Участник", width='medium'), 
        # 'finishes': st.column_config.Column(label="# финишей", width='medium'),
        'volunteers': st.column_config.Column(label="# волонтерств", width=''),
        # 'achievements': st.column_config.Column(label="Достижения", width='large'),
        'time': st.column_config.Column(label="Время", width=''),
        'position': st.column_config.Column(label="Позиция", width=''),
    },
    hide_index=True
)

if username in ['host', 'org']:
    i = i + 1 # button key
    new_list = add_button(list_name, df, i)
    tables_summary.append(new_list)

##############################################
list_name = 'Вступившие в клубы пробегов'
st.header(list_name)

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

if username in ['host', 'org']:
    i = i + 1 # button key
    new_list = add_button(list_name, df, i)
    tables_summary.append(new_list)

##############################################
list_name = 'Вступившие в клубы волонтёрств'
st.header(list_name)

querie = '''
WITH runner AS (
    SELECT 
        profile_link,
        time,
        run_date,
        position
    FROM runners
    WHERE run_date = (SELECT MAX(run_date) FROM runners)
    --WHERE substr(run_date, 1, 10) = "2025-01-04"
    )
SELECT DISTINCT o.profile_link,
        o.name,
        u.volunteers,
        --substr(o.run_date, 1, 10),
        r.time,
        r.position
    FROM organizers o
    LEFT JOIN users u
        ON o.profile_link = u.profile_link
    LEFT JOIN runner r 
        ON r.profile_link = o.profile_link
    WHERE 
        u.volunteers IN (10, 25, 50, 100, 150)
        AND o.run_date = (SELECT MAX(run_date) FROM organizers)
'''

df = pd.read_sql(querie, con=engine)

# Отображаем таблицу
st.data_editor(
    df,
    column_config={
        'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
        'name': st.column_config.Column(label="Участник", width='medium'), 
        'finishes': st.column_config.Column(label="# финишей", width=''),
        'volunteers': st.column_config.Column(label="# волонтерств", width=''),
        'time': st.column_config.Column(label="Время", width=''),
        'position': st.column_config.Column(label="Позиция", width=''),
        'achievements': st.column_config.Column(label="Достижения", width=''),
    },
    hide_index=True
)

if username in ['host', 'org']:
    i = i + 1 # button key
    new_list = add_button(list_name, df, i)
    tables_summary.append(new_list)

##############################################
list_name = 'Вторая суббота в Петергофе'
st.header(list_name)

querie = '''
WITH au as (
SELECT profile_link, name, run_date, position, Null as volunteer_role
FROM runners
WHERE profile_link LIKE "%userstats%"
UNION ALL
SELECT profile_link, name, run_date, Null as position, volunteer_role
FROM organizers 
WHERE profile_link LIKE "%userstats%")
SELECT DISTINCT au.profile_link, 
    au.name, 
    CAST(au.position AS INT) as position, 
    au.volunteer_role, 
    substr(min(au.run_date), 1, 10) as first_date, 
    CAST(us.finishes AS INT) as "Всего финишей", 
    CAST(us.volunteers AS INT) as "Всего волонтерств",
    count(distinct au.run_date) as num_subbot
FROM au
JOIN users us on au.profile_link = us.profile_link
GROUP BY au.profile_link 
HAVING max(au.run_date) = (SELECT max(run_date) FROM au) AND num_subbot = 2
'''

df = pd.read_sql(querie, con=engine)

# Отображаем таблицу
st.data_editor(
    df,
    column_config={
        'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
        'name': st.column_config.Column(label="Участник", width='medium'), 
        'volunteer_role': st.column_config.Column(label="Роль", width=''),
        'position': st.column_config.Column(label="Позиция", width=''),
        'first_date': st.column_config.Column(label="Первая суббота", width=''),
        'peterhof_finishes_count': st.column_config.Column(label="# финишей в Петергофе", width=''),
        'peterhof_volunteers_count': st.column_config.Column(label="# волонтерств в Петергофе", width=''),
        'num_subbot': st.column_config.Column(label="# суббот в Петергофе", width=''),
    },
    hide_index=True
)

if username in ['host', 'org']:
    i = i + 1 # button key
    new_list = add_button(list_name, df, i)
    tables_summary.append(new_list)

    summary = ""
    for record in tables_summary:
        summary += f"{record[0]}: {record[1]}<br>"

    st.header("Сводка")
    st.write(summary, unsafe_allow_html=True)