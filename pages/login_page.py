# # import pickle
# from pathlib import Path

import streamlit_authenticator as stauth
import streamlit as st
from utils import authentication, login_fields

authenticator = authentication()
name, authentication_status, username = authenticator.login(location="main", key="Login", fields=login_fields)

if authentication_status:
    st.session_state.authentication_status = True
    st.switch_page('pages/home.py')
elif authentication_status is False:
    st.session_state.authentication_status = False
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.session_state.authentication_status = None
    st.warning('Please enter your username and password')

st.page_link("pages/home.py", label="Продолжить без входа", icon="🏠")
# st.write(st.session_state)