# # import pickle
# from pathlib import Path

import streamlit_authenticator as stauth
import streamlit as st
from streamlit import session_state as ss
from utils import authentication
import time

authenticator, name, authentication_status, username = authentication(page='login_page')

placeholder = st.empty()
placeholder.page_link("pages/home.py", label="Продолжить без входа", icon="🏠")
if authentication_status:
    placeholder.write("Переходим на домашнюю страницу")
    time.sleep(1)
    ss.session_start = 1
    st.switch_page('pages/home.py')
    
# st.write(st.session_state)
