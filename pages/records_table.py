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

# st.header('Таблица для сверки результатов')

# querie = '''
# SELECT 
#     profile_link,
#     name,
#     finishes,
#     volunteers,
#     achievements
# FROM runners
# WHERE (
#     finishes IN ('10 финишей', '25 финишей', '50 финишей', '100 финишей')
#     OR volunteers IN ('10 волонтёрств', '25 волонтёрств', '50 волонтёрств', '100 волонтёрств')
#     OR (achievements IS NOT NULL AND TRIM(achievements) != '')
# )
# AND run_date = (
#     SELECT MAX(run_date)
#     FROM runners
# );
# '''

# df = pd.read_sql(querie, con=engine)

# # Отображаем таблицу
# st.data_editor(
#     df,
#     column_config={
#         'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width='medium'),
#         'name': st.column_config.Column(label="Участник", width='large'), 
#         'finishes': st.column_config.Column(label="# финишей", width='medium'),
#         'volunteers': st.column_config.Column(label="# волонтерств", width='medium'),
#         'achievements': st.column_config.Column(label="Достижения", width='large'),
#     },
#     hide_index=True
# )

st.header('Рекорды')

querie = '''
SELECT 
    profile_link,
    name,
    time,
    position
    --finishes,
    --volunteers,
    --achievements
FROM runners
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
        'time': st.column_config.Column(label="Время", width=''), 
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
    profile_link,
    name,
    time,
    position
    --finishes,
    --volunteers,
    --achievements
FROM runners
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
WITH ranked_runs AS (
  SELECT 
    name,
    run_date,
    finishes,
    ROW_NUMBER() OVER (PARTITION BY name ORDER BY run_date DESC) AS run_rank
  FROM runners
)
SELECT 
    p.profile_link,
    p.name,
    p.finishes,
    p.time,
    p.position
    --rr1.run_date AS last_date,
    --rr1.finishes AS last_finishes,
    --rr2.run_date AS second_to_last_date,
    --rr2.finishes AS second_to_last_finishes
FROM (
    SELECT 
        profile_link,
        name,
        finishes,
        time,
        position
    FROM runners
    WHERE 
        finishes IN ('10 финишей', '25 финишей', '50 финишей', '100 финишей')
        AND run_date = (SELECT MAX(run_date) FROM runners)
) p
LEFT JOIN ranked_runs rr1
    ON p.name = rr1.name AND rr1.run_rank = 1
LEFT JOIN ranked_runs rr2
    ON p.name = rr2.name AND rr2.run_rank = 2;
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
        o.volunteers,
        --substr(o.run_date, 1, 10),
        r.time,
        r.position
    FROM organizers o
    LEFT JOIN runner r 
        ON r.profile_link = o.profile_link
    WHERE 
        o.volunteers IN ('10 волонтёрств', '25 волонтёрств', '50 волонтёрств', '100 волонтёрств')
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
SELECT profile_link, name, position, volunteer_role, max(run_date) as last_date, count(distinct run_date) as num_subbot
FROM au
GROUP BY profile_link 
HAVING num_subbot = 2 AND last_date = (SELECT max(run_date) FROM au)
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
        'num_subbot':  st.column_config.Column(label="Субботы", width=''),
    },
    hide_index=True
)