import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
from menu import menu

# Установка конфигурации страницы
st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

menu()

engine = create_engine('sqlite:///mydatabase.db')

# Заголовок
st.title('Таблицы по рекордсменам, новичкам и вступившим в клубы 10/25/50/100')

st.header('Рекорды')

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

# st.write(df['name'].unique())

st.header('Первый финиш на 5 верст')

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

st.header('Первый финиш в Петергофе')

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
achievements LIKE '%Первый финиш на Петергоф Александрийский%'
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

st.header('Первое волонтерство на 5 верст')

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

st.header('Первое волонтерство в Петергофе')

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

st.header('Вступившие в клубы пробегов')
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


st.header('Вступившие в клубы волонтёрств')

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

st.header('Вторая суббота в Петергофе')

querie = '''
WITH au as (
SELECT profile_link, name, run_date, position, Null as volunteer_role
FROM runners
WHERE profile_link LIKE "%userstats%"
UNION ALL
SELECT profile_link, name, run_date, Null as position, volunteer_role
FROM organizers 
WHERE profile_link LIKE "%userstats%")
SELECT au.profile_link, au.name, CAST(au.position AS INT) as position, au.volunteer_role, max(au.run_date) as last_date, count(distinct au.run_date) as num_subbot, 
CAST(us.finishes AS INT) as finishes, 
CAST(us.volunteers AS INT) as volunteers 
--us.peterhof_finishes_count,
--us.peterhof_volunteers_count
FROM au
JOIN users us on au.profile_link = us.profile_link
GROUP BY au.profile_link 
HAVING last_date = (SELECT max(run_date) FROM au) AND 
                    (num_subbot = 2 
                    --OR 
                    --(us.peterhof_finishes_count = 2) OR 
                    --(us.peterhof_volunteers_count = 2 AND au.volunteer_role IS NOT Null)
                    )
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
        'last_date': None,
        'num_subbot':  st.column_config.Column(label="# суббот в Петергофе", width=''),
        'peterhof_finishes_count': st.column_config.Column(label="# финишей в Петергофе", width=''),
        'peterhof_volunteers_count': st.column_config.Column(label="# волонтерств в Петергофе", width=''),
    },
    hide_index=True
)