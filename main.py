import streamlit as st
from utils import menu, authentication

authentication()
st.switch_page('pages/home.py')  # for stramlit 1.32 - to work on iphone with old ios 