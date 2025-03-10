import pandas as pd
from sqlalchemy import create_engine
import streamlit as st

st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

st.title('Серия суббот подряд - волонтерства на поляне (все кроме связей) и пробежки')
st.markdown('Считаются не буквально субботы, а все мероприятия')

engine = create_engine('sqlite:///mydatabase.db')
querie = '''
WITH usrs as (
SELECT name, cast(run_number as int) as rn
FROM organizers
WHERE volunteer_role NOT LIKE "%Связи%"
UNION ALL
SELECT name, cast(run_number as int) as rn
FROM runners
WHERE profile_link LIKE "%userstats%"),
subbota as (
SELECT DISTINCT name, rn
FROM usrs
ORDER BY 1, 2),
groups as (
SELECT ROW_NUMBER() OVER (ORDER BY name, rn) as row_num, name, rn,
rn - ROW_NUMBER() OVER (ORDER BY name, rn) as grp
FROM subbota
ORDER BY name, rn),
num_c as (
SELECT name, min(rn) as minrn, max(rn) as maxrn, count(*) as num_consec
FROM groups
GROUP BY name, grp
ORDER BY 1, 2)
SELECT name, minrn, maxrn, num_consec
FROM num_c
--GROUP BY name
'''

# суббота
# querie = '''
# WITH sat as (
# SELECT profile_link, run_number
# FROM runners
# UNION ALL
# SELECT profile_link, run_number
# FROM organizers)
# SELECT runners.name, count(distinct sat.run_number)
# FROM sat
# LEFT JOIN runners on sat.profile_link = runners.profile_link
# GROUP by sat.profile_link
# '''
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