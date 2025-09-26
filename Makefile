# TEC_Q5EP Makefile
# Quick commands for development workflow

.PHONY: help dev-api dev-ui dev-all test build clean install

# Default Python executable (using virtual environment)
PYTHON := .venv/Scripts/python.exe
PIP := .venv/Scripts/pip.exe

help: ## Show this help message
	@echo "TEC_Q5EP Development Commands"
	@echo "=============================\n"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install all dependencies (Python + Node)
	$(PIP) install -r requirements.txt
	cd ui && npm install

dev-api: ## Start FastAPI development server
	$(PYTHON) -m uvicorn server.app:app --reload --host 0.0.0.0 --port 8000

dev-ui: ## Start Vite UI development server  
	cd ui && npm run dev

dev-all: ## Start both API and UI servers (requires separate terminals)
	@echo "Starting API server in background..."
	@start /B $(PYTHON) -m uvicorn server.app:app --reload --host 0.0.0.0 --port 8000
	@echo "Starting UI server..."
	@cd ui && npm run dev

test: ## Run all tests
	$(PYTHON) -m pytest server/tests/ -v

test-api: ## Run only API tests
	$(PYTHON) -m pytest server/tests/ -v

build-ui: ## Build UI for production
	cd ui && npm run build

verify: ## Verify evidence hashes
	$(PYTHON) analysis/verify_hashes.py

clean: ## Clean build artifacts
	rm -rf ui/dist/
	rm -rf .pytest_cache/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -delete

secrets: ## Load secrets from Bitwarden
	$(PYTHON) tools/secrets.py create-env
	@echo "Created .env file from Bitwarden secrets"

# Development workflow shortcuts
quick-test: ## Quick test run
	$(PYTHON) -m pytest server/tests/ -q

api-logs: ## Show API logs (if running as service)
	@echo "API should be running on http://localhost:8000"
	@echo "Check logs in the terminal where 'make dev-api' is running"

status: ## Check if services are running
	@echo "Checking API (port 8000)..."
	@powershell -Command "try { Invoke-RestMethod -Uri 'http://localhost:8000/runs' -Method GET | Select-Object -First 1 } catch { Write-Host 'API not running on port 8000' }"
	@echo "\nChecking UI (port 5173)..."  
	@powershell -Command "try { Invoke-WebRequest -Uri 'http://localhost:5173' -UseBasicParsing | Select-Object StatusCode } catch { Write-Host 'UI not running on port 5173' }"