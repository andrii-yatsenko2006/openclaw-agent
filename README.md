# AI Agent (Streamlit + Ollama + ChromaDB)

This project is a local AI agent built with a ReAct architecture. It uses a local LLM via Ollama, ChromaDB as a vector database for memory/context, and Streamlit for a user-friendly web interface.

## 📋 Prerequisites
Before you begin, ensure you have the following installed on your system:
- Python 3.10 or higher
- Ollama
- Docker and Docker Compose (optional, for containerized run)

## 📦 1. Pull the Ollama Model
This project uses a local model. Make sure the Ollama application is running on your machine, open your terminal, and run the following command to download the required model:

```bash
ollama pull llama3
```

## ⚙️ 2. Environment Setup
Set up your environment variables by copying the provided example file. Create a `.env` file in the root directory and copy the contents from `.env.example`:

```bash
cp .env.example .env
```

## 🚀 3. Running the Application
You can run this project in two ways: using Docker (recommended) or locally.

⚠️ Important: For both methods, ensure the Ollama application is actively running on your system before starting the app.

### Option A: Run via Docker (Recommended)
This is the easiest way to run the app in an isolated environment.
1. Ensure Docker Desktop and Ollama are both running.

2. Open a terminal in the project directory and run:

```bash
docker-compose up --build
```

3. Once the build is complete, open your browser and go to: http://localhost:8501
4. To stop the application, press `Ctrl+C` in the terminal, then run `docker-compose down`.

### Option B: Run Locally (Without Docker)
If you prefer to run the application directly on your machine:
1. Create and activate a virtual environment:

**For Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**For Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Start the application using Streamlit:
```bash
streamlit run app.py
```

4. The web interface will automatically open in your browser at: http://localhost:8501