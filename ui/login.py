import streamlit as st


def check_credentials(username, password):
    if username == st.secrets["USERNAME"] and password == st.secrets["PASSWORD"]:
        st.session_state["authenticated"] = True
    else:
        st.error("Senha ou usuário inválidos")


def login():
    st.title("Login")
    username = st.text_input("Usuário", key="username")
    password = st.text_input("Senha", type="password", key="password")
    if st.button("Login", on_click=check_credentials, args=(username, password)):
        pass
