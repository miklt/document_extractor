import streamlit as st
import pandas as pd
import json
from openai import OpenAI
import requests
from azure.identity import ClientSecretCredential


def configure_azure():
    # Configuration
    TENANT_ID = "YOUR_TENANT_ID"
    CLIENT_ID = "YOUR_CLIENT_ID"
    CLIENT_SECRET = "80984f26431044419225d9e6aff5ea39"
    RESOURCE = "https://management.azure.com/.default"
    IMAGE_PATH = "YOUR_IMAGE_PATH"

    # Authenticate and get token
    credential = ClientSecretCredential(
        tenant_id=TENANT_ID, client_id=CLIENT_ID, client_secret=CLIENT_SECRET
    )
    token = credential.get_token(RESOURCE).token
    print(token, "token")


# Show title and description.


def payload_gpto_mini(token, base64_image_1):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "Você é um assistente de IA que ajuda as pessoas a encontrar informações.",
                    },
                    {
                        "type": "text",
                        "text": "You are a machine that only returns and replies with valid, iterable RFC8259 compliant JSON in your responses. Don't use a codeblock json format, just return the JSON object.",
                    },
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image_1}",
                        },
                    },
                    {
                        "type": "text",
                        "text": "Extraia as informações abaixo e retorne um objeto JSON que segue a norma RFC8259 no seguinte formato: {'cnpj':<string>,'data_hora_entrega':<string>,'hash_arquivo':<string>,'inscricao':<string>,'periodo_base':<string no formato 'aaaa-mm' por exemplo 2024-05>,'protocolo':<string>,'tipo_entrega':<string>,'validacao':<string>}.",
                    },
                    {
                        "type": "text",
                        "text": "Don't use a codeblock json format, just return the JSON object without breaklines or spaces.",
                    },
                ],
            },
        ],
        "max_tokens": 300,
    }
    return headers, payload


def create_payload(token, encoded_image):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

    # Payload for the request
    payload = (
        {
            "messages": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": "Você é um assistente de IA que ajuda as pessoas a encontrar informações.",
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{encoded_image}"
                            },
                        },
                        {
                            "type": "text",
                            "text": "Extraia as informações abaixo e retorne um JSON:",
                        },
                        {"type": "text", "text": "• CNPJ"},
                        {"type": "text", "text": "• Data Hora de Entrega"},
                        {"type": "text", "text": "• Hash arquivo"},
                        {"type": "text", "text": "• Inscrição"},
                        {
                            "type": "text",
                            "text": "• Período Base (utilize o formato ano-mes. Ex.: 2024-05)",
                        },
                        {"type": "text", "text": "• Protocolo"},
                        {"type": "text", "text": "• Tipo de Entrega"},
                        {"type": "text", "text": "• Validação"},
                    ],
                },
            ]
        },
    )
    return headers, payload


az_function_url = "https://funcoesmichelet.azurewebsites.net/api/image_to_base64"
ENDPOINT_AZURE_AI = "https://synchrodatapowersolutions.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview"
OPENAI_URL = "https://api.openai.com/v1/chat/completions"
st.title("Aplicativo de Avaliação de Modelo")

# Carregador de arquivo
arquivo = st.file_uploader("Escolha um arquivo para enviar")

if arquivo is not None:
    # Enviar o arquivo para a API
    files = {"file": arquivo.getvalue()}
    response = requests.post(az_function_url, files=files)

    if response.status_code == 200:
        base64_image = response.json()
        conteudo_base64 = base64_image["content"]
        # headers, payload = create_payload(st.secrets["openai_api_key"], conteudo_base64)
        headers, payload = payload_gpto_mini(st.secrets["token_mich"], conteudo_base64)
        # Send request
        try:
            # response = requests.post(ENDPOINT_AZURE_AI, headers=headers, json=payload)
            response = requests.post(OPENAI_URL, headers=headers, json=payload)
            response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        except requests.RequestException as e:
            raise SystemExit(f"Failed to make the request. Error: {e}")

        # Handle the response as needed (e.g., print or process)
        print(response.json())
        objeto_json = json.loads(response.json()["choices"][0]["message"]["content"])
        print(objeto_json)
        df_resultado = pd.DataFrame(
            list(objeto_json.items()), columns=["Campo", "Valor"]
        )

        # Exibir a tabela
        st.table(df_resultado)
        comentario = st.text_area("Escreva um comentário:", height=150)

        if st.button("Enviar para Avaliação"):
            st.write("Arquivo enviado com sucesso!")
