import os
import streamlit as st
from streamlit import session_state as ss
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, text
from datetime import datetime
import pandas as pd  
from utils import menu, authentication

#####################################################################################################################################################
# Настройка страницы
#####################################################################################################################################################

# Конфигурация страницы
st.set_page_config(page_title='Duck🌳Run', page_icon=':running:')

menu()
authenticator, name, authentication_status, username = authentication()

# Путь к изображению
image_path = 'logo.jpg'

# Вставка изображения
st.image(image_path, caption='')

# Скрытие футера и меню
hide_streamlit_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Заголовок
# st.header('База участников 5Верст Петергоф Александрийский')

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader('Список страниц:')
    # st.page_link("pages_dir\main_table.py", label="База участников")
    # st.page_link("pages_dir\records_table.py", label="Клубы и рекорды")
    st.markdown('''
    - [База участников](main_table)
    - [Клубы и рекорды](records_table)
    - [Почти в клубе](almost_club)
    - [Последние результаты](last_results)
    ''')

#####################################################################################################################################################
# Парсинг
#####################################################################################################################################################

main_url = 'https://5verst.ru/results/latest/'
tarjet_park = 'Петергоф'  # Петергоф Александрийский
target_runs = [tarjet_park]

# Проверка актуальности данных
#####################################################################################################################################################

# Функция для получения последней даты из сайта
def get_last_date_from_site():
    url = 'https://5verst.ru/petergofaleksandriysky/results/all/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    cell_date = soup.find_all('table')[0].find_all('tr')[1].find_all('td')[1]
    last_date = cell_date.text.strip()
    link = cell_date.find('a')['href']
    # print(link)

    # Преобразование last_date из формата DD.MM.YYYY в объект datetime
    last_date_site = datetime.strptime(last_date, '%d.%m.%Y').date()
    return last_date_site, link

# Функция для получения последней даты из БД
def get_last_date_from_db(db_url='sqlite:///mydatabase.db'):
    # Проверяем, существует ли файл базы данных
    db_path = db_url.replace('sqlite:///', '')  # Извлекаем путь к файлу базы данных
    if not os.path.exists(db_path):
        return None  # Если базы данных нет, возвращаем None
    try:
        # Подключение к базе данных, если файл существует
        engine = create_engine(db_url)
        with engine.connect() as connection:
            query = text("SELECT MAX(run_date) FROM runners;")  # Заменить run_date на реальное имя колонки с датой
            result = connection.execute(query)
            last_date_db = result.scalar()

            # Проверяем, если last_date_db не None, то преобразуем строку в дату
            if last_date_db:
                last_date_db = datetime.strptime(last_date_db, '%Y-%m-%d %H:%M:%S.%f').date()
            else:
                last_date_db = None
    except Exception as e:
        st.write(f"Произошла ошибка: {e}")
        return None
    return last_date_db


last_date_site, last_results_link = get_last_date_from_site()
last_date_db = get_last_date_from_db()
    
with col2:
    st.subheader('Актуальность данных:')  
    # Проверяем, если last_date_db не пустая
    if last_date_db is None:
        st.write('Данных в базе нет!')
    else:
        # Сравнение дат
        if last_date_db != last_date_site:
            st.write(f'Данные устарели. Дата в базе: {last_date_db}, дата на сайте: [{last_date_site}]({last_results_link}).')
        else:
            st.markdown(f'''Данные актуальны 👍  
                        Последняя дата в базе данных: {last_date_db}  
                        Последняя дата на сайте: [{last_date_site}]({last_results_link})
                        ''')

#####################################################################################################################################################
# Поиск по имени
#####################################################################################################################################################
def go_search_by_role(option, engine):
    sql_query = text(f'''SELECT name, 
                                COUNT(*) as number, 
                                volunteer_role, 
                                MAX(run_date) as last_date_of_role,
                                profile_link
                        FROM organizers
                        WHERE volunteer_role LIKE "%{option}%" AND run_number != ''
                        GROUP BY profile_link;
                     ''')
    try:
        with engine.connect() as connection:
            result = connection.execute(sql_query).fetchall()

        if result:
            df_results = pd.DataFrame(result)
            df_results['last_date_of_role'] = pd.to_datetime(df_results['last_date_of_role']).dt.date

            with st.container():
                st.data_editor(
                    df_results,
                    column_config={
                        'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width='100px'),
                        'name': st.column_config.Column(label="Имя", width='120px'), 
                        # 'best_time': st.column_config.Column(label="Лучшее время", width='100px'),
                        # 'finishes': st.column_config.Column(label="# финишей", width='100px'),
                        # 'peterhof_finishes_count': st.column_config.Column(label="# финишей в Петергофе", width='150px'),
                        'volunteer_role': st.column_config.Column(label="Роль", width='medium'),
                        'number': st.column_config.Column(label="#", width='small'),
                        'last_date_of_role': st.column_config.Column(label="Последняя дата", width='medium'),
                        # 'peterhof_volunteers_count': st.column_config.Column(label="# волонтерств в Петергофе", width='150px'),
                        # 'clubs_titles': st.column_config.Column(label="Клубы", width='large'),
                    },
                    hide_index=True,
                    key="roles"
                )
        else:
            st.write("Нет результатов по вашему запросу.")

    except Exception as e:
        st.write(f"Ошибка {e}")


def go_search_by_name(search_query, engine):
    # Очистка ввода
    words = ' '.join(search_query.strip().split()).lower()
    if not words: 
        return

    # st.write(f'Поисковые слова: {words}')
    # Формируем условия поиска
    conditions = " OR ".join([f"name_lc LIKE :word{i}" for i in range(len(words.lower().split()))])
    sql_query = text(f'''SELECT profile_link, 
                                name, 
                                best_time, 
                                finishes, 
                                peterhof_finishes_count, 
                                volunteers, 
                                peterhof_volunteers_count, 
                                clubs_titles 
                    FROM users 
                    WHERE {conditions}''')
    params = {f"word{i}": f"%{word}%" for i, word in enumerate(words.split())}

    # st.write(f'SQL запрос: {sql_query}')
    # st.write(f'Параметры: {params}')

    try:
        with engine.connect() as connection:
            result = connection.execute(sql_query, params).fetchall()

        if result:
            # Преобразуем результат в DataFrame
            df_results = pd.DataFrame(result)
            with st.container():
                st.data_editor(
                    df_results,
                    column_config={
                        'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width='100px'),
                        'name': st.column_config.Column(label="Имя", width='120px'), 
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
        else:
            st.write("Нет результатов по вашему запросу.")

    except Exception as e:
        st.write(f"Произошла ошибка: {e}")

def show_search(db_url):
    # Подключение к базе данных
    # db_url = 'sqlite:///mydatabase.db'
    engine = create_engine(db_url)
    try:
        if username in ['host', 'org']:
            querie = '''
            SELECT volunteer_role
            FROM organizers
            '''
            df = pd.read_sql(querie, con=engine)
            array_of_roles = df['volunteer_role'].unique()
            roles = [role.split(', ') for role in array_of_roles]
            unique_roles = []
            for role in roles:
                unique_roles.extend(role)
            
            st.divider()

            st.subheader('Поиск по волонтерской роли:')

            option = st.selectbox(
            "Поиск по волонтерской роли",
            options=sorted(set(unique_roles)),
            index=None,
            placeholder="Выберите роль",
            label_visibility='collapsed'
            )

            if option:
                go_search_by_role(option, engine)

        st.divider()

        st.subheader('Поиск участника по имени:')

        # Поле для ввода поискового запроса
        search_query = st.text_input('Поиск по имени', 
                                    placeholder="Введите имя или фамилию", 
                                    label_visibility="collapsed")

        if search_query:
            go_search_by_name(search_query, engine)
    except Exception as e:
        # st.write(f"Произошла ошибка: {e}")
        pass

db_url='sqlite:///mydatabase.db'
db_path = db_url.replace('sqlite:///', '')  # Извлекаем путь к файлу базы данных

if os.path.exists(db_path):
    show_search(db_url)