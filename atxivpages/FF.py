import streamlit as st
from menu import menu
import requests
import re
from bs4 import BeautifulSoup

st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

menu()

st.header('Список фотофинишей')

# URL on the Github where the folders files are stored
github_url = 'https://github.com/AndreyKurdyubov/FF'  # change USERNAME, REPOSITORY and FOLDER with actual name

result = requests.get(github_url)

soup = BeautifulSoup(result.text, 'html.parser')
folders = soup.find_all(title=re.compile("^out_[\d]*.html$"))

filename = [ ]
for i in folders:
        filename.append(i.extract().get_text()[4:7])

ffs = list(sorted(set(filename), reverse=True))
print(ffs)

def template(ff):
      return f"https://html-preview.github.io/?url=https://github.com/AndreyKurdyubov/FF/blob/main/out_{ff}.html"

out = ""

for ff in ffs:
    out += f"[#{ff}]({template(ff)})\n\n"

st.write(out)    