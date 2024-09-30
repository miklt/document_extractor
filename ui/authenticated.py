import streamlit as st
import pandas as pd
import json


from utils.payload import payload_azure_ai
from utils.image_to_b64 import image_to_base64
from utils.request_to_azure import send_request_to_azure_ai
from db.postgres import insert_document


def authenticated_page():
    # Carregador de arquivo
    arquivo = st.file_uploader("Escolha um arquivo para enviar")
    if arquivo is not None:
        st.session_state["file_uploaded"] = True
        filename = arquivo.name
        conteudo_base64, arquivo_png = image_to_base64(arquivo)
        if conteudo_base64 is not None:
            st.session_state["file_decoded"] = True
        if arquivo_png is not None:
            st.session_state["png_file"] = arquivo_png
        # prompt = "Extraia as informações abaixo e retorne um objeto JSON que segue a norma RFC8259 no seguinte formato: {'cnpj':<string>,'data_hora_entrega':<string>,'hash_arquivo':<string>,'inscricao':<string>,'periodo_base':<string no formato 'aaaa-mm' por exemplo 2024-05>,'protocolo':<string>,'tipo_entrega':<string>,'validacao':<string>}"
        prompt = st.session_state["text_prompt"]
        response = send_request_to_azure_ai(
            st.secrets["token_gm"], conteudo_base64, prompt
        )

        if response is not None:
            st.session_state["json_from_ai_received"] = True

            json_string = response.json()["choices"][0]["message"]["content"]
            print(json_string)
            # Convert the string to a JSON object
            json_string = json_string.replace(
                "'", '"'
            )  # Replace single quotes with double quotes
            objeto_json = json.loads(json_string)
            st.session_state["json_object"] = objeto_json


def visualizar_resultado():
    # Visualize the image file
    if st.session_state["png_file"]:
        st.image(
            st.session_state.png_file,
            caption="Imagem enviada",
            use_column_width=True,
            output_format="PNG",
        )
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

        if st.button(
            "Enviar para Avaliação",
            on_click=insert_document,
            args=(objeto_json, comentario),
        ):
            st.toast("Arquivo enviado com sucesso!")
