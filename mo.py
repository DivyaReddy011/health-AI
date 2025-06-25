import os
import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("AI_API_KEY")


def get_access_token():
    token_url = "https://iam.cloud.ibm.com/identity/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "apikey": API_KEY,
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
    }
    response = requests.post(token_url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"❌ Failed to get access token: {response.text}")

# Step 2: List all available models
def list_supported_models():
    access_token = get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    url = "https://us-south.ml.cloud.ibm.com/ml/v1/foundation_model_specs?version=2024-05-01"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        models = response.json().get("resources", [])
        print("✅ Available Models:")
        for model in models:
            print(f"- {model.get('model_id')}")
    else:
        print(f"❌ API Error: {response.status_code} - {response.text}")

# Run it
if __name__ == "__main__":
    list_supported_models()
