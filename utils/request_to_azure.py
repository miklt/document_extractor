import requests
from utils.payload import payload_azure_ai

ENDPOINT_AZURE_AI = "https://synchrodatapowersolutions.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-06-01"


def send_request_to_azure_ai(token, conteudo_base64, prompt):
    headers, payload = payload_azure_ai(token, conteudo_base64, prompt=prompt)
    # Send request
    try:
        response = requests.post(ENDPOINT_AZURE_AI, headers=headers, json=payload)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response
    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")
