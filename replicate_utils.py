# replicate_utils.py
import os
import requests
import json

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")  # Set in .streamlit/secrets.toml

HEADERS = {
    "Authorization": f"Token {REPLICATE_API_TOKEN}",
    "Content-Type": "application/json"
}

REPLICATE_ENDPOINT = "https://api.replicate.com/v1/predictions"
MODEL_VERSION = "a16z-infra/mistral-7b-instruct-v0.1"  # Public model on Replicate


def ask_mistral(prompt: str, context: str = "") -> str:
    input_payload = {
        "version": MODEL_VERSION,
        "input": {
            "prompt": f"[INST] Use the following context to answer the question.\n\nContext: {context}\n\nQuestion: {prompt} [/INST]"
        }
    }

    response = requests.post(REPLICATE_ENDPOINT, headers=HEADERS, data=json.dumps(input_payload))

    if response.status_code != 201:
        return f"Error: {response.status_code} - {response.text}"

    prediction = response.json()
    prediction_url = prediction["urls"]["get"]

    # Poll for result
    while True:
        result = requests.get(prediction_url, headers=HEADERS).json()
        if result["status"] == "succeeded":
            return result["output"]
        elif result["status"] == "failed":
            return "Model failed to generate a response."
