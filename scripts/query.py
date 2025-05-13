import os
from langchain.vectorstores import FAISS
from langchain.embeddings import OllamaEmbeddings
from langchain.chat_models import ChatOllama
from langchain.chains import RetrievalQA
from config import OLLAMA_EMBED_MODEL, OLLAMA_LLM_MODEL
from langchain.callbacks.base import BaseCallbackHandler
from queue import Queue
from threading import Thread

# FAISS index location
FAISS_INDEX_DIR = os.path.join(os.path.dirname(__file__), "..", "faiss_index")

# Streaming callback handler
class StreamHandler(BaseCallbackHandler):
    def __init__(self, queue: Queue):
        self.queue = queue

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.queue.put(token)

def load_faiss_vector_store():
    embeddings = OllamaEmbeddings(model=OLLAMA_EMBED_MODEL)
    return FAISS.load_local(FAISS_INDEX_DIR, embeddings, allow_dangerous_deserialization=True)

def ask_question(query):
    vector_store = load_faiss_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    llm = ChatOllama(model=OLLAMA_LLM_MODEL)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=False
    )
    return qa_chain.run(query)

# 🆕 Generator-based streaming
def stream_answer(query):
    queue = Queue()
    handler = StreamHandler(queue)

    vector_store = load_faiss_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # Enable streaming
    llm = ChatOllama(model=OLLAMA_LLM_MODEL, streaming=True, callbacks=[handler])

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=False
    )

    def task():
        try:
            qa_chain.run(query)
        finally:
            queue.put(None)  # Signal end of stream

    # Run the model in a background thread
    thread = Thread(target=task)
    thread.start()

    while True:
        token = queue.get()
        if token is None:
            break
        yield token

def main():
    vector_store = load_faiss_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    llm = ChatOllama(model=OLLAMA_LLM_MODEL)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    while True:
        query = input("\n❓ Ask a question (or type 'exit'): ")
        if query.lower() == "exit":
            break

        result = qa_chain.run(query)
        print("\n💡 Answer:")
        print(result)

if __name__ == "__main__":
    main()
