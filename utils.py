import streamlit_authenticator as stauth
import streamlit as st
from streamlit import session_state as ss
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import time

def menu():
    st.sidebar.page_link("pages/home.py", label="Домашняя")
    st.sidebar.page_link("pages/main_table.py", label="Таблица участников")
    st.sidebar.page_link("pages/records_table.py", label="Клубы и рекорды")
    st.sidebar.page_link("pages/almost_club.py", label="Почти в клубе")
    st.sidebar.page_link("pages/last_results.py", label="Последние результаты")
    if ('username' in ss) and (ss.username == 'host'):
        st.sidebar.page_link("pages/update.py", label="Обновление базы")
    st.sidebar.divider()
    
def title(string):
    return string.title()

def dict_to_text(d):
    result = []
    for key, values in d.items():
        result.append(f"{key}:")
        result.append(", ".join(values))
    return "<br>".join(result)

def tags_table():
    # Таблица тегов

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets"
    ]
    # creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    service_account_info = dict(st.secrets["sheets"])
    creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
    client = gspread.authorize(creds)

    sheet_id = st.secrets["sheets"]["sheet_id"]
    workbook = client.open_by_key(sheet_id)

    cop = workbook.sheet1.get_all_values()
    df_tag = pd.DataFrame(cop[1:], columns=cop[0])
    return df_tag

def link_to_tag(vk_link, name_5verst, name_real):
    id = str(vk_link)[15:]
    name = name_real if isinstance(name_real, str) else name_5verst
    if len(id) > 0:
        tag = "@"  + id +  f" ({name.title()})"
        return tag
    else: 
        return f"{name.title()}"
    
def showFF(start_num, names, positions, show=False, photos=False):
    url = f"https://raw.githubusercontent.com/AndreyKurdyubov/FF/main/photos_{start_num}"
    if show:
        if photos:
            for nam, pos in zip(names, positions):
                try:
                    pos = int(pos)
                    st.write(f'{pos}. {nam}')
                    st.image(image=url + f"/{pos}.jpg")
                except Exception as e:
                    st.write(f'{nam} не бежал(а).')
        else:
            st.write("<br>".join(names), unsafe_allow_html=True)
        st.write(f"Всего: {len(names)}")

def add_control(start_num, list_name, names, positions, i):
    # Создаем контейнер и применяем CSS для горизонтального расположения

    button = st.button(f"{list_name}")
    checkbox = st.checkbox(f"фото", key=i)

    if f"checkbox_prev_state_{i}" not in ss:
        ss[f"checkbox_prev_state_{i}"] = False

    if f"button_prev_state_{i}" not in ss:
        ss[f"button_prev_state_{i}"] = False

    if checkbox:
        ss[f"checkbox_prev_state_{i}"] = checkbox

    if button:
        ss[f"button_prev_state_{i}"] = not ss[f"button_prev_state_{i}"]

    if ss[f"button_prev_state_{i}"]:
        show = ss[f"button_prev_state_{i}"]
        showFF(start_num, names, positions, show=show, photos=checkbox)

# authentication
def authentication(page='main'):
    usernames = [
        st.secrets['credentials']['user1']['username'], 
        st.secrets['credentials']['user2']['username']
        ]
    names = [
        st.secrets['credentials']['user1']['name'],
        st.secrets['credentials']['user2']['name']
        ]
    hashed_passwords = [
        st.secrets['credentials']['user1']['password'], 
        st.secrets['credentials']['user2']['password']
        ]

    credentials = {
        "usernames":{
            usernames[0]:{
                "name": names[0],
                "password": hashed_passwords[0]
                },
            usernames[1]:{
                "name": names[1],
                "password": hashed_passwords[1]
                }            
            }
        }
    cookie_name = st.secrets['cookie']['name']
    cookie_key = st.secrets['cookie']['key']
    expiry_days = st.secrets['cookie']['expiry_days']

    # login
    login_fields = {
        'Form name': '', 
        'Username': 'Логин', 
        'Password': 'Пароль', 
        'Login': 'Войти', 
        'Captcha': 'Captcha'
    }

    if page == 'login_page':
        login_location = 'main'
    else:
        login_location = 'unrendered'

    authenticator = stauth.Authenticate(credentials, cookie_name, cookie_key, expiry_days)
    # time.sleep(1)
    name, authentication_status, username = authenticator.login(location=login_location, key="Login", 
    fields=login_fields)
    ss.name = name
    ss.username = username

    if page == 'main':
        if authentication_status:
            ss.authentication_status = True
            st.sidebar.write(f"Вы вошли как {name}")
            authenticator.logout('Выйти', 'sidebar', key='unique_key')
        else:
            st.sidebar.write(f"Вы не вошли")
            st.sidebar.page_link("pages/login_page.py", label="**Войти**", icon="➡️")

    elif page == 'login_page':
        if authentication_status:
            ss.authentication_status = True
            # time.sleep(0)
            # st.switch_page('pages/home.py')
        elif authentication_status is False:
            ss.authentication_status = False
            st.error('Имя пользователя или пароль введены неверно')
        elif authentication_status is None:
            ss.authentication_status = None
            st.warning('Введите имя пользователя и пароль')

    return authenticator, name, authentication_status, username