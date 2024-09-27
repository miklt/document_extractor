import streamlit as st
from ui.authenticated import authenticated_page
from ui.login import login


# Main logic
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if st.session_state["authenticated"]:
    authenticated_page()
else:
    login()
