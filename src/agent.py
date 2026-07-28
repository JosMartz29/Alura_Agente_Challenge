"""
agent.py
Construye el agente de preguntas y respuestas (RAG):
1. Carga el índice FAISS generado por ingest.py
2. Recupera los fragmentos más relevantes para la pregunta del usuario
3. Le pide al modelo de lenguaje (Google Gemini) que responda usando esos fragmentos
"""
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

try:
    from langchain.chains import RetrievalQA
except Exception:  # pragma: no cover - fallback para versiones de LangChain sin esa exportación
    RetrievalQA = None

load_dotenv()

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
INDEX_DIR = os.path.join(DATA_DIR, "index")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")


def build_agent():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "Falta la variable de entorno GOOGLE_API_KEY. "
            "Consigue una gratis en https://aistudio.google.com/app/apikey "
            "y colócala en un archivo .env (ver .env.example)."
        )

    if not os.path.isdir(INDEX_DIR):
        raise FileNotFoundError(
            "No se encontró el índice en /data/index. Ejecuta primero: python src/ingest.py"
        )

    if RetrievalQA is None:
        raise ImportError("La versión instalada de LangChain no expone RetrievalQA de forma compatible.")

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local(
        INDEX_DIR, embeddings, allow_dangerous_deserialization=True
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL, google_api_key=api_key, temperature=0.2)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
    )
    return qa_chain


def ask(agent, question: str):
    try:
        result = agent.invoke({"query": question})
        answer = result["result"]
        sources = result.get("source_documents", [])
        return answer, sources
    except Exception as exc:
        error_message = str(exc).lower()
        if "quota" in error_message or "resource exhausted" in error_message or "429" in error_message:
            return (
                "No pude completar la respuesta porque la API de Gemini excedió su cuota o límite de solicitudes. "
                "Prueba de nuevo más tarde o revisa la configuración de la API.",
                [],
            )
        raise
