# Tidy Swarm

An autonomous, fully offline, multi-agent data preprocessing pipeline powered by local models running via **Ollama** and orchestrated using **LangGraph**.

`Tidy Swarm` takes messy, real-world CSV files and automatically audits, writes cleaning code for, and executes data transformations all on your local GPU.


## 🏗️ System Architecture
### System Architecture

```mermaid
graph TD
    CSV[("📂 raw_messy_data.csv")] --> Profiler["📊 Dataset Profiler"]
    Profiler --> State["💾 SwarmState (Memory DataFrame)"]

    subgraph Swarm ["🧼 Tidy Swarm State Machine"]
        State --> Node1["🔍 Node 1: Auditor Agent (Qwen 2.5)"]
        Node1 -->|"Audit Report"| Node2["⚙️ Node 2: Engineer Agent (Llama 3.2)"]
        Node2 -->|"Pandas Code"| Node3["🚀 Node 3: Python Executor"]
        Node3 --> Router{"Status Check"}
    end

    Router -->|"Success"| Output[("✅ raw_messy_data_cleaned.csv")]
    Router -->|"Runtime Error"| Node1
```

## ⚙️ Hardware & Stack Requirements
- Package & Env Management: uv
- Local LLM Engine: Ollama
- Target GPU: Optimized for GPUs with ≥8GB VRAM (e.g., RTX 4060).


## 🚀 Quickstart
### 1. Model Setup
Pull the recommended models via Ollama:

```shell
# Auditor Agent (Specialized in code logic & schema reasoning)
ollama pull qwen2.5:7b

# Engineer Agent (Ultra-fast code generation)
ollama pull llama3.2:3b
```

### 2. Environment Setup
Clone the repository and install all dependencies using uv:
```
uv sync
```

### 3. Run the Agentic Swarm Pipeline
```
uv run python -m src.main
```


## 🛠️ Configuration
All pipeline variables can be adjusted in src/config.py:

```{python}
AUDITOR_MODEL = "qwen2.5:7b"
ENGINEER_MODEL = "llama3.2:3b"
OLLAMA_TEMPERATURE = 0.0
MAX_RETRIES = 3
```