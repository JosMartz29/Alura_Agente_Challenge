"""
app.py
Interfaz web mínima (Streamlit) para el Alura Agente.
Ejecutar:
    streamlit run app.py --server.port 8501 --server.address 0.0.0.0
"""
import os
import streamlit as st
from src.agent import CURRENT_MODEL, build_agent, ask, INDEX_DIR
from src.ingest import build_index

st.set_page_config(page_title="Alura Agente", page_icon="🤖")
st.title("🤖 Alura Agente")
st.caption("Hazme preguntas sobre el documento cargado y te responderé en lenguaje natural.")
st.markdown(f"**Modelo actual:** {CURRENT_MODEL}")

if not os.path.isdir(INDEX_DIR):
    with st.spinner("Preparando el documento por primera vez (esto tarda un poco)..."):
        build_index()

if "agent" not in st.session_state:
    with st.spinner("Cargando el agente..."):
        try:
            st.session_state.agent = build_agent()
            st.session_state.error = None
        except Exception as e:
            st.session_state.agent = None
            st.session_state.error = str(e)

if st.session_state.get("error"):
    st.error(st.session_state.error)
else:
    question = st.text_input("Escribe tu pregunta:")
    if question:
        with st.spinner("Buscando la respuesta..."):
            answer, sources = ask(st.session_state.agent, question)
        st.markdown("### Respuesta")
        st.write(answer)
        with st.expander("Ver fragmentos utilizados"):
            for i, doc in enumerate(sources, start=1):
                fname = doc.metadata.get("source_file", "documento")
                st.markdown(f"**Fragmento {i}** — _{fname}_")
                st.write(doc.page_content[:500])
