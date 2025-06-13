import requests
import os

API_TOKEN = os.getenv("HF_API_TOKEN") or "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"
MODEL_ID = "EleutherAI/gpt-neo-125M"

API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    
    if response.status_code == 404:
        print(f"Error: Model '{MODEL_ID}' not found (404). Check model ID and access rights.")
        return None
    elif response.status_code != 200:
        print(f"Error: HTTP {response.status_code} - {response.text}")
        return None
    
    return response.json()

if __name__ == "__main__":
    prompt = "Once upon a time"
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 50}}

    result = query(payload)
    if result:
        generated_text = result[0]["generated_text"] if isinstance(result, list) else result.get("generated_text")
        print("Generated text:\n", generated_text)
