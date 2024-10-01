import streamlit as st
from ui.authenticated import (
    authenticated_page,
    visualizar_resultado,
    visualizar_png,
    enviar_imagem_para_azure,
)
from db.postgres import get_prompts
from ui.login import login


if "file_uploaded" not in st.session_state:
    st.session_state["file_uploaded"] = False
if "file_decoded" not in st.session_state:
    st.session_state["file_decoded"] = False
if "conteudo_base64" not in st.session_state:
    st.session_state["conteudo_base64"] = None
if "png_file" not in st.session_state:
    st.session_state["png_file"] = None
if "json_object" not in st.session_state:
    st.session_state["json_object"] = None
if "prompt_received" not in st.session_state:
    st.session_state["prompt_received"] = False

if "text_prompts" not in st.session_state:
    st.session_state["text_prompts"] = None

if "json_from_ai_received" not in st.session_state:
    st.session_state["json_from_ai_received"] = False
# Main logic
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
st.title("Aplicativo de Avaliação de Modelo")

if not st.session_state["prompt_received"]:
    prompts = get_prompts()

    if prompts is not None:
        st.session_state["text_prompts"] = prompts
        st.session_state["prompt_received"] = True

if st.session_state["authenticated"]:
    if not st.session_state["file_uploaded"]:
        authenticated_page()

    visualizar_png()
    enviar_imagem_para_azure()
    visualizar_resultado()
else:
    login()
