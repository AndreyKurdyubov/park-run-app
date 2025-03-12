import pandas as pd
from sqlalchemy import create_engine
import streamlit as st

st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

st.title('Серия суббот подряд - волонтерства на поляне (все кроме связей) и пробежки')
st.markdown('Считаются не буквально субботы, а все мероприятия')

engine = create_engine('sqlite:///mydatabase.db')
querie = '''
WITH usrs as (
SELECT name, profile_link, cast(run_number as int) as rn
FROM organizers
WHERE profile_link LIKE "%userstats%" AND volunteer_role NOT LIKE "%Связи%"
UNION ALL
SELECT name, profile_link, cast(run_number as int) as rn
FROM runners
WHERE profile_link LIKE "%userstats%"),
subbota as (
SELECT DISTINCT profile_link, rn, name
FROM usrs
ORDER BY 1, 2),
groups as (
SELECT ROW_NUMBER() OVER (ORDER BY profile_link, rn) as row_num, name, profile_link, rn,
rn - ROW_NUMBER() OVER (ORDER BY profile_link, rn) as grp
FROM subbota
ORDER BY profile_link, rn),
num_c as (
SELECT name, profile_link, min(rn) as minrn, max(rn) as maxrn, count(*) as num_consec
FROM groups
GROUP BY profile_link, grp
ORDER BY 2, 3)
SELECT name, minrn as "начало серии", maxrn as "конец серии", MAX(num_consec) as "длина серии"
FROM num_c
GROUP BY profile_link
ORDER BY 4 desc
'''

df = pd.read_sql(querie, con=engine)

# Отображаем таблицу 
st.data_editor(
    df,
    column_config={
        'profile_link': st.column_config.LinkColumn(),
    },
    hide_index=True
)


st.markdown(f'''
            Уникальных участников в таблице {len(df)}  
            ''')

st.title('Серия суббот подряд только пробежки')
st.markdown('Считаются не буквально субботы, а все мероприятия')

querie1 = '''
WITH subbota as (
SELECT name, profile_link, cast(run_number as int) as rn
FROM runners
WHERE profile_link LIKE "%userstats%"),
groups as (
SELECT ROW_NUMBER() OVER (ORDER BY profile_link, rn) as row_num, name, profile_link, rn,
rn - ROW_NUMBER() OVER (ORDER BY profile_link, rn) as grp
FROM subbota
ORDER BY profile_link, rn),
num_c as (
SELECT name, profile_link, min(rn) as minrn, max(rn) as maxrn, count(*) as num_consec
FROM groups
GROUP BY profile_link, grp
ORDER BY 2, 3)
SELECT name, minrn as "начало серии", maxrn as "конец серии", MAX(num_consec) as "длина серии"
FROM num_c
GROUP BY profile_link
ORDER BY 4 desc
'''

df1 = pd.read_sql(querie1, con=engine)

# Отображаем таблицу 
st.data_editor(
    df1,
    column_config={
        'profile_link': st.column_config.LinkColumn(),
    },
    hide_index=True
)


st.markdown(f'''
            Уникальных участников в таблице {len(df1)}  
            ''')


# querie2 = '''
# SELECT DISTINCT name, profile_link
# FROM organizers
# --WHERE profile_link NOT LIKE "%userstats%"
# '''

# df2 = pd.read_sql(querie2, con=engine)

# # Отображаем таблицу 
# st.data_editor(
#     df2,
#     column_config={
#         'profile_link': st.column_config.LinkColumn(),
#     },
#     hide_index=True
# )


# st.markdown(f'''
#             Уникальных участников в таблице {len(df2)}  
#             ''')
