.PHONY: help install install-dev clean test lint format check docker-pull run-test run-github setup

# Default target
help: ## Show this help message
	@echo "Available targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Setup and Installation
setup: ## Complete project setup (install uv, dependencies, docker image)
	@echo "🚀 Setting up demo-agent-01..."
	@command -v uv >/dev/null 2>&1 || (echo "Installing uv..." && curl -LsSf https://astral.sh/uv/install.sh | sh)
	$(MAKE) install
	$(MAKE) docker-pull
	@echo "✅ Setup complete! Don't forget to configure your .env file."

install: ## Install dependencies using uv
	@echo "📦 Installing dependencies..."
	uv sync

install-dev: ## Install with development dependencies
	@echo "📦 Installing with dev dependencies..."
	uv sync --extra dev --extra test --extra docs

# Docker
docker-pull: ## Pull the GitHub MCP server Docker image
	@echo "🐳 Pulling GitHub MCP server Docker image..."
	docker pull ghcr.io/github/github-mcp-server

docker-clean: ## Remove old Docker containers
	@echo "🧹 Cleaning up Docker containers..."
	docker container prune -f

# Development
clean: ## Clean up build artifacts and caches
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .pytest_cache/ .coverage htmlcov/
	rm -f *.log mcp_docker.log

format: ## Format code with black and isort
	@echo "🎨 Formatting code..."
	uv run black .
	uv run isort .

lint: ## Lint code with flake8 and mypy
	@echo "🔍 Linting code..."
	uv run flake8 .
	uv run mypy agent_tools/ agents/ demo_agent/

check: format lint ## Run all code quality checks
	@echo "✅ Code quality checks complete"

# Testing
test: ## Run tests
	@echo "🧪 Running tests..."
	uv run pytest

test-cov: ## Run tests with coverage
	@echo "🧪 Running tests with coverage..."
	uv run pytest --cov --cov-report=html --cov-report=term

test-mcp: ## Test MCP Docker connection
	@echo "🧪 Testing MCP connection..."
	uv run demo-agent test-mcp

# Running
run-github: ## Run GitHub agent with test prompt
	@echo "🤖 Running GitHub agent..."
	uv run demo-agent github "Do not use any tool just say hi to confirm you are working with the GitHub MCP agent."

run-test: test-mcp ## Alias for test-mcp

# Environment
env-setup: ## Setup environment file from template
	@if [ ! -f .env ]; then \
		echo "📄 Creating .env from template..."; \
		cp .env.template .env; \
		echo "⚠️  Please edit .env and add your GitHub Personal Access Token"; \
	else \
		echo "ℹ️  .env file already exists"; \
	fi

# Build and Release
build: ## Build the package
	@echo "🏗️  Building package..."
	uv build

# Development workflow
dev: install-dev env-setup docker-pull ## Setup complete development environment
	@echo "🎯 Development environment ready!"
	@echo "Next steps:"
	@echo "1. Edit .env with your GitHub token"
	@echo "2. Run: make test-mcp"
	@echo "3. Run: make run-github"

# CI/CD targets
ci-install: ## Install dependencies for CI
	uv sync --frozen

ci-test: ## Run tests in CI environment
	uv run pytest --cov --cov-report=xml

ci-lint: ## Run linting in CI environment
	uv run black --check .
	uv run isort --check-only .
	uv run flake8 .
	uv run mypy agent_tools/ agents/ demo_agent/

# Documentation
docs-serve: ## Serve documentation locally (if using mkdocs)
	@echo "📚 Serving documentation..."
	uv run mkdocs serve

docs-build: ## Build documentation
	@echo "📚 Building documentation..."
	uv run mkdocs build

# Info
info: ## Show project information
	@echo "📋 Project Information:"
	@echo "Name: demo-agent-01"
	@echo "Description: AI Agent using Docker-based MCP for GitHub integration"
	@echo ""
	@echo "🔧 Environment:"
	@python --version
	@echo "uv version: $(shell uv --version 2>/dev/null || echo 'not installed')"
	@echo "Docker version: $(shell docker --version 2>/dev/null || echo 'not installed')"
	@echo ""
	@echo "📁 Project structure:"
	@tree -L 2 -I '.git|__pycache__|*.egg-info|.venv|venv' . 2>/dev/null || find . -maxdepth 2 -type d | grep -E '^\./[^/]*$$' | head -10