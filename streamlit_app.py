import streamlit as st
import pandas as pd
import json
import requests

from utils.azure_config import configure_azure
from utils.payload import create_payload, payload_gpto_mini, payload_azure_ai
from utils.image_to_b64 import image_to_base64, base64_to_png

az_function_url = "https://funcoesmichelet.azurewebsites.net/api/image_to_base64"
ENDPOINT_AZURE_AI = "https://synchrodatapowersolutions.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-06-01"
OPENAI_URL = "https://api.openai.com/v1/chat/completions"
st.title("Aplicativo de Avaliação de Modelo")

# Carregador de arquivo
arquivo = st.file_uploader("Escolha um arquivo para enviar")
if arquivo is not None:
    filename = arquivo.name
    conteudo_base64, arquivo_png = image_to_base64(arquivo)
    # headers, payload = payload_gpto_mini(st.secrets["token_mich"], conteudo_base64)
    # headers, payload = payload_gpto_mini(st.secrets["token_gm"], conteudo_base64)
    headers, payload = payload_azure_ai(st.secrets["token_gm"], conteudo_base64)
    # Send request
    try:
        # response = requests.post(ENDPOINT_AZURE_AI, headers=headers, json=payload)
        # response = requests.post(OPENAI_URL, headers=headers, json=payload)
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
    df_resultado = pd.DataFrame(list(objeto_json.items()), columns=["Campo", "Valor"])

    st.table(df_resultado)
    comentario = st.text_area("Escreva um comentário:", height=150)

    if st.button("Enviar para Avaliação"):
        st.write("Arquivo enviado com sucesso!")
