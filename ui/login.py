import streamlit as st


def login():
    st.title("Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    # Check credentials
    if st.button("Login"):
        if username == st.secrets["USERNAME"] and password == st.secrets["PASSWORD"]:
            st.session_state["authenticated"] = True
        else:
            st.error("Senha ou usuário inválidos")
