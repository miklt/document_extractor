import streamlit as st
import pandas as pd
import json
import requests


from utils.payload import payload_azure_ai
from utils.image_to_b64 import image_to_base64

ENDPOINT_AZURE_AI = "https://synchrodatapowersolutions.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-06-01"


def authenticated_page():
    st.title("Aplicativo de Avaliação de Modelo")
    # Carregador de arquivo
    arquivo = st.file_uploader("Escolha um arquivo para enviar")
    if arquivo is not None:
        filename = arquivo.name
        conteudo_base64, arquivo_png = image_to_base64(arquivo)

        headers, payload = payload_azure_ai(st.secrets["token_gm"], conteudo_base64)
        # Send request
        try:

            response = requests.post(ENDPOINT_AZURE_AI, headers=headers, json=payload)
            response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        except requests.RequestException as e:
            raise SystemExit(f"Failed to make the request. Error: {e}")

        # Handle the response as needed (e.g., print or process)
        json_string = response.json()["choices"][0]["message"]["content"]
        # Convert the string to a JSON object
        json_string = json_string.replace(
            "'", '"'
        )  # Replace single quotes with double quotes
        objeto_json = json.loads(json_string)

        # Visualize the image file
        if arquivo_png is not None:
            st.image(arquivo_png, caption="Imagem enviada", use_column_width=True)
        df_resultado = pd.DataFrame(
            list(objeto_json.items()), columns=["Campo", "Valor"]
        )

        st.table(df_resultado)
        comentario = st.text_area("Escreva um comentário:", height=150)

        if st.button("Enviar para Avaliação"):
            st.write("Arquivo enviado com sucesso!")
