"""
agent.py
Construye el agente de preguntas y respuestas (RAG):
1. Carga el índice FAISS generado por ingest.py
2. Recupera los fragmentos más relevantes para la pregunta del usuario
3. Le pide al modelo de lenguaje (Cohere Chat) que responda usando esos fragmentos
"""
import os
from typing import Any, Dict
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_cohere import ChatCohere

try:
    from langchain.chains import RetrievalQA
except Exception:  # pragma: no cover - fallback para versiones de LangChain sin esa exportación
    RetrievalQA = None

load_dotenv()

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
INDEX_DIR = os.path.join(DATA_DIR, "index")
COHERE_MODEL = None
CURRENT_MODEL = "Cohere Chat"


def _get_secret(name, default=None):
    """Busca la variable primero en el entorno, luego en Streamlit secrets."""
    value = os.getenv(name)
    if value:
        return value

    try:
        import streamlit as st
    except Exception:
        st = None

    if st is not None:
        try:
            secrets = st.secrets
            if hasattr(secrets, "get"):
                value = secrets.get(name, default)
            elif isinstance(secrets, dict):
                value = secrets.get(name, default)
            else:
                value = getattr(secrets, name, default)
            if value:
                return value
        except Exception:
            pass

    return default


class SafeChatCohere(ChatCohere):
    def _get_generation_info(self, response: Any) -> Dict[str, Any]:
        info = {}
        if hasattr(response, "documents"):
            info["documents"] = response.documents
        if hasattr(response, "citations"):
            info["citations"] = response.citations
        if hasattr(response, "search_results"):
            info["search_results"] = response.search_results
        if hasattr(response, "search_queries"):
            info["search_queries"] = response.search_queries
        if hasattr(response, "token_count"):
            info["token_count"] = response.token_count
        elif getattr(response, "meta", None) is not None:
            tokens = getattr(response.meta, "tokens", None)
            if tokens is not None:
                input_tokens = getattr(tokens, "input_tokens", None)
                output_tokens = getattr(tokens, "output_tokens", None)
                if input_tokens is not None and output_tokens is not None:
                    info["token_count"] = input_tokens + output_tokens
        return info


def build_agent():
    api_key = _get_secret("COHERE_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "Falta la variable COHERE_API_KEY. "
            "En local agrégala en .env; en Streamlit Cloud en Secrets con formato TOML: "
            "[secrets] COHERE_API_KEY = 'tu_key'"
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

    model_name = _get_secret("COHERE_MODEL", "command-a-03-2025")
    global COHERE_MODEL
    COHERE_MODEL = model_name
    CURRENT_MODEL = f"Cohere Chat ({model_name})"

    llm = SafeChatCohere(model=model_name, cohere_api_key=api_key, temperature=0.2)

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
                "No pude completar la respuesta porque la API excedió su cuota o límite de solicitudes. "
                "Prueba de nuevo más tarde o revisa la configuración de la API.",
                [],
            )
        raise
