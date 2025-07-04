from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaLLM
import os

# 1️⃣ Carica e splitta il PDF
def load_and_split_pdf(pdf_path, chunk_size=1000, chunk_overlap=200):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = splitter.split_documents(documents)
    return docs

def answer_query(query, k=3):
    # Carica il vector store FAISS
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs_simili = db.similarity_search(query, k=k)
    contesto = "\n\n".join([d.page_content for d in docs_simili])
    prompt = f"""Rispondi alla domanda: {query}\nUsa solo le informazioni dal seguente testo e indica da quale paragrafo o pagina le prendi.\n\nTesto:\n{contesto}\n"""
    llm = OllamaLLM(model="mistral")
    risposta = llm.invoke(prompt)
    print("Risposta:\n", risposta)
    print("\n---\nRiferimenti:")
    for i, d in enumerate(docs_simili, 1):
        print(f"Chunk {i}: {d.metadata}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python manual_reader.py <manuale.pdf>")
        exit(1)
    pdf_path = sys.argv[1]
    docs = load_and_split_pdf(pdf_path)
    print(f"Caricati e splittati {len(docs)} chunk dal PDF.")

    # 2️⃣ Embeddings locali
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # 3️⃣ Crea vector store
    db = FAISS.from_documents(docs, embeddings)
    db.save_local("faiss_index")
    print("Vector store FAISS salvato nella cartella 'faiss_index'.")

    if len(sys.argv) >= 3 and sys.argv[2] == "query":
        if len(sys.argv) > 3:
            query = " ".join(sys.argv[3:])
        else:
            query = input("Domanda: ")
        answer_query(query)
