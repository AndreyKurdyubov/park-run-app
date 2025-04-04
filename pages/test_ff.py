import streamlit as st

def showFF(start_num, quantity=2, show=False, photos=False):
    url = f"https://raw.githubusercontent.com/AndreyKurdyubov/FF/main/photos_{start_num}"
    if show:
        for k in range(quantity):
            st.write(f'{k+1}')
            if photos: 
                st.image(image=url + f"/{k+1}.jpg")

def add_control(quantity, i):
    # Создаем контейнер и применяем CSS для горизонтального расположения
    st.markdown("""
                <style>
                    div[data-testid="column"] {
                        width: fit-content !important;
                        flex: unset;
                    }
                    div[data-testid="column"] * {
                        width: 200 !important;
                    }
                </style>
                """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        button = st.button(f"Нажми{i}")
    with col2:
        checkbox = st.checkbox(f"с фото{i}")

    if f"checkbox_prev_state_{i}" not in st.session_state:
        st.session_state[f"checkbox_prev_state_{i}"] = False

    if f"button_prev_state_{i}" not in st.session_state:
        st.session_state[f"button_prev_state_{i}"] = False

    if checkbox:
        st.session_state[f"checkbox_prev_state_{i}"] = checkbox

    if button:
        st.session_state[f"button_prev_state_{i}"] = not st.session_state[f"button_prev_state_{i}"]

    if st.session_state[f"button_prev_state_{i}"]:
        show = st.session_state[f"button_prev_state_{i}"]
        showFF(153, quantity=quantity, show=show, photos=checkbox)

add_control(quantity=1, i=1)

add_control(quantity=2, i=2)