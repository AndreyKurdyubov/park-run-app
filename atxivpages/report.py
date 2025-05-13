import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
from collections import OrderedDict as odict
from menu import menu, tags_table, link_to_tag, dict_to_text

st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

st.title('Волонтеры для отчета')

button = st.button("Отчет")

if button:
    engine = create_engine('sqlite:///mydatabase.db')
    querie = '''
    SELECT * 
    FROM organizers
    WHERE run_number = (SELECT MAX(CAST(run_number as INT)) 
                        FROM organizers) 
    '''

    df = pd.read_sql(querie, con=engine)

    df_tag = tags_table()

    df_comb = df.merge(df_tag[['profile_link', 'VK link']], on='profile_link', how='left')

    df_comb['tag'] = df_comb.apply(lambda row: link_to_tag(row['VK link'], row['name']), axis=1)

    roles = df['volunteer_role'].values
    names = df_comb['tag'].values
    role_dict = odict()

    for k in range(len(roles)):
        if roles[k] in role_dict:
            role_dict[roles[k]].append(names[k])
        else:
            role_dict[roles[k]] = [names[k]]


    # Отображаем таблицу 
    st.markdown(f'''
                Количество волонтеров:{df_comb['tag'].nunique()}, {len(df)}  
                ''')

    st.write(dict_to_text(role_dict), unsafe_allow_html=True)