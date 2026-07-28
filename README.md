# 🤖 Alura Agente

Agente de inteligencia artificial que responde preguntas en lenguaje natural sobre documentos internos en formato PDF o CSV. El proyecto está pensado para que cualquier persona pueda consultar información institucional sin abrir manualmente los archivos.

## 📋 Descripción general

El usuario escribe una pregunta como “¿Cuál es la política de reembolsos?” y el agente busca la respuesta en los documentos cargados, recupera los fragmentos más relevantes y devuelve una respuesta en lenguaje natural.

**Empresa:** BimBam Buy. El sistema está preparado para responder sobre documentos como:

- Política de Reembolsos y Devoluciones
- Programa de Afiliados
- Guía de Tiempos y Costos de Envío
- Preguntas Frecuentes sobre Métodos de Pago
- Manual de Garantía de Productos

## 🏗️ Arquitectura

```text
Documento (PDF/CSV)
        │
        ▼
  src/ingest.py  → divide el contenido en fragmentos y genera embeddings locales
        │            con HuggingFace y los guarda en un índice FAISS en data/index
        ▼
  src/agent.py   → recupera los fragmentos más relevantes para la pregunta (RAG)
        │            y los envía al modelo de lenguaje de Cohere para generar la respuesta
        ▼
     app.py      → interfaz web con Streamlit
```

**Flujo RAG:**
1. El documento se divide en fragmentos pequeños.
2. Cada fragmento se convierte en un embedding y se guarda en FAISS.
3. Cuando llega una pregunta, el sistema recupera los fragmentos más similares.
4. Esos fragmentos se envían al modelo junto con la pregunta para producir la respuesta final.

## 🛠️ Tecnologías utilizadas

- Python
- Streamlit
- LangChain
- LangChain Community
- HuggingFace sentence-transformers
- FAISS
- Cohere
- PyPDF / CSVLoader

## ▶️ Cómo ejecutar el proyecto localmente

1. Clona el repositorio y entra a la carpeta:
   ```bash
   git clone <URL_DE_ESTE_REPOSITORIO>
   cd alura-agente
   ```

2. Crea un entorno virtual e instala las dependencias:
   ```bash
   python -m venv .venv
   source .venv/bin/activate      # En Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Copia el archivo de ejemplo a `.env` y agrega tu API key de Cohere:
   ```bash
   cp .env.example .env
   ```

4. Coloca tus documentos en la carpeta `data/`.

5. Ejecuta la aplicación:
   ```bash
   streamlit run app.py
   ```

6. Abre `http://localhost:8501` y empieza a preguntar.

> El índice FAISS se construye automáticamente al iniciar la app si aún no existe.

## ☁️ Despliegue en Streamlit Community Cloud

La aplicación está preparada para desplegarse de forma gratuita en Streamlit Community Cloud.

### Pasos recomendados

1. Sube este repositorio a GitHub.
2. Crea una nueva app en Streamlit Community Cloud y selecciona este repositorio.
3. Define el archivo principal como `app.py`.
4. Agrega los secretos en la sección de Secrets:
   - `COHERE_API_KEY`
   - `COHERE_MODEL` (opcional, por ejemplo `command-xlarge-nightly`)

La app podrá leer esos valores desde `.env` en local o desde `st.secrets` en la nube.

## 📁 Estructura del repositorio

```text
alura-agente/
├── app.py                # Interfaz web (Streamlit)
├── requirements.txt
├── .env.example
├── data/                 # Documentos fuente (PDF/CSV)
└── src/
    ├── ingest.py         # Procesa documentos y genera el índice FAISS
    └── agent.py          # Lógica del agente (RAG + LLM)
```

## ✅ Estado del proyecto

- [x] Lectura y procesamiento de documentos
- [x] Agente funcional respondiendo preguntas
- [x] Preparado para despliegue en Streamlit Community Cloud
