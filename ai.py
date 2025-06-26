import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AI_API_KEY")
PROJECT_ID = os.getenv("AI_PROJECT_ID")
WML_URL = os.getenv("AI_URL")


def get_ai_response(prompt):
    token_url = "https://iam.cloud.ibm.com/identity/token"
    print("🔐 Getting access token...")
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "apikey": API_KEY,
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
    }

    token_response = requests.post(token_url, headers=headers, data=data)
    if token_response.status_code != 200:
        return "⚠️ Error fetching access token."

    access_token = token_response.json().get("access_token")
    print("✅ Access token received")
    print("🚀 Sending prompt to Granite model...")

    model_id = "ibm/granite-3-2b-instruct"
    inference_url = f"{WML_URL}/ml/v1/text/generation?version=2024-05-01"

    payload = {
        "model_id": model_id,
        "input": prompt,
        # "parameters": {
        #     "decoding_method": "greedy",
        #     "max_new_tokens": 500
        # },
        "parameters": {
            "decoding_method": "sample",    # Better than "greedy"
            "temperature": 0.7,               # Controls creativity
            "top_k": 50,                      # Top K sampling
            "top_p": 0.95,                    # Nucleus sampling
            "max_new_tokens": 500             # Longer output
        },
        "project_id": PROJECT_ID  
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(inference_url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()['results'][0]['generated_text']
    else:
        return f"❌ API Error: {response.status_code} - {response.text}"
# if __name__ == "__main__":
#     prompt = "Explain Artificial Intelligence in simple words."
#     response = get_ai_response(prompt)
#     print("🤖 Response:", response)
if __name__ == "__main__":
    while True:
        prompt = input("\n📝 Enter your prompt (or type 'exit' to quit):\n> ")
        if prompt.lower() == "exit":
            break
        response = get_ai_response(prompt)
        print("\n🤖 AI Response:\n", response)

