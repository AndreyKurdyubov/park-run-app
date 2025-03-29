import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
from collections import OrderedDict as odict

def title(string):
    return string.title()

def dict_to_text(d):
    result = []
    for key, values in d.items():
        result.append(f"{key}:")
        result.append(", ".join(map(title, values)))
    return "<br>".join(result)

st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

st.title('Волонтеры для отчета')

engine = create_engine('sqlite:///mydatabase.db')
querie = '''
SELECT * 
FROM organizers
WHERE run_number = (SELECT MAX(CAST(run_number as INT)) 
                    FROM organizers) 
'''

df = pd.read_sql(querie, con=engine)

roles = df['volunteer_role'].values
names = df['name'].values
role_dict = odict()

for k in range(len(roles)):
    if roles[k] in role_dict:
        role_dict[roles[k]].append(names[k])
    else:
        role_dict[roles[k]] = [names[k]]


# Отображаем таблицу 
st.data_editor(
    df,
    column_config={
        'profile_link': st.column_config.LinkColumn(),
    },
    hide_index=True
)

st.markdown(f'''
            Уникальных участников в таблице {len(df)}  
            ''')


st.write(dict_to_text(role_dict), unsafe_allow_html=True)

st.write("""
**INDUSTRY**  
Software Application
""")