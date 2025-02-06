import pandas as pd
from sqlalchemy import create_engine
import streamlit as st

st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

st.title('Данные по пробегам и организаторам')

engine = create_engine('sqlite:///mydatabase.db')
querie = '''
SELECT count(distinct profile_link)
FROM organizers
'''
df = pd.read_sql(querie, con=engine)

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

array_of_roles = df['volunteer_role'].unique()
roles = [role.split(', ') for role in array_of_roles]
unique_roles = []
for role in roles:
    unique_roles.extend(role)
st.write(sorted(set(unique_roles)))