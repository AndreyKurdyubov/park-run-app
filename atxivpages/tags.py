import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import streamlit as st
import json
from menu import menu, tags_table, link_to_tag
from sqlalchemy import create_engine

st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

menu()

# Таблица тегов

df_tag = tags_table()

# scopes = [
#     "https://www.googleapis.com/auth/spreadsheets"
# ]
# # creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
# service_account_info = dict(st.secrets["sheets"])
# creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
# client = gspread.authorize(creds)

# sheet_id = st.secrets["sheets"]["sheet_id"]
# workbook = client.open_by_key(sheet_id)

# cop = workbook.sheet1.get_all_values()
# df_tag = pd.DataFrame(cop[1:], columns=cop[0])
# grouped = df.groupby(['profile_link']).count()

# st.write(grouped[grouped['name'] > 1])

# Таблица участников
engine = create_engine('sqlite:///mydatabase.db')

querie = f'''
    WITH aProfs as (SELECT profile_link
    FROM runners 
    WHERE profile_link LIKE "%userstats%"
    UNION ALL
    SELECT profile_link
    FROM organizers
    WHERE profile_link LIKE "%userstats%"
    ),
    Profs as (SELECT distinct profile_link FROM aProfs),
    Ages as (SELECT profile_link, max(age_group) as ag FROM runners GROUP By profile_link)
    SELECT  
        ROW_NUMBER () OVER (ORDER BY u.peterhof_finishes_count + u.peterhof_volunteers_count desc) RowNum, --u.peterhof_finishes_count + 
        u.profile_link, u.sex, a.ag, u.name, u.best_time, 
        u.peterhof_finishes_count + u.peterhof_volunteers_count as sum_fin_vol,
        u.peterhof_finishes_count,  
        u.peterhof_volunteers_count
    FROM Profs
    LEFT JOIN users u on u.profile_link = Profs.profile_link
    LEFT JOIN Ages a on u.profile_link = a.profile_link
    ORDER By 1
    '''

df = pd.read_sql(querie, con=engine)

df_comb = df.merge(df_tag[['profile_link', 'VK link']], on='profile_link', how='left')

# st.dataframe(df_comb)

df_comb['check'] = df_comb.apply(lambda row: link_to_tag(row['VK link'], row['name']), axis=1)

st.dataframe(df_comb)
