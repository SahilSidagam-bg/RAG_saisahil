import requests

def get_ollama_embedding(text):
    """Fetch the embedding for the provided text using the Ollama API."""
    api_url = "http://localhost:11411/v1/embeddings"
    payload = {
        "model": "llama3",  # Specify the LLaMA 3 model
        "input": text
    }
    response = requests.post(api_url, json=payload)
    
    if response.status_code == 200:
        return response.json()['embedding']
    else:
        raise Exception(f"Error fetching embedding: {response.text}")
