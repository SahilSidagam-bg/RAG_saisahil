import requests

def query_llama3(prompt):
    """Query the LLaMA 3 model for an answer based on the provided prompt."""
    api_url = "http://localhost:11434/api/generate"  # Correct Ollama endpoint
    payload = {
        "model": "llama3",  # Ensure the model name matches your Ollama model (e.g., llama3:8b)
        "prompt": prompt,
        "stream": False  # Optional, avoids streaming
    }

    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()  # Raises HTTPError if status is not 200

        resp_json = response.json()

        if 'response' in resp_json:
            return resp_json['response'].strip()
        elif 'output' in resp_json:
            return resp_json['output'].strip()
        else:
            raise KeyError("No 'response' or 'output' field found in response.")
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Connection or HTTP error: {e}")
    except ValueError:
        raise Exception(f"Invalid JSON response: {response.text}")
    except Exception as e:
        raise Exception(f"Unexpected error: {e}")
