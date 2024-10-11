import streamlit as st
import pandas as pd

from utils.FileToBase64 import FileToBase64
from utils.request_to_azure import send_request_to_azure_ai
from db.postgres import insert_document_v2


@st.dialog("Arquivo enviado com sucesso")
def reiniciar_app():
    st.write("O arquivo foi enviado com sucesso. Você pode fechar esta mensagem.")
    st.session_state["file_uploaded"] = False
    st.session_state["file_decoded"] = False
    st.session_state["pdf_text_no_ocr"] = None
    st.session_state["filename"] = None
    st.session_state["conteudo_base64"] = None
    st.session_state["png_file"] = None
    st.session_state["json_object"] = None
    st.session_state["tipo_documento"] = None
    st.session_state["json_from_ai_received"] = False
    st.session_state["token_metadata"] = None

    if st.button("Ok"):
        st.rerun()
    else:
        st.session_state["label_button_enviar"] = "Enviar outro documento"


def get_label(label):
    if label == "acessorio":
        return "Acessório"
    if label == "principal":
        return "Principal"
    if label == "compensacao":
        return "Compensação"
    if label == "nfe":
        return "Nota Fiscal"


def authenticated_page():
    # Carregador de arquivo
    arquivo = st.file_uploader("Escolha um arquivo para enviar")
    st.session_state["label_button_enviar"] = "Salvar Documento"
    if arquivo is not None:
        st.session_state["file_uploaded"] = True
        filename = arquivo.name
        st.session_state["filename"] = filename

        # conteudo_base64, arquivo_png = image_to_base64(arquivo)

        conteudo_base64, arquivo_png, pdf_text_no_ocr = FileToBase64.get_base64(arquivo)
        if conteudo_base64 is not None:
            st.session_state["file_decoded"] = True
            st.session_state["conteudo_base64"] = conteudo_base64
        if arquivo_png is not None:
            st.session_state["png_file"] = arquivo_png
        if pdf_text_no_ocr is not None:
            st.session_state["pdf_text_no_ocr"] = pdf_text_no_ocr
        arquivo = None


def enviar_imagem_para_azure():
    if st.session_state["conteudo_base64"] is None:
        st.info("Nenhum arquivo foi carregado")
        return
    else:
        conteudo_base64 = st.session_state["conteudo_base64"]

    tipo_documento = st.radio(
        "Tipo de Documento",
        ["acessorio", "principal", "compensacao", "nfe"],
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
    detail = st.radio(
        "Detalhe",
        ["auto", "high", "low"],
        index=None,
        horizontal=True,
    )
    if not detail:
        st.info("Selecione a qualidade da imagem esperada")
        return
    st.session_state["detail"] = detail
    if st.session_state["pdf_text_no_ocr"]:
        prompt = (
            prompt
            + "Além da imagem, considere o markdown a seguir extraído do PDF\n\n"
            + st.session_state["pdf_text_no_ocr"]
        )
    if st.button(
        "Consultar IA",
        on_click=send_request_to_azure_ai,
        args=(
            st.secrets["token_gm"],
            st.session_state["conteudo_base64"],
            prompt,
            st.session_state["detail"],
        ),
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
        tokens = st.session_state.token_metadata

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
                st.session_state["escala_imagem"],
                st.session_state["token_metadata"],
                st.session_state["detail"],
            ),
        ):
            reiniciar_app()
