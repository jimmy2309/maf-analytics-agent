# MAF Analytics Agent (The Brain)

This repository is part of the **MAF Enterprise Distributed Architecture**. It serves as the intelligent core (The Brain) for all analytics-related queries.

## 🧠 Role in Architecture
- **No Local Tools:** This agent does not execute database queries or run Python code locally.
- **MCP Integration:** It fetches available tools and requests execution through the central `maf-mcp-server`.
- **Dynamic Prompts:** Its system prompt is not hardcoded; it is loaded directly from the database at runtime.

---

## 🛠️ Setup Instructions

### 1. Prerequisites (Virtual Environment)
It is highly recommended to use a Python virtual environment.
```bash
# Create a virtual environment
python -m venv venv

# Activate it (Windows)
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Variables
Ensure a `.env` file exists in the root of this repository:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/maf_poc
OLLAMA_API_BASE=http://localhost:11434/v1
MCP_SERVER_URL=http://localhost:8002
```

### 3. Running the Server
Start the FastAPI server on port **8001**:
```bash
uvicorn src.main:app --port 8001 --reload
```

---

## 📁 Directory Structure (Ultra-Clean)
- `logs/` - Dynamic daily logs (auto-generated)
- `src/core/settings.py` - Strict Environment configurations
- `src/db/` - DB Models (AgentConfig) and Session logic
- `src/modules/agent/services.py` - Agent logic integrating with Ollama and MCP
- `src/main.py` - FastAPI Entry Point
