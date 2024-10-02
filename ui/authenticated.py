import streamlit as st
import pandas as pd
import json


from utils.payload import payload_azure_ai
from utils.image_to_b64 import image_to_base64
from utils.request_to_azure import send_request_to_azure_ai
from db.postgres import insert_document_v2


@st.dialog("Arquivo enviado com sucesso")
def reiniciar_app():
    st.write("O arquivo foi enviado com sucesso. Você pode fechar esta mensagem.")
    st.session_state["file_uploaded"] = False
    st.session_state["file_decoded"] = False
    st.session_state["filename"] = None
    st.session_state["conteudo_base64"] = None
    st.session_state["png_file"] = None
    st.session_state["json_object"] = None
    st.session_state["tipo_documento"] = None
    st.session_state["json_from_ai_received"] = False

    if st.button("Ok"):
        st.rerun()
    else:
        st.session_state["label_button_enviar"] = "Enviar outro documento"


def escolher_prompt(tipo_prompt):
    print(tipo_prompt)
    if tipo_prompt == "prompt 1":
        st.session_state["text_prompt"] = st.secrets["prompt_1"]


def get_label(label):
    if label == "acessorio":
        return "Acessório"
    if label == "principal":
        return "Principal"
    if label == "compensacao":
        return "Compensação"


def authenticated_page():
    # Carregador de arquivo
    arquivo = st.file_uploader("Escolha um arquivo para enviar")
    st.session_state["label_button_enviar"] = "Salvar Documento"
    if arquivo is not None:
        st.session_state["file_uploaded"] = True
        filename = arquivo.name
        st.session_state["filename"] = filename
        conteudo_base64, arquivo_png = image_to_base64(arquivo)
        if conteudo_base64 is not None:
            st.session_state["file_decoded"] = True
            st.session_state["conteudo_base64"] = conteudo_base64
        if arquivo_png is not None:
            st.session_state["png_file"] = arquivo_png
        arquivo = None


def enviar_imagem_para_azure():
    if st.session_state["conteudo_base64"] is None:
        st.info("Nenhum arquivo foi carregado")
        return
    else:
        conteudo_base64 = st.session_state["conteudo_base64"]

    tipo_documento = st.radio(
        "Tipo de Documento",
        ["acessorio", "principal", "compensacao"],
        index=None,
        format_func=get_label,
        horizontal=True,
    )
    if not tipo_documento:
        st.info("Selecione um tipo de documento")
        return
    else:
        st.session_state["tipo_documento"] = tipo_documento
    # atualizar o prompt pelo select box
    if st.session_state["text_prompts"] is not None:
        prompt = st.session_state["text_prompts"][tipo_documento]

    # st.write("Prompt: ", prompt)
    if st.button(
        "Consultar IA",
        on_click=send_request_to_azure_ai,
        args=(st.secrets["token_gm"], conteudo_base64, prompt),
    ):
        pass


def visualizar_png():
    if st.session_state["png_file"]:
        st.image(
            st.session_state.png_file,
            caption="Imagem enviada",
            use_column_width=True,
            output_format="PNG",
        )


def visualizar_resultado():
    if st.session_state.json_object:
        st.write("Resultado da extração de informações:")
        objeto_json = st.session_state.json_object

        df_resultado = pd.DataFrame(
            list(objeto_json.items()), columns=["Campo", "Valor"]
        )

        st.table(df_resultado)
        comentario = st.text_area(
            "Escreva um comentário:",
            height=150,
        )
        if comentario:
            pass

        if st.button(
            st.session_state["label_button_enviar"],
            on_click=insert_document_v2,
            args=(
                objeto_json,
                st.session_state["tipo_documento"],
                st.session_state["filename"],
                comentario,
            ),
        ):
            reiniciar_app()
