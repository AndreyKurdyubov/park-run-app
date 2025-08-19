import pandas as pd
from sqlalchemy import create_engine, text
import streamlit as st
from streamlit import session_state as ss
from utils import menu, authentication
import datetime

st.set_page_config(layout='wide')

menu()
authenticator, name, authentication_status, username = authentication()
# if 'session_start' not in ss:
#     ss.session_start = 1
#     st.rerun()

st.header('База участников 5 вёрст в Петергофе')

engine = create_engine('sqlite:///mydatabase.db')


col1, col2 = st.columns(2)

with col1:
    datefrom = st.date_input(label="Отфильтровать от", format="YYYY-MM-DD",value=datetime.date.fromisoformat(("2022-06-11")))
   

with col2:
    sex = st.radio(
        "Пол",
        ["МЖ", "М", "Ж"],
        horizontal=True,
    )
    if sex == "МЖ":
        choice = ""
    else: 
        choice = sex

if datefrom:
    ##### tables #####
    # runners
    querie = f'''
    SELECT profile_link, name, max(age_group) as ag, count(run_date) as num_runs_period
    FROM runners
    WHERE run_date >= "{datefrom}" and profile_link LIKE "%userstats%"
    GROUP BY profile_link
    '''
    df_run = pd.read_sql(querie, con=engine) # all runs for run <= run_number

    # orgs
    querie = f'''
    SELECT profile_link, name, count(distinct run_date) as num_vols_period
    FROM organizers 
    WHERE run_date >= "{datefrom}" and profile_link LIKE "%userstats%"
    GROUP BY profile_link
    '''
    df_org = pd.read_sql(querie, con=engine) # all vols for run <= run_number

    # users
    querie = f'''
    SELECT profile_link, name, best_time,
        peterhof_finishes_count,
        peterhof_volunteers_count,
        sex
    FROM users us
    '''
    df_users = pd.read_sql(querie, con=engine)
    ##### tables ######    
    
    df_comb = df_run.merge(df_org, on=['profile_link', 'name'], how='outer'
                           ).merge(
                           df_users, on=['profile_link', 'name'], how='left')
    df_comb['sum_fin_vol'] = df_comb['num_runs_period'] + df_comb['num_vols_period']
    if choice:
        df_comb = df_comb[df_comb['sex'] != "Ж"] if choice == "М" else df_comb[df_comb['sex'] != "М"]

    df_comb = df_comb.sort_values('sum_fin_vol', ascending=False)
    df_comb['row_num'] = range(1, len(df_comb) + 1)
    

#     querie = f'''
#     WITH aProfs as (SELECT profile_link
#     FROM runners 
#     WHERE run_date >= "{datefrom}" and profile_link LIKE "%userstats%"
#     UNION ALL
#     SELECT profile_link
#     FROM organizers
#     WHERE run_date >= "{datefrom}" and profile_link LIKE "%userstats%"
#     ),
#     Profs as (SELECT distinct profile_link FROM aProfs),
#     Ages as (SELECT profile_link, max(age_group) as ag FROM runners GROUP By profile_link)
#     SELECT  
#         ROW_NUMBER () OVER (ORDER BY u.peterhof_finishes_count + u.peterhof_volunteers_count desc) RowNum, --u.peterhof_finishes_count + 
#         u.profile_link, u.sex, a.ag, u.name, u.best_time, 
#         u.peterhof_finishes_count + u.peterhof_volunteers_count as sum_fin_vol,
#         --CAST(u.finishes as int) as finishes, 
#         u.peterhof_finishes_count, 
#         --CAST(u.volunteers as int) as volunteers, 
#         u.peterhof_volunteers_count
#         --u.clubs_titles,
#     FROM Profs
#     LEFT JOIN users u on u.profile_link = Profs.profile_link
#     LEFT JOIN Ages a on u.profile_link = a.profile_link
#     WHERE sex LIKE "%{choice}" OR sex is Null
#     ORDER By 1
#     '''

# df = pd.read_sql(querie, con=engine)

st.markdown(f'''
            Начиная с {datefrom} Петергоф посетило {len(df_comb)} зарегистрированных участников {sex}
            ''')
st.write("""Пояснение к колонкам:<br>
            **Рекорд** - личный рекорд **во всех парках за все время на 5 верст**<br>
            **Сумма** - сумма финишей и волонтерств в **Петергофе** за период<br>
            **Финишей** - количество финишей в **Петергофе** за период<br>
            **Волонтерств** - количество волонтерств в **Петергофе** за период<br>
            """, unsafe_allow_html=True)

# CSS для изменения ширины таблицы
table_css = """
    <style>
    .data-editor-container {
        width: 800px;  /* Ширина всей таблицы */
        margin: 0 auto;  /* Центрирование */
    }
    </style>
"""

# Отображаем CSS через markdown
st.markdown(table_css, unsafe_allow_html=True)

# Контейнер для таблицы с классом для применения стилей
with st.container():
    st.data_editor(
        df_comb,
        column_order=['row_num', 'profile_link', 'name', 'sex', 'ag', 'best_time', 'sum_fin_vol', 'num_runs_period', 'num_vols_period', 'peterhof_finishes_count', 'peterhof_volunteers_count'],
        column_config={
            'row_num': st.column_config.Column(label="#", width=''), 
            'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width='100px'),
            'name': st.column_config.Column(label="Участник", width=''), 
            'sex': st.column_config.Column(label="Пол", width=''), 
            'ag': st.column_config.Column(label="Группа", width=''), 
            'best_time': st.column_config.Column(label="Рекорд", width='100px'),
            'num_runs_period': st.column_config.Column(label="Финишей за период", width=''), 
            'num_vols_period': st.column_config.Column(label="Волонтерств за период", width=''),
            'sum_fin_vol': st.column_config.Column(label="Сумма", width=''),
            # 'finishes': st.column_config.Column(label="# финишей", width='100px'),
            'peterhof_finishes_count': st.column_config.Column(label="Всего финишей в Петергофе", width='150px'),
            # 'volunteers': st.column_config.Column(label="# волонтерств", width='120px'),
            'peterhof_volunteers_count': st.column_config.Column(label="Всего волонтерств в Петергофе", width='150px'),
            # 'clubs_titles': st.column_config.Column(label="Клубы", width='large'),
        },
        hide_index=True,
        key="custom_table"
    )