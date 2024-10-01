import requests
import streamlit as st
import json
from utils.payload import payload_azure_ai

ENDPOINT_AZURE_AI = "https://synchrodatapowersolutions.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-06-01"


def send_request_to_azure_ai(token, conteudo_base64, prompt):
    headers, payload = payload_azure_ai(token, conteudo_base64, prompt=prompt)
    print("Sending request to Azure AI")
    print(prompt)
    # Send request
    try:
        response = requests.post(
            ENDPOINT_AZURE_AI, headers=headers, json=payload, timeout=10
        )
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        print(response)
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
        return response
    except Exception as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")
