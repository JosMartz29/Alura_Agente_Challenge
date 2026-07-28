# 🤖 Alura Agente

<img width="1833" height="682" alt="image" src="https://github.com/user-attachments/assets/d57afb52-5095-44b1-9b45-ab5712c2ebd1" />

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

## 💬 Ejemplos de preguntas y respuestas

| Pregunta | Respuesta del agente |
|---|---|
| ¿Cuántos días tengo para solicitar una devolución por retracto? | 10 días corridos posteriores a la recepción del pedido, siempre que el producto cumpla los requisitos de elegibilidad (sin uso, completo, con empaque original cuando corresponda). |
| ¿Qué cubre la garantía de los productos y qué la excluye? | Cubre fallas de fabricación, materiales o ensamblaje en condiciones normales de uso (falla de encendido, mal funcionamiento, defectos visibles al primer uso). No cubre daños por golpes o caídas, humedad o fuego, manipulación por terceros no autorizados, desgaste normal ni alteración de seriales. |
| ¿Cuánto tarda en procesarse un reembolso y a qué medio de pago vuelve? | Entre 5 y 10 días hábiles desde la aprobación, dependiendo del método de pago y el país. El reembolso vuelve al mismo medio de pago original, salvo imposibilidad técnica o regulatoria. |
| ¿Qué pasa con la comisión de un afiliado si el pedido que generó la venta termina en devolución? | La comisión puede ajustarse o reversarse según la política interna de BimBam Buy y la elegibilidad final de la venta, ya que el Programa de Afiliados está directamente vinculado a la Política de Reembolsos y Devoluciones. |

> Ejecuta la app, haz estas 5 preguntas (una por cada documento) y pega aquí las respuestas exactas que te dio el agente — así el evaluador ve que realmente combina las 5 fuentes.

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
   - `COHERE_MODEL` (opcional, por ejemplo `command-a-03-2025`)

La app podrá leer esos valores desde `.env` en local o desde `st.secrets` en la nube, incluyendo el modelo de Cohere que se usará para responder.

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
