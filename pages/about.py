import streamlit as st

st.set_page_config(page_title='PARK🌳RUN',
                   page_icon=':running:')

hide_streamlit_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.title('Домашняя страница')

# st.write("[Основная таблица](about.py)")
st.markdown(
f'''
Тут возможно будет какое-то описание функционала приложения.
Список страниц:
- [Основная таблица](main_table)
- Таблица рекордов
- Страница с таблицей бегунов
- Страница с таблицей организаторов
- Парсинг тут
- Кастомный SQL
'''
)