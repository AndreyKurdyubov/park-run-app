import pandas as pd
from sqlalchemy import create_engine
import streamlit as st

st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

st.title('Данные по пробегам и организаторам')

engine = create_engine('sqlite:///mydatabase.db')
querie = '''
WITH orgs as (
SELECT DISTINCT name, cast(run_number as int) as rn
FROM organizers
WHERE volunteer_role NOT LIKE "%Связи%"
ORDER BY 1, 2),
groups as (
SELECT ROW_NUMBER() OVER (ORDER BY name, rn) as row_num, name, rn,
rn - ROW_NUMBER() OVER (ORDER BY name, rn) as grp
FROM orgs
ORDER BY name, rn),
num_c as (
SELECT name, min(rn) as minrn, max(rn) as maxrn, count(*) as num_consec
FROM groups
GROUP BY name, grp
ORDER BY 1, 2)
SELECT name, minrn, maxrn, max(num_consec)
FROM num_c
GROUP BY name
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

# df['run_date'] = pd.to_datetime(df['run_date'])
# df['run_date'] = df['run_date'].dt.strftime('%d.%m.%Y')

# st.write(f'Всего событий {len(df)}')
# unique_orgs_number = len(df['participant_id'].unique())
# st.write(f'Уникальных участников {unique_orgs_number}')

# Отображаем таблицу 
st.data_editor(
    df,
    column_config={
        'profile_link': st.column_config.LinkColumn(),
    },
    hide_index=True
)

# array_of_roles = df['volunteer_role'].unique()
# roles = [role.split(', ') for role in array_of_roles]
# unique_roles = []
# for role in roles:
#     unique_roles.extend(role)
# st.write(sorted(set(unique_roles)))

st.markdown(f'''
            Уникальных участников в таблице {len(df)}  
            ''')