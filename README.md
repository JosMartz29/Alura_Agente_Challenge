# 🤖 Alura Agente

Agente de inteligencia artificial que responde preguntas en lenguaje natural sobre un documento interno (PDF o CSV), sin que la persona tenga que abrirlo. Proyecto final del **Challenge Alura Agente**.

## 📋 Descripción general

Cualquier persona colaboradora puede escribir una pregunta (por ejemplo: *"¿Cuál es la política de reembolsos?"*) y el agente busca la respuesta dentro del documento y la devuelve en lenguaje natural, citando los fragmentos utilizados.

**Empresa:** BimBam Buy (e-commerce). El agente responde preguntas combinando 5 documentos internos:

- Política de Reembolsos y Devoluciones
- Programa de Afiliados
- Guía de Tiempos y Costos de Envío
- Preguntas Frecuentes sobre Métodos de Pago
- Manual de Garantía de Productos

## 🏗️ Arquitectura

```
Documento (PDF/CSV)
        │
        ▼
  src/ingest.py  → divide el texto en fragmentos y genera embeddings (HuggingFace,
        │            local, sin costo) → los guarda en un índice FAISS (data/index)
        ▼
  src/agent.py   → recupera los fragmentos más relevantes para la pregunta (RAG)
        │            y se los pasa al modelo de lenguaje (Google Gemini) para
        │            generar la respuesta final
        ▼
     app.py      → interfaz web con Streamlit donde la persona escribe su pregunta
```

**Flujo (RAG — Retrieval Augmented Generation):**
1. El documento se transforma en fragmentos pequeños de texto.
2. Cada fragmento se convierte en un vector (embedding) y se guarda en un índice FAISS.
3. Cuando llega una pregunta, se buscan los fragmentos más parecidos semánticamente.
4. Esos fragmentos + la pregunta se envían al modelo de lenguaje, que redacta la respuesta final.

## 🛠️ Tecnologías utilizadas

- **Python** — lenguaje del proyecto
- **LangChain** — orquestación del agente (RAG)
- **PyPDF / pandas (CSVLoader)** — lectura de documentos
- **HuggingFace sentence-transformers** — embeddings locales y gratuitos
- **FAISS** — base de datos vectorial local
- **Cohere** — modelo de lenguaje que genera las respuestas
- **Streamlit** — interfaz web
- **OCI Compute** — despliegue en la nube

## ▶️ Cómo ejecutar el proyecto localmente

1. Clona el repositorio y entra a la carpeta:
   ```bash
   git clone <URL_DE_ESTE_REPOSITORIO>
   cd alura-agente
   ```

2. Crea un entorno virtual e instala las dependencias:
   ```bash
   python -m venv venv
   source venv/bin/activate        # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Copia `.env.example` a `.env` y coloca tu API key de Cohere
   (https://dashboard.cohere.com/signup):
   ```bash
   cp .env.example .env
   ```

4. Coloca tu documento (PDF o CSV) dentro de la carpeta `data/`.

5. Genera el índice de búsqueda (solo la primera vez o cuando cambies el documento):
   ```bash
   python src/ingest.py
   ```

6. Ejecuta la aplicación:
   ```bash
   streamlit run app.py
   ```

7. Abre el navegador en `http://localhost:8501` y empieza a preguntar.

## 💬 Ejemplos de preguntas y respuestas

| Pregunta | Respuesta del agente |
|---|---|
| ¿Cuántos días tengo para solicitar un reembolso? | [COMPLETAR: pegar la respuesta real que te dio el agente] |
| ¿Qué métodos de pago acepta BimBam Buy? | [COMPLETAR] |
| ¿Cuánto tarda el envío estándar y cuánto cuesta? | [COMPLETAR] |
| ¿Cómo funciona el programa de afiliados? | [COMPLETAR] |
| ¿Qué cubre la garantía de los productos? | [COMPLETAR] |

> Ejecuta la app, haz estas 5 preguntas (una por cada documento) y pega aquí las respuestas exactas que te dio el agente — así el evaluador ve que realmente combina las 5 fuentes.

## ☁️ Despliegue en OCI (Oracle Cloud Infrastructure)

La aplicación fue desplegada en una instancia **OCI Compute** (VM.Standard.E2.1.Micro — capa gratuita).

- **URL pública:** [COMPLETAR: http://TU_IP_PUBLICA:8501]
- **Captura de pantalla:** ver `docs/deploy-screenshot.png` (o pega aquí la imagen)

### Pasos que se siguieron para el despliegue

1. Se creó una instancia gratuita en OCI (Ubuntu, VM.Standard.E2.1.Micro).
2. Se abrió el puerto `8501` en la Security List / Network Security Group de la subred, y también con `sudo ufw allow 8501` dentro de la instancia.
3. Se instalaron Python y git en la instancia:
   ```bash
   sudo apt update && sudo apt install -y python3-pip python3-venv git
   ```
4. Se clonó el repositorio y se instalaron las dependencias (mismos pasos que en local).
5. Se colocó la API key en el archivo `.env` dentro de la instancia.
6. Se ejecutó la aplicación de forma persistente:
   ```bash
   nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &
   ```
7. Se verificó el acceso público desde el navegador usando la IP pública de la instancia.

## 📁 Estructura del repositorio

```
alura-agente/
├── app.py                # Interfaz web (Streamlit)
├── requirements.txt
├── .env.example
├── data/                  # Aquí se coloca el documento fuente (PDF/CSV)
└── src/
    ├── ingest.py          # Procesa el documento y genera el índice FAISS
    └── agent.py           # Lógica del agente (RAG + LLM)
```

## ✅ Estado del proyecto

- [x] Lectura y procesamiento del documento
- [x] Agente funcional respondiendo preguntas
- [ ] Evidencia de despliegue en OCI (agregar URL/captura antes de entregar)
