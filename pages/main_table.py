import pandas as pd
from sqlalchemy import create_engine, text
import streamlit as st
from utils import menu, authentication
import datetime

st.set_page_config(layout='wide')

menu()
authenticator, name, authentication_status, username = authentication()

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
    querie = f'''
    WITH aProfs as (SELECT profile_link
    FROM runners 
    WHERE run_date >= "{datefrom}" and profile_link LIKE "%userstats%"
    UNION ALL
    SELECT profile_link
    FROM organizers
    WHERE run_date >= "{datefrom}" and profile_link LIKE "%userstats%"
    ),
    Profs as (SELECT distinct profile_link FROM aProfs),
    Ages as (SELECT profile_link, max(age_group) as ag FROM runners GROUP By profile_link)
    SELECT  
        ROW_NUMBER () OVER (ORDER BY u.peterhof_finishes_count + u.peterhof_volunteers_count desc) RowNum, --u.peterhof_finishes_count + 
        u.profile_link, u.sex, a.ag, u.name, u.best_time, 
        u.peterhof_finishes_count + u.peterhof_volunteers_count as sum_fin_vol,
        --CAST(u.finishes as int) as finishes, 
        u.peterhof_finishes_count, 
        --CAST(u.volunteers as int) as volunteers, 
        u.peterhof_volunteers_count
        --u.clubs_titles,
    FROM Profs
    LEFT JOIN users u on u.profile_link = Profs.profile_link
    LEFT JOIN Ages a on u.profile_link = a.profile_link
    WHERE sex LIKE "%{choice}" OR sex is Null
    ORDER By 1
    '''

df = pd.read_sql(querie, con=engine)

st.markdown(f'''
            Начиная с {datefrom} Петергоф посетило {len(df)} зарегистрированных участников {sex}
            ''')

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
        df,
        column_config={
            'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width='100px'),
            'name': st.column_config.Column(label="Участник", width=''), 
            'sex': st.column_config.Column(label="Пол", width=''), 
            'best_time': st.column_config.Column(label="Лучшее время", width='100px'),
            'finishes': st.column_config.Column(label="# финишей", width='100px'),
            'peterhof_finishes_count': st.column_config.Column(label="# финишей в Петергофе", width='150px'),
            'volunteers': st.column_config.Column(label="# волонтерств", width='120px'),
            'peterhof_volunteers_count': st.column_config.Column(label="# волонтерств в Петергофе", width='150px'),
            'clubs_titles': st.column_config.Column(label="Клубы", width='large'),
        },
        hide_index=True,
        key="custom_table"
    )
