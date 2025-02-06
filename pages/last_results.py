import pandas as pd
from sqlalchemy import create_engine, text
import streamlit as st
import streamlit.components.v1 as components
from menu import menu
import base64

st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

menu()


# """### gif from local file"""
# with open("PF/131/photos_131/1.jpg", "rb") as file_:
#     contents = file_.read()
#     data_url = base64.b64encode(contents).decode("utf-8")

    # st.markdown(
    # f'<img src="data:image/jpeg;base64,{data_url}" alt="cat gif">',
    # unsafe_allow_html=True,
    # )

with open("PF/131/out_131.html", 'r', encoding='utf-8') as file:
    source_code = file.read() 

components.html(source_code, width=500, height=300, scrolling=True)