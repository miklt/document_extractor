from azure.identity import ClientSecretCredential


def configure_azure():
    # Configuration
    TENANT_ID = "YOUR_TENANT_ID"
    CLIENT_ID = "YOUR_CLIENT_ID"
    CLIENT_SECRET = ""
    RESOURCE = "https://management.azure.com/.default"
    IMAGE_PATH = "YOUR_IMAGE_PATH"

    # Authenticate and get token
    credential = ClientSecretCredential(
        tenant_id=TENANT_ID, client_id=CLIENT_ID, client_secret=CLIENT_SECRET
    )
    token = credential.get_token(RESOURCE).token
    print(token, "token")


# Show title and description.
