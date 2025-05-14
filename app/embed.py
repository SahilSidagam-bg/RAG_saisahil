import requests

def get_ollama_embedding(text):
    """Fetch the embedding for the provided text using the Ollama API."""
    api_url = "http://localhost:11434/api/embeddings"
    payload = {
        "model": "nomic-embed-text",
        "prompt": text
    }

    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()  # Raises an error for 4xx/5xx responses
        resp_json = response.json()
    except requests.exceptions.RequestException as req_err:
        raise Exception(f"HTTP error during embedding request: {req_err}")
    except ValueError:
        raise Exception(f"Invalid JSON response: {response.text}")

    if 'embedding' in resp_json:
        return resp_json['embedding']
    else:
        raise KeyError(f"'embedding' key not found in response: {resp_json}")
