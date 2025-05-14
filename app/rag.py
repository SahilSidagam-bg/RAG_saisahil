from .embed import get_ollama_embedding
from .db import search_similar
from .chat import query_llama3

def generate_answer(query):
    """Generates an answer using the query and relevant document context."""

    print("\n🔍 New query received:")
    print("🧠 Query:", query)

    # Step 1: Generate embedding
    try:
        query_emb = get_ollama_embedding(query)
        print("🔢 Embedding generated. Dimension:", len(query_emb))
    except Exception as e:
        print("❌ Failed to generate embedding:", str(e))
        return "❌ Error: Failed to generate query embedding."

    # Step 2: Search for similar documents
    try:
        results = search_similar(query_emb)
        print(f"🔁 Retrieved {len(results)} similar document(s).")
    except Exception as e:
        print("❌ Search failed:", str(e))
        return "❌ Error: Failed to search for similar documents."

    # Fallback if no results found
    if not results:
        print("⚠️ No similar documents found for this query.")
        return "⚠️ No relevant documents found in the database. Try rephrasing your question."

    # Step 3: Build context from top results
    context_pieces = []
    for i, doc in enumerate(results, 1):
        score = doc.get("score", "N/A")
        preview = doc["text"][:150].replace("\n", " ")
        print(f"📄 Doc {i} | Score: {score} | Preview: {preview}...")
        context_pieces.append(doc["text"])

    context = "\n".join(context_pieces)

    # Step 4: Build RAG prompt
    prompt = f"""Use the following context to answer the question:
{context}

Question: {query}
Answer:"""

    print("📨 Sending prompt to LLaMA 3 via Ollama...")

    # Step 5: Query LLaMA 3
    try:
        answer = query_llama3(prompt)
        print("✅ Answer received from LLaMA 3.")
        return answer
    except Exception as e:
        print("❌ LLaMA 3 query failed:", str(e))
        return "❌ Error: Failed to generate answer from LLaMA 3."
