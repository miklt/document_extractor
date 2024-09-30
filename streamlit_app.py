import streamlit as st
from ui.authenticated import authenticated_page, visualizar_resultado
from db.postgres import get_prompt
from ui.login import login


if "file_uploaded" not in st.session_state:
    st.session_state["file_uploaded"] = False
if "file_decoded" not in st.session_state:
    st.session_state["file_decoded"] = False
if "png_file" not in st.session_state:
    st.session_state["png_file"] = None
if "json_object" not in st.session_state:
    st.session_state["json_object"] = None
if "prompt_received" not in st.session_state:
    st.session_state["prompt_received"] = False

if "text_prompt" not in st.session_state:
    st.session_state["text_prompt"] = None

if "json_from_ai_received" not in st.session_state:
    st.session_state["json_from_ai_received"] = False
# Main logic
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
st.title("Aplicativo de Avaliação de Modelo")

if not st.session_state["prompt_received"]:
    prompt = get_prompt()[0]
    
    if prompt is not None:
        st.session_state["text_prompt"] = prompt
        st.session_state["prompt_received"] = True

if st.session_state["authenticated"]:
    if not st.session_state["file_uploaded"]:
        authenticated_page()
    visualizar_resultado()
else:
    login()
