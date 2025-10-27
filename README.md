# Multi-Agent Content Creator Assistant

A Streamlit-based application that uses multiple AI agents powered by CrewAI and Groq to automate the complete content creation pipeline - from topic research to script generation and media asset creation.

## 🎯 Project Overview

This intelligent content creation assistant leverages a **multi-agent system** where specialized AI agents collaborate to handle different aspects of content creation:

- 🔍 **Topic Research** - Identifies trending topics in your content niche
- 📊 **Data Retrieval** - Gathers comprehensive research and information
- ✍️ **Script Writing** - Creates engaging, well-structured video scripts
- 🎨 **Media Enhancement** - Generates attention-grabbing titles and thumbnail concepts

The application guides users through a **5-step workflow**, maintaining state between sessions for seamless continuation of work.

## 🏗️ Technical Architecture

- **Frontend**: Streamlit
- **Backend**: Python with CrewAI framework
- **LLM Provider**: Groq API (via CrewAI native LLM integration)
- **Model**: `meta-llama/llama-4-scout-17b-16e-instruct`
- **Vector Database**: ChromaDB with DuckDB backend
- **State Management**: JSON-based session persistence
- **Package Manager**: uv (ultrafast Python package installer)
- **Logging**: Python's built-in logging module

## 📦 Installation Instructions

### Prerequisites
- Python 3.10 or higher
- uv package manager (recommended) or pip

### Quick Start with uv (Recommended)

1. **Install uv** (if not already installed):
```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using pip
pip install uv
```

2. **Clone the repository**:
```bash
git clone https://github.com/SiddharthShukla48/Multi-Agent-Content-Creator-Assistant.git
cd Multi-Agent-Content-Creator-Assistant
```

3. **Create virtual environment**:
```bash
# Using uv (recommended - much faster!)
uv venv --python 3.10

# Activate the environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows
```

4. **Install dependencies**:
```bash
# Using uv (10-100x faster than pip!)
uv pip install -r requirements.txt

# Or using pip
pip install -r requirements.txt
```

5. **Set up environment variables**:
```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your Groq API key
# GROQ_API_KEY=your_groq_api_key_here
```

6. **Run the application**:
```bash
# Using uv
uv run streamlit run app.py

# Or directly
streamlit run app.py

# Or using Makefile
make run
```

### Alternative: Using Makefile

```bash
# Setup everything from scratch
make setup

# Install dependencies
make install

# Run the app
make run

# Run debug interface
make debug

# Clean cache files
make clean
```
