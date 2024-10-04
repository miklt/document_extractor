import requests
import streamlit as st
import json
from utils.payload import payload_azure_ai, payload_base64_azure_ai


def send_request_to_azure_ai(token, conteudo_base64=None, ocr_text=None, prompt=None):
    # headers, payload = payload_azure_ai(token=token, ocr_text=ocr_text, prompt=prompt)

    headers, payload = payload_base64_azure_ai(
        token=token, base64_image_1=conteudo_base64, prompt=prompt, ocr_text=ocr_text
    )
    print("Sending image request to Azure AI")
    print(prompt)
    # Send request
    ENDPOINT_AZURE_AI = "https://synchrodatapowersolutions.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-06-01"
    response = None
    try:
        s = requests.Session()
        response = s.post(
            # response = requests.post(
            ENDPOINT_AZURE_AI,
            headers=headers,
            json=payload,
        )
        s.close()

        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        if response is not None:
            print(response, "response")
            st.session_state["json_from_ai_received"] = True
            json_string = response.json()["choices"][0]["message"]["content"]
            print(json_string)
            # Convert the string to a JSON object
            json_string = json_string.replace(
                "'", '"'
            )  # Replace single quotes with double quotes
            objeto_json = json.loads(json_string)
            st.session_state["json_object"] = objeto_json

        return response
    except requests.RequestException as e:
        st.error(f"Failed to make the request. Error: {e}")
        return None
