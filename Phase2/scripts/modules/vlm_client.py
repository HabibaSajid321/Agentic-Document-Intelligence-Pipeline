# scripts/vlm_client.py
import requests
import base64
OLLAMA_URL = "http://localhost:11434"

def query_vlm(image_path: str, prompt: str, model: str = "llava:7b-v1.6-mistral-fp16") -> str:
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    payload = {
        "model": model,
        "prompt": prompt,
        "images": [b64],
        "stream": False,
        "options": {"temperature": 0.2}
    }
    r = requests.post(f"{OLLAMA_URL}/api/generate", json=payload)
    return r.json()["response"]