.PHONY: install dev run debug clean test update venv sync format lint quality setup

# Install dependencies using uv
install:
	uv pip install -r requirements.txt

# Install development dependencies
dev:
	uv pip install -r requirements.txt
	uv pip install ipython pytest black ruff

# Run the application
run:
	uv run streamlit run app.py

# Run debug interface
debug:
	uv run streamlit run debug_app.py

# Clean cache and temporary files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	rm -f step_transition.txt app_debug.log

# Run tests (if you add them)
test:
	uv run pytest tests/ -v

# Update dependencies
update:
	uv pip install --upgrade -r requirements.txt
	uv pip freeze > requirements.txt

# Create virtual environment
venv:
	uv venv --python 3.10
	@echo "Virtual environment created. Activate with:"
	@echo "  source .venv/bin/activate  (macOS/Linux)"
	@echo "  .venv\\Scripts\\activate     (Windows)"

# Sync dependencies (faster than install)
sync:
	uv pip sync requirements.txt

# Format code with black
format:
	uv run black agents/ tasks/ crews/ utils/ *.py

# Lint code with ruff
lint:
	uv run ruff check agents/ tasks/ crews/ utils/ *.py

# Run all quality checks
quality: format lint
	@echo "All quality checks passed!"

# Setup project from scratch
setup: venv install
	@if [ ! -f .env ]; then cp .env.example .env; fi
	@echo "Setup complete! Edit .env with your GROQ_API_KEY"

# Show help
help:
	@echo "Available commands:"
	@echo "  make install   - Install dependencies"
	@echo "  make run       - Run the Streamlit app"
	@echo "  make debug     - Run debug interface"
	@echo "  make clean     - Clean cache files"
	@echo "  make venv      - Create virtual environment"
	@echo "  make sync      - Sync dependencies (faster)"
	@echo "  make update    - Update all dependencies"
	@echo "  make format    - Format code with black"
	@echo "  make lint      - Lint code with ruff"
	@echo "  make setup     - Setup project from scratch"
