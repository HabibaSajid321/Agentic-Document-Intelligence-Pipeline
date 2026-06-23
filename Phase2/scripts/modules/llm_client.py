# scripts/llm_client.py
import requests
import json

OLLAMA_URL = "http://localhost:11434"

def query_llm(prompt: str, model: str = "llama3:8b") -> dict:
    payload = {
        "model": model,
        "prompt": prompt,
        "format": "json",
        "stream": False,
        "options": {"temperature": 0.0}
    }
    try:
        response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        return json.loads(result["response"])
    except Exception as e:
        raise RuntimeError(f"LLM call failed: {e}")