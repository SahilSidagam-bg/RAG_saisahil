from .embed import get_ollama_embedding
from .db import insert_document, search_similar
from .chat import query_llama3

def generate_answer(query):
    """Generates an answer using the query and relevant document context."""
    
    # Step 1: Generate embedding for the query
    query_emb = get_ollama_embedding(query)
    
    # Step 2: Search for similar documents in the database
    results = search_similar(query_emb)
    
    # Step 3: Get the text content of the top results to use as context
    context = "\n".join([doc["text"] for doc in results])
    
    # Step 4: Formulate the prompt with context and query
    prompt = f"""Use the following context to answer:
    {context}

    Question: {query}
    Answer:"""
    
    # Step 5: Query Ollama LLaMA 3 to generate the answer
    answer = query_llama3(prompt)
    
    return answer
