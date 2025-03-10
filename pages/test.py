import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import datetime

st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

st.title('Тестирование')

engine = create_engine('sqlite:///mydatabase.db')

querie = '''
SELECT *
FROM organizers
GROUP BY sex, volunteers_role
'''
df = pd.read_sql(querie, con=engine)
st.data_editor(
    df,
    # column_config={
    #     'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
    #     'name_lc': st.column_config.Column(label="Участник", width='medium'), 
    #     'time': st.column_config.Column(label="Время", width=''), 
    #     'position': st.column_config.Column(label="Позиция", width=''), 
    #     'finishes': st.column_config.Column(label="# финишей", width='medium'),
    #     'volunteers': st.column_config.Column(label="# волонтерств", width='medium'),
    #     'achievements': st.column_config.Column(label="Достижения", width='large'),
    # },
    # hide_index=True
    )


# array_of_dates = df['run_date'].unique()
# dates1 = [obj[:10] for obj in array_of_dates]
# dates2 = dates1.copy()
# unique_roles = []
# for role in roles:
#     unique_roles.extend(role)

# st.divider()

# col1, col2 = st.columns(2)

# with col1:
#     datefrom = st.date_input(label="Отфильтровать от", format="YYYY-MM-DD",value=datetime.date.fromisoformat(("2022-06-11")))
   

# with col2:
#     sex = st.radio(
#         "Пол",
#         ["МЖ", "М", "Ж"],
#         horizontal=True,
#     )
#     if sex == "МЖ":
#         choice = ""
#     else: 
#         choice = sex


# if datefrom:
#     querie = f'''
#     WITH aProfs as (SELECT profile_link
#     FROM runners 
#     WHERE run_date >= "{datefrom}" and profile_link LIKE "%userstats%"
#     UNION ALL
#     SELECT profile_link
#     FROM organizers
#     WHERE run_date >= "{datefrom}" and profile_link LIKE "%userstats%"
#     ),
#     Profs as (SELECT distinct profile_link FROM aProfs)
#     SELECT u.profile_link, u.sex, u.name, u.best_time, CAST(u.finishes as int) as finishes, 
#         u.peterhof_finishes_count, CAST(u.volunteers as int) as volunteers, u.peterhof_volunteers_count, u.clubs_titles
#     FROM Profs
#     LEFT JOIN users u on u.profile_link = Profs.profile_link
#     WHERE sex LIKE "%{choice}" OR sex is Null
#     '''

#     df = pd.read_sql(querie, con=engine)

#     st.data_editor(
#     df,
#     column_config={
#         'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
#         'name_lc': st.column_config.Column(label="Участник", width='medium'), 
#         'time': st.column_config.Column(label="Время", width=''), 
#         'position': st.column_config.Column(label="Позиция", width=''), 
#         'finishes': st.column_config.Column(label="# финишей", width='medium'),
#         'volunteers': st.column_config.Column(label="# волонтерств", width='medium'),
#         'achievements': st.column_config.Column(label="Достижения", width='large'),
#     },
#     hide_index=True
#     )

#     st.write(f"Начиная с {datefrom} Петергоф посетило {len(df)} участников {sex}")

# querie = '''
# WITH au as (
# SELECT profile_link, name_lc, run_date, position, Null as volunteer_role
# FROM runners
# WHERE profile_link LIKE "%userstats%"
# UNION ALL
# SELECT profile_link, name_lc, run_date, Null as position, volunteer_role
# FROM organizers 
# WHERE profile_link LIKE "%userstats%")
# SELECT *, max(run_date) as last_date, count(distinct run_date) as num_subbot
# --SELECT count(distinct run_date)
# FROM au
# GROUP BY profile_link 
# HAVING num_subbot = 2 AND last_date = (SELECT max(run_date) FROM au)
# '''

# # querie = '''
# # WITH allusers as (
# # SELECT r.profile_link
# # FROM runners r LEFT JOIN organizers o on r.profile_link = o.profile_link 
# # UNION ALL
# # SELECT o.profile_link
# # FROM organizers o LEFT JOIN runners r on r.profile_link = o.profile_link 
# # WHERE r.profile_link IS NULL)
# # SELECT count(distict profile_liks)
# # FROM allusers
# # --WHERE run_date = (SELECT max(run_date) FROM USERS)
# # '''
# df = pd.read_sql(querie, con=engine)

# Отображаем таблицу 
