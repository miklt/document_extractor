def payload_gpto_mini(token, base64_image_1):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    payload = {
        "model": "gpt-4o-mini",
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
