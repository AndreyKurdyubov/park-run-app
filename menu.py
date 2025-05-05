import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

def menu():
    st.sidebar.page_link("pages/home.py", label="Домашняя")
    st.sidebar.page_link("pages/main_table.py", label="Таблица участников")
    st.sidebar.page_link("pages/records_table.py", label="Клубы и рекорды")
    # st.sidebar.page_link("pages/FF.py", label="Фотофиниш")
    st.sidebar.page_link("pages/almost_club.py", label="Почти в клубе")
    st.sidebar.page_link("pages/last_results.py", label="Последние результаты")
    
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

    if f"checkbox_prev_state_{i}" not in st.session_state:
        st.session_state[f"checkbox_prev_state_{i}"] = False

    if f"button_prev_state_{i}" not in st.session_state:
        st.session_state[f"button_prev_state_{i}"] = False

    if checkbox:
        st.session_state[f"checkbox_prev_state_{i}"] = checkbox

    if button:
        st.session_state[f"button_prev_state_{i}"] = not st.session_state[f"button_prev_state_{i}"]

    if st.session_state[f"button_prev_state_{i}"]:
        show = st.session_state[f"button_prev_state_{i}"]
        showFF(start_num, names, positions, show=show, photos=checkbox)