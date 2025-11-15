import os
import streamlit as st
from streamlit import session_state as ss
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, text
from datetime import datetime
import pandas as pd  
from zoneinfo import ZoneInfo
import glob
import re
from utils import find_db_files, convert_date_string
from utils import menu, authentication
import random
import time

#####################################################################################################################################################
# Настройка страницы
#####################################################################################################################################################

# Конфигурация страницы
st.set_page_config(page_title='Duck🌳Run', page_icon=':running:')

menu()
authenticator, name, authentication_status, username = authentication()
# if 'session_start' not in ss:
#     ss.session_start = 1
#     st.rerun()

db_name = find_db_files()

# Путь к изображению
image_path = 'logo.jpg'
num_runs = 3  # количество загружаемых протоколов

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
time_out = 20
run_data = ss.get('run_data')
now_t = ss.get('now_t')
all_participant_data = ss.get('all_participant_data')
all_volunteer_data = ss.get('all_volunteer_data')

# Заголовок
# st.header('База участников 5Верст Петергоф Александрийский')

st.divider()

col1, col2 = st.columns(2)

with col1:
    if username in ['host', 'org']:
        if db_name:
            db_name = 'sqlite:///' + db_name[-1]
            st.success(f'Найдена БД от {convert_date_string(db_name[10:-3])}')
            engine = create_engine(db_name)
            
            st.write('*Список страниц:*')
            # st.page_link("pages_dir\main_table.py", label="База участников")
            st.markdown('''
            - [Клубы и рекорды](records_table)
            - [Последние результаты](last_results)        
            ''')
        else:
            st.write('База отсутствует')

    # if username in ['host']:
    #     st.markdown('''
    #     - [База участников](main_table)
    #     - [Клубы и рекорды](records_table)
    #     - [Почти в клубе](almost_club)
    #     - [Какие люди!](hellothere)
    #     - [Последние результаты](last_results)
    #     - [Обновление](update)           
    #     ''')
    # else:
    #     st.markdown('''
    #     - [База участников](main_table)
    #     - [Клубы и рекорды](records_table)
    #     - [Почти в клубе](almost_club)
    #     - [Какие люди!](hellothere)
    #     - [Последние результаты](last_results)
    #     ''')

#####################################################################################################################################################
# Парсинг
#####################################################################################################################################################

main_url = 'https://5verst.ru/results/latest/'
tarjet_park = 'Петергоф'  # Петергоф Александрийский
target_runs = [tarjet_park]

def get_last_date_from_site():
    url = 'https://5verst.ru/petergofaleksandriysky/results/all/'
    location_name = "petergof"
    
    try:
        # Добавляем заголовки для имитации браузера
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=time_out)
        response.raise_for_status()  # Проверяем статус ответа
        time.sleep(random.uniform(1, 2.1))
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Более надежный поиск таблицы
        tables = soup.find_all('table')
        if not tables:
            raise ValueError("Таблицы не найдены на странице")

        # Получаем ячейки из второй строки
        run_data = []

        for row in tables[0].find_all('tr')[1:]:
            run_cells = row.find_all('td')
            number = run_cells[0].get_text(strip=True)
            date_cell = run_cells[1].get_text(strip=True)
            last_date_site = datetime.strptime(date_cell, '%d.%m.%Y').date()

            link = run_cells[1].find('a')['href'] if run_cells[1].find('a') else None
            finishers = int(run_cells[2].get_text(strip=True))
            volunteers = int(run_cells[3].get_text(strip=True))
            avg_time = run_cells[4].get_text(strip=True)
            best_female_time = run_cells[5].get_text(strip=True)
            best_male_time = run_cells[6].get_text(strip=True)
                
            if number:
                run_data.append([location_name, number, last_date_site, link, finishers, volunteers, avg_time, best_female_time, best_male_time])

        # Преобразование last_date из формата DD.MM.YYYY в объект datetime
        moscow_tz = ZoneInfo('Europe/Moscow')
        now_t = datetime.now(moscow_tz).replace(microsecond=0, tzinfo=None)

        return run_data, now_t
        
    except requests.RequestException as e:
        st.write(f"Ошибка при запросе к сайту: {e}")
        return None, None
    except ValueError as e:
        st.write(f"Ошибка при обработке данных: {e}")
        return None, None
    except Exception as e:
        st.write(f"Неожиданная ошибка: {e}")
        return None, None


def parse_participant_and_volunteer_tables(run_protocol_link, run_data):
    '''get tables from protocol'''

    try:
        # Добавляем заголовки для имитации браузера
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(run_protocol_link, headers=headers, timeout=time_out)
        response.raise_for_status()  # Проверяем статус ответа
        
        soup = BeautifulSoup(response.text, 'html.parser')
        st.write(f'Загружаю протокол #{run_data[1]}')
        time.sleep(random.uniform(3, 4.1))
        # st.write('wake up')
        
   
    except requests.RequestException as e:
        print(f"Ошибка при запросе к сайту: {e}")
        return None, None
    
    all_tables = soup.find_all('table')

    # Забег: location_name, number, date_cell, link, finishers, volunteers, avg_time, best_female_time, best_male_time
    location_name, number, date_cell, link, finishers, volunteer_count, avg_time, best_female_time, best_male_time = run_data

    participants_data = []
    volunteers_data = []

    # Парсим участников
    participant_table = all_tables[0]
    for row in participant_table.find_all('tr')[1:]:
        cells = row.find_all('td')
        if len(cells) >= 4:
            position = cells[0].get_text(strip=True)
            name_tag = cells[1].find('a')
            name = name_tag.get_text(strip=True) if name_tag else '—'
            name_lc = name.lower()
            profile_link = name_tag['href'] if name_tag else '—'
            participant_id = profile_link.split('/')[-1] if profile_link != '—' else '—'
            stats_div = cells[1].find('div', class_='user-stat')
            finishes = '—'
            volunteers = '—'
            if stats_div:
                stats_spans = stats_div.find_all('span')
                finishes = stats_spans[0].get_text(strip=True).split(' ')[0] if len(stats_spans) > 0 else '—'
                volunteers = stats_spans[1].get_text(strip=True).split(' ')[0] if len(stats_spans) > 1 else '—'
            club_tags = cells[1].find_all('span', class_='club-icon')
            clubs = ', '.join([club['title'] for club in club_tags]) if club_tags else '—'
            age_group = cells[2].get_text(strip=True).split(' ')[0] if cells[2] else '—'
            age_grade_tag = cells[2].find('div', class_='age_grade')
            age_grade = age_grade_tag.get_text(strip=True) if age_grade_tag else '—'
            time_fin = cells[3].get_text(strip=True) if cells[3] else '—'
            achievements = []
            achievements_div = cells[3].find('div', class_='table-achievments')
            if achievements_div:
                achievement_icons = achievements_div.find_all('span', class_='results_icon')
                for icon in achievement_icons:
                    achievements.append(icon['title'])
            participants_data.append([location_name, number, date_cell, link, finishers, volunteer_count, avg_time, best_female_time, best_male_time,
                                      position, name, name_lc, profile_link, participant_id, clubs, finishes, volunteers, age_group, age_grade, time_fin, ', '.join(achievements)])
            
    # Парсим волонтёров
    volunteer_table = all_tables[1]
    for row in volunteer_table.find_all('tr')[1:]:
        columns = row.find_all('td')
        if len(columns) > 1:
            name_tag = columns[0].find('a')
            name = name_tag.get_text(strip=True) if name_tag else '—'
            name_lc = name.lower()
            profile_link = name_tag['href'] if name_tag else '—'
            participant_id = profile_link.split('/')[-1] if profile_link != '—' else '—'
            stats_div = columns[0].find('div', class_='user-stat')
            finishes = '—'
            volunteers = '—'
            if stats_div:
                stats_spans = stats_div.find_all('span')
                finishes = stats_spans[0].get_text(strip=True).split(' ')[0] if len(stats_spans) > 0 else '—'
                volunteers = stats_spans[1].get_text(strip=True).split(' ')[0] if len(stats_spans) > 1 else '—'
            club_tags = columns[0].find_all('span', class_='club-icon')
            clubs = ', '.join([club['title'] for club in club_tags]) if club_tags else '—'
            volunteer_role_info = columns[1].find('div', class_='volunteer__role')
            if volunteer_role_info:
                first_volunteer_tag = volunteer_role_info.find('span', class_='results_icon')
                first_volunteer_info = first_volunteer_tag['title'] if first_volunteer_tag else '—'
                role_tag = volunteer_role_info.find_all('span')
                volunteer_role = role_tag[-1].get_text(strip=True) if role_tag else '—'
            else:
                first_volunteer_info = '—'
                volunteer_role = '—'
            volunteers_data.append([location_name, number, date_cell, link, finishers, volunteer_count, avg_time, best_female_time, best_male_time,
                                    name, name_lc, profile_link, participant_id, finishes, volunteers, clubs, volunteer_role, first_volunteer_info])
    
    return participants_data, volunteers_data

def get_full_run_data(run_data):
    '''Get runners and volonteers from several protocols'''
    all_participant_data = []
    all_volunteer_data = []

    for run_dat in run_data[:num_runs]:
        participants, volunteers = parse_participant_and_volunteer_tables(run_dat[3], run_dat)
    
        all_participant_data.extend(participants)
        all_volunteer_data.extend(volunteers)

    return all_participant_data, all_volunteer_data

def save_to_database(df_runners, df_orgs, db_url):
    # Создаем подключение к базе данных
    print(db_url)
    engine = create_engine(db_url)
    # Сохраняем данные бегунов в таблицу 'runners'
    df_runners.to_sql('runners', con=engine, if_exists='replace', index=False)
    # Сохраняем данные организаторов в таблицу 'organizers'
    df_orgs.to_sql('organizers', con=engine, if_exists='replace', index=False)


def update_data(all_participant_data, all_volunteer_data, db_name):
    # Создаём DataFrame для бегунов
    df_runners = pd.DataFrame(all_participant_data, columns=[
        'run', 'run_number', 'run_date', 'run_link', 'finisher', 'volunteer', 'avg_time',
        'best_female_time', 'best_male_time', 'position', 'name', 'name_lc', 'profile_link',
        'participant_id', 'clubs', 'finishes', 'volunteers', 'age_group', 'age_grade',
        'time', 'achievements'
    ])
    df_runners['run_date'] = pd.to_datetime(df_runners['run_date'], dayfirst=True)

    # Создаём DataFrame для волонтёров
    df_orgs = pd.DataFrame(all_volunteer_data, columns=[
        'run', 'run_number', 'run_date', 'run_link', 'finisher', 'volunteer', 'avg_time',
        'best_female_time', 'best_male_time', 'name', 'name_lc', 'profile_link', 'participant_id',
        'finishes', 'volunteers', 'clubs', 'volunteer_role', 'first_volunteer_info'
    ])
    df_orgs['run_date'] = pd.to_datetime(df_orgs['run_date'], dayfirst=True)

    save_to_database(df_runners, df_orgs, db_name)


def get_last_date_from_db(db_url):
    # Извлекаем путь к файлу базы данных
    db_path = db_url.replace('sqlite:///', '')
    
    # Проверяем, существует ли файл базы данных
    if not os.path.exists(db_path):
        return None, None  # Если базы данных нет, возвращаем None
    
    # Извлекаем дату и время из названия файла
    filename = os.path.basename(db_path)
    time_db = convert_date_string(filename[:-3])
    
    try:
        # Подключение к базе данных, если файл существует
        # st.write(db_url)
        engine = create_engine(db_url)
        with engine.connect() as connection:
            st.write('connected')
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
        return None, time_db
    
    return last_date_db, time_db

# def extract_datetime_from_filename(filename):
#     """
#     Извлекает дату и время из названия файла в формате YYYY_MM_DD_HH_MM_SS.db
#     """
#     # Регулярное выражение для поиска шаблона даты и времени
#     pattern = r'(\d{4})_(\d{2})_(\d{2})_(\d{2})_(\d{2})_(\d{2})\.db$'
#     match = re.search(pattern, filename)
    
#     if match:
#         year, month, day, hour, minute, second = map(int, match.groups())
#         try:
#             time_db = datetime(year, month, day, hour, minute, second)
#             st.write(time_db)
#             return time_db
#         except ValueError:
#             st.write('Incorrect data')
#             # Если дата некорректна (например, 2023_02_30_25_61_61.db)
#             return None
    
#     return None  # Если шаблон не найден


def keep_only_latest_db_by_mtime():
    """
    Оставляет самую свежую БД по дате изменения файла
    """
    db_files = glob.glob(os.path.join('*.db'))
    
    if not db_files:
        print("Базы данных не найдены")
        return None
    
    if len(db_files) == 1:
        print(f"Только одна БД: {os.path.basename(db_files[0])}")
        return db_files[0]
    
    # Находим самую свежую по дате изменения
    latest_db = max(db_files, key=os.path.getmtime)
    
    print(f"Сохраняем: {os.path.basename(latest_db)}")
    print(f"Удаляем {len(db_files) - 1} файлов:")
    
    for db_file in db_files:
        if db_file != latest_db:
            try:
                os.remove(db_file)
                print(f"  ✓ Удалено: {os.path.basename(db_file)}")
            except Exception as e:
                print(f"  ✗ Ошибка при удалении {db_file}: {e}")
    
    return latest_db

if username in ['host']:
    with col2:
        st.write('*Управление БД:*')
        if st.button('Получить список протоколов с сайта'):
            try:
                run_data, now_t = get_last_date_from_site()
                if run_data:
                    ss['run_data'] = run_data
                    ss['now_t'] = now_t
                    st.subheader(f'Протоколы с оф. сайта на {now_t}')  
                    for run_dat in run_data[:num_runs]:
                        location_name, number, date_cell, link, finishers, volunteers, avg_time, best_female_time, best_male_time = run_dat
                        st.markdown(f'''[#{number} {date_cell}]({link}), {finishers} фин. {volunteers} вол.''')
                    st.success('Списки получены')
            except Exception as e:
                st.write(f"Неожиданная ошибка: {e}")
        # last_date_db = get_last_date_from_db()
            
        # with col2:
        if st.button('Загрузить данные'):
            if run_data:
                # st.subheader(f'Актуальность данных на {now_t}')  
                for run_dat in run_data[:num_runs]:
                    location_name, number, date_cell, link, finishers, volunteers, avg_time, best_female_time, best_male_time = run_dat
                    # st.markdown(f'''[#{number} {date_cell}]({link}), {finishers} фин. {volunteers} вол.''')
                
                try:
                    all_participant_data, all_volunteer_data = get_full_run_data(run_data)
                    ss['all_participant_data'] = all_participant_data
                    ss['all_volunteer_data'] = all_volunteer_data
                    st.success('Протоколы обработаны')
                except Exception as e:
                    st.write(f"Неожиданная ошибка: {e}")

                # st.markdown(f'''{all_participant_data[0]} {all_volunteer_data[0]}''')
                # st.markdown(f'''{len(all_participant_data)} {len(all_volunteer_data)} {len(run_data)}''')
            else:
                st.write('Протоколы с сайта не загружены')

        if st.button('Сохранить данные в базу'):
            if all_participant_data and all_volunteer_data and now_t:
                print(now_t)
                db_name = 'sqlite:///' + now_t.strftime("%Y_%m_%d_%H_%M_%S.db")
                print(db_name)
                update_data(all_participant_data, all_volunteer_data, db_name)
                keep_only_latest_db_by_mtime()
                st.success('Сохранено в базу')
            else: 
                st.write('Данные не получены')

        if st.button('Проверка базы'):
            # Использование:
            db_name = find_db_files()
            if db_name:
                db_name = 'sqlite:///' + db_name[-1]
                engine = create_engine(db_name)
                st.success(f'Найдена БД от {convert_date_string(db_name[10:-3])}')
            else:
                st.write('База отсутствует')
            # last_date_db, time_db = get_last_date_from_db(db_name)