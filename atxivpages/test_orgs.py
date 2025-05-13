import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import datetime

st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

engine = create_engine('sqlite:///mydatabase.db')

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

SELECT u.profile_link, u.name, u.finishes, u.volunteers, u.peterhof_finishes_count, u.peterhof_volunteers_count,
substr(last_time, 1, 10) as last_time
FROM USERS u
LEFT JOIN aProfs a
ON u.profile_link = a.profile_link
WHERE (23 <= u.finishes AND u.finishes <= 25) OR 
(48 <= u.finishes AND u.finishes <= 50) OR 
(98 <= u.finishes AND u.finishes <= 100) OR 


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
