# # import pickle
# from pathlib import Path

import streamlit_authenticator as stauth
import streamlit as st
from utils import authentication
import time

authenticator, name, authentication_status, username = authentication(page='login_page')

st.page_link("pages/home.py", label="Продолжить без входа", icon="🏠")
if authentication_status:
    time.sleep(1)
    st.switch_page('pages/home.py')
    
# st.write(st.session_state)
