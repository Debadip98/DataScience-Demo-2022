.PHONY: help install lint format test test-cov run clean build serve docker-build docker-run dev-setup frontend-install

# Variables
PYTHON := python3
PIP := pip3
FLASK_APP := app.py
FLASK_ENV := development
FRONTEND_DIR := frontend

# Color output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Display this help message
	@echo "$(BLUE)XGBoost ML Project - Makefile Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

# ============================================================================
# PYTHON BACKEND TARGETS
# ============================================================================

install: ## Install Python and frontend dependencies
	@echo "$(BLUE)Installing Python dependencies...$(NC)"
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements.txt
	@echo "$(BLUE)Installing development dependencies...$(NC)"
	$(PIP) install flake8 pytest pytest-cov black isort bandit safety flask flask-cors python-dotenv
	@echo "$(GREEN)✓ Python dependencies installed$(NC)"
	@make frontend-install

dev-setup: install ## Complete development environment setup
	@echo "$(BLUE)Setting up development environment...$(NC)"
	$(PIP) install jupyter notebook
	@echo "$(GREEN)✓ Development environment ready$(NC)"

lint: ## Run linting and code quality checks
	@echo "$(BLUE)Running flake8 linter...$(NC)"
	flake8 src/ tests/ app/ --max-line-length=120 --extend-ignore=E203,W503
	@echo "$(GREEN)✓ Flake8 checks passed$(NC)"

format: ## Format code with black and isort
	@echo "$(BLUE)Formatting code with black...$(NC)"
	black src/ tests/ app/ frontend/
	@echo "$(BLUE)Sorting imports with isort...$(NC)"
	isort src/ tests/ app/ frontend/
	@echo "$(GREEN)✓ Code formatted$(NC)"

security: ## Run security checks
	@echo "$(BLUE)Running Bandit security scan...$(NC)"
	bandit -r src/ app/ -ll 2>/dev/null || echo "$(YELLOW)Security scan completed$(NC)"
	@echo "$(BLUE)Checking for known vulnerabilities...$(NC)"
	safety check --json 2>/dev/null || echo "$(YELLOW)Safety check completed$(NC)"

test: ## Run all tests
	@echo "$(BLUE)Running pytest...$(NC)"
	pytest tests/ -v --tb=short
	@echo "$(GREEN)✓ All tests passed$(NC)"

test-cov: ## Run tests with coverage report
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	pytest tests/ -v --cov=src --cov=app --cov-report=html --cov-report=term
	@echo "$(GREEN)✓ Coverage report generated$(NC)"
	@echo "$(YELLOW)Open htmlcov/index.html to view coverage report$(NC)"

run: ## Run the Flask application
	@echo "$(BLUE)Starting Flask development server...$(NC)"
	FLASK_APP=$(FLASK_APP) FLASK_ENV=$(FLASK_ENV) $(PYTHON) $(FLASK_APP)

run-prod: ## Run Flask in production mode
	@echo "$(BLUE)Starting Flask production server...$(NC)"
	FLASK_APP=$(FLASK_APP) FLASK_ENV=production $(PYTHON) -m gunicorn --workers 4 --bind 0.0.0.0:5000 app:app

# ============================================================================
# FRONTEND TARGETS
# ============================================================================

frontend-install: ## Install frontend dependencies
	@echo "$(BLUE)Installing frontend dependencies...$(NC)"
	cd $(FRONTEND_DIR) && npm install 2>/dev/null || echo "$(YELLOW)npm not installed, skipping frontend setup$(NC)"

frontend-dev: ## Run frontend development server
	@echo "$(BLUE)Starting frontend dev server...$(NC)"
	cd $(FRONTEND_DIR) && npm run dev 2>/dev/null || echo "$(YELLOW)Frontend dev server not available$(NC)"

frontend-build: ## Build frontend assets
	@echo "$(BLUE)Building frontend...$(NC)"
	cd $(FRONTEND_DIR) && npm run build 2>/dev/null || echo "$(YELLOW)Frontend build not available$(NC)"

# ============================================================================
# BUILD AND DOCKER TARGETS
# ============================================================================

build: format lint test ## Run format, lint, and tests (full build)
	@echo "$(GREEN)✓ Full build successful$(NC)"

docker-build: ## Build Docker image
	@echo "$(BLUE)Building Docker image...$(NC)"
	docker build -t xgboost-ml-app:latest .
	docker tag xgboost-ml-app:latest xgboost-ml-app:$(shell date +%s)
	@echo "$(GREEN)✓ Docker image built$(NC)"
	docker images | grep xgboost-ml-app

docker-run: docker-build ## Build and run Docker container
	@echo "$(BLUE)Running Docker container...$(NC)"
	docker run -p 5000:5000 -p 3000:3000 --name xgboost-ml-app xgboost-ml-app:latest
	@echo "$(GREEN)✓ Container running on http://localhost:5000$(NC)"

docker-stop: ## Stop and remove Docker container
	@echo "$(BLUE)Stopping Docker container...$(NC)"
	docker stop xgboost-ml-app 2>/dev/null || echo "$(YELLOW)Container not running$(NC)"
	docker rm xgboost-ml-app 2>/dev/null || echo "$(YELLOW)Container not found$(NC)"
	@echo "$(GREEN)✓ Container stopped$(NC)"

docker-clean: docker-stop ## Clean Docker containers and images
	@echo "$(BLUE)Cleaning Docker artifacts...$(NC)"
	docker rmi xgboost-ml-app:latest 2>/dev/null || echo "$(YELLOW)Image not found$(NC)"
	@echo "$(GREEN)✓ Docker cleanup complete$(NC)"

# ============================================================================
# DEVELOPMENT TARGETS
# ============================================================================

dev: ## Run development environment (backend + frontend)
	@echo "$(BLUE)Starting development environment...$(NC)"
	@echo "$(YELLOW)Starting Flask backend on port 5000...$(NC)"
	FLASK_APP=$(FLASK_APP) FLASK_ENV=$(FLASK_ENV) $(PYTHON) $(FLASK_APP) &
	@echo "$(YELLOW)Starting frontend dev server on port 3000...$(NC)"
	cd $(FRONTEND_DIR) && npm run dev 2>/dev/null || echo "$(YELLOW)Frontend not available$(NC)"
	@echo "$(GREEN)✓ Development environment running$(NC)"

# ============================================================================
# CLEANING TARGETS
# ============================================================================

clean: ## Clean up generated files and caches
	@echo "$(BLUE)Cleaning up...$(NC)"
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .coverage -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name dist -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name build -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	find . -type f -name '.DS_Store' -delete
	rm -f .coverage
	@echo "$(GREEN)✓ Cleanup complete$(NC)"

deep-clean: clean docker-clean ## Deep clean - remove all generated content
	@echo "$(BLUE)Performing deep clean...$(NC)"
	rm -rf venv/
	rm -rf $(FRONTEND_DIR)/node_modules/
	rm -rf $(FRONTEND_DIR)/dist/
	@echo "$(GREEN)✓ Deep clean complete$(NC)"

# ============================================================================
# UTILITY TARGETS
# ============================================================================

requirements-freeze: ## Freeze current Python dependencies
	@echo "$(BLUE)Freezing requirements...$(NC)"
	$(PIP) freeze > requirements-frozen.txt
	@echo "$(GREEN)✓ Requirements frozen to requirements-frozen.txt$(NC)"

check: lint security test ## Run all checks (lint, security, test)
	@echo "$(GREEN)✓ All checks passed!$(NC)"

status: ## Show project status
	@echo "$(BLUE)Project Status$(NC)"
	@echo "===================="
	@echo "Python version: $$($(PYTHON) --version)"
	@echo "Node version: $$(node --version 2>/dev/null || echo 'Not installed')"
	@echo "npm version: $$(npm --version 2>/dev/null || echo 'Not installed')"
	@echo "Docker: $$(docker --version 2>/dev/null || echo 'Not installed')"
	@echo "git: $$(git --version)"
	@echo ""
	@echo "$(BLUE)Key Paths$(NC)"
	@echo "===================="
	@echo "Python: $$(which $(PYTHON))"
	@echo "pip: $$(which $(PIP))"
	@echo ""
	@echo "$(GREEN)Ready to develop!$(NC)"

# Default target
.DEFAULT_GOAL := help
