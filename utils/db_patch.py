import os

# Set environment variables to change ChromaDB's behavior
os.environ["LANGCHAIN_TRACING_V2"] = "false"  # Disable LangChain tracing
os.environ["CHROMA_DB_IMPL"] = "duckdb+parquet"  # Use DuckDB instead of SQLite

# Alternative: disable persistence
os.environ["CHROMADB_CLIENT_SETTINGS_PERSIST_DIRECTORY"] = ""