import requests

def query_llama3(prompt):
    """Query the LLaMA 3 model for an answer based on the provided prompt."""
    api_url = "http://localhost:11411/v1/llama3"
    payload = {
        "model": "llama3",  # LLaMA 3 model
        "input": prompt
    }
    response = requests.post(api_url, json=payload)
    
    if response.status_code == 200:
        return response.json()['output']
    else:
        raise Exception(f"Error querying model: {response.text}")
