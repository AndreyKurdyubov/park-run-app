import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

def menu():
    st.sidebar.page_link("pages/about.py", label="Домашняя")
    st.sidebar.page_link("pages/main_table.py", label="Таблица участников")
    st.sidebar.page_link("pages/records_table.py", label="Клубы и рекорды")
    # st.sidebar.page_link("pages/FF.py", label="Фотофиниш")
    st.sidebar.page_link("pages/almost_club.py", label="Почти в клубе")

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

def link_to_tag(vk_link, name):
    id = str(vk_link)[15:]
    if len(id) > 0:
        tag = "@"  + id +  f" ({name.title()})"
        return tag
    else: 
        return f"{name.title()}"