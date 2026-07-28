"""
ingest.py
Lee un documento (PDF o CSV) desde la carpeta /data, lo divide en fragmentos,
genera embeddings locales (sin costo, sin API key) y guarda un índice FAISS
en /data/index para que el agente pueda buscar en él rápidamente.

Uso:
    python src/ingest.py
"""
import os
import glob
from langchain_community.document_loaders import PyPDFLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
INDEX_DIR = os.path.join(DATA_DIR, "index")


def find_source_documents():
    """Busca todos los PDF o CSV dentro de /data (ignorando la carpeta index)."""
    candidates = []
    for ext in ("*.pdf", "*.csv"):
        candidates.extend(glob.glob(os.path.join(DATA_DIR, ext)))
    if not candidates:
        raise FileNotFoundError(
            "No se encontró ningún archivo .pdf o .csv dentro de la carpeta /data. "
            "Coloca tus documentos allí antes de ejecutar este script."
        )
    return sorted(candidates)


def load_document(path):
    if path.lower().endswith(".pdf"):
        loader = PyPDFLoader(path)
    else:
        loader = CSVLoader(path, encoding="utf-8")
    documents = loader.load()
    # Guardamos el nombre del archivo en los metadatos de cada fragmento,
    # así el agente puede indicar de qué documento sacó cada respuesta.
    filename = os.path.basename(path)
    for doc in documents:
        doc.metadata["source_file"] = filename
    return documents


def main():
    source_paths = find_source_documents()
    print(f"Documentos encontrados ({len(source_paths)}):")
    for p in source_paths:
        print(f"  - {os.path.basename(p)}")

    documents = []
    for path in source_paths:
        docs = load_document(path)
        documents.extend(docs)
    print(f"Páginas/filas cargadas en total: {len(documents)}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(documents)
    print(f"Fragmentos generados: {len(chunks)}")

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    os.makedirs(INDEX_DIR, exist_ok=True)
    vectorstore.save_local(INDEX_DIR)
    print(f"Índice FAISS guardado en: {INDEX_DIR}")


if __name__ == "__main__":
    main()
