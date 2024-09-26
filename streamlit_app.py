import streamlit as st
import pandas as pd
import json
import requests

from utils.azure_config import configure_azure
from utils.payload import create_payload, payload_gpto_mini
from utils.image_to_b64 import image_to_base64, base64_to_png

az_function_url = "https://funcoesmichelet.azurewebsites.net/api/image_to_base64"
ENDPOINT_AZURE_AI = "https://synchrodatapowersolutions.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview"
OPENAI_URL = "https://api.openai.com/v1/chat/completions"
st.title("Aplicativo de Avaliação de Modelo")

# Carregador de arquivo
arquivo = st.file_uploader("Escolha um arquivo para enviar")
if arquivo is not None:
    filename = arquivo.name
    print(filename)
    conteudo_base64 = image_to_base64(arquivo)
    headers, payload = payload_gpto_mini(st.secrets["token_mich"], conteudo_base64)
    # Send request
    try:
        # response = requests.post(ENDPOINT_AZURE_AI, headers=headers, json=payload)
        response = requests.post(OPENAI_URL, headers=headers, json=payload)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")

    # Handle the response as needed (e.g., print or process)

    objeto_json = json.loads(response.json()["choices"][0]["message"]["content"])
    print(objeto_json)

    # Visualize the image file
    st.image(arquivo, caption="Imagem enviada", use_column_width=True)
    df_resultado = pd.DataFrame(list(objeto_json.items()), columns=["Campo", "Valor"])

    # # Exibir a tabela
    # edited_values = {}
    # for index, row in df_resultado.iterrows():
    #     edited_value = st.text_input(f"{row['Campo']}:", value=row["Valor"])
    #     edited_values[row["Campo"]] = edited_value

    # edited_object = json.dumps(edited_values)
    # st.json(edited_object)
    st.table(df_resultado)
    comentario = st.text_area("Escreva um comentário:", height=150)

    if st.button("Enviar para Avaliação"):
        st.write("Arquivo enviado com sucesso!")


# if arquivo is not None:
#     # Enviar o arquivo para a API
#     files = {"file": arquivo.getvalue()}
#     response = requests.post(az_function_url, files=files)

#     if response.status_code == 200:
#         base64_image = response.json()
#         conteudo_base64 = base64_image["content"]
#         # headers, payload = create_payload(st.secrets["openai_api_key"], conteudo_base64)
#         headers, payload = payload_gpto_mini(st.secrets["token_mich"], conteudo_base64)
#         # Send request
#         try:
#             # response = requests.post(ENDPOINT_AZURE_AI, headers=headers, json=payload)
#             response = requests.post(OPENAI_URL, headers=headers, json=payload)
#             response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
#         except requests.RequestException as e:
#             raise SystemExit(f"Failed to make the request. Error: {e}")

#         # Handle the response as needed (e.g., print or process)

#         objeto_json = json.loads(response.json()["choices"][0]["message"]["content"])
#         print(objeto_json)
#         df_resultado = pd.DataFrame(
#             list(objeto_json.items()), columns=["Campo", "Valor"]
#         )

#         # Exibir a tabela
#         st.table(df_resultado)
#         comentario = st.text_area("Escreva um comentário:", height=150)

#         if st.button("Enviar para Avaliação"):
#             st.write("Arquivo enviado com sucesso!")
