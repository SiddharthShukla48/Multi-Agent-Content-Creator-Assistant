# Multi Agent Content Creator Assistant

A Streamlit-based application that uses multiple AI agents (via crewAI) to automate the content creation pipeline, from topic research to script generation and media assets preparation.

## Project Overview

This project implements a content creation assistant that leverages a multi-agent system to handle different aspects of content creation:
- Topic research and selection
- Content research
- Script generation
- Media asset recommendations

The application guides users through a 5-step process, maintaining state between sessions.

## Technical Architecture

- **Frontend**: Streamlit
- **Backend**: Python with crewAI framework
- **LLM Integration**: Groq API
- **Vector Database**: ChromaDB (for embedding storage)
- **State Management**: Session-based persistence with file storage
- **Logging**: Python's built-in logging module


## Installation Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/multi-agent-content-creator-assistant.git
cd multi-agent-content-creator-assistant
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  
```

3. Install dependencies:
```bash 
pip install -r requirements.txt
```
4. Set up environment variables:
```bash
# Create a .env file or export variables directly
export GROQ_API_KEY=your_groq_api_key
```

5. Start the Streamlit application:
``` bash
python -m streamlit run app.py
```
