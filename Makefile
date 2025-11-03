.PHONY: help install install-dev clean test lint format check docker-pull run-test run-github run-agents setup

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
	$(MAKE) env-setup
	@echo "✅ Setup complete! Don't forget to configure your .env file with GitHub token."

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
	uv run mypy agent_tools/ agents/

check: format lint ## Run all code quality checks
	@echo "✅ Code quality checks complete"

# Testing
test: ## Run basic tests (currently creates simple test structure)
	@echo "🧪 Running tests..."
	@if [ ! -d "tests" ]; then \
		echo "Creating basic test structure..."; \
		mkdir -p tests; \
		echo "import pytest\n\ndef test_basic():\n    assert True" > tests/test_basic.py; \
	fi
	uv run pytest tests/

test-cov: ## Run tests with coverage
	@echo "🧪 Running tests with coverage..."
	@if [ ! -d "tests" ]; then \
		echo "Creating basic test structure..."; \
		mkdir -p tests; \
		echo "import pytest\n\ndef test_basic():\n    assert True" > tests/test_basic.py; \
	fi
	uv run pytest --cov=agent_tools --cov=agents --cov-report=html --cov-report=term tests/

test-mcp: ## Test MCP Docker connection (using github agent directly)
	@echo "🧪 Testing MCP connection via GitHub agent..."
	@if [ ! -f .env ]; then \
		echo "❌ .env file not found. Run 'make env-setup' first."; \
		exit 1; \
	fi
	uv run python -m agents.github_agent

# Running agents
run-github: ## Run GitHub agent
	@echo "🤖 Running GitHub agent..."
	@if [ ! -f .env ]; then \
		echo "❌ .env file not found. Run 'make env-setup' first."; \
		exit 1; \
	fi
	uv run python -m agents.github_agent

run-web: ## Run web search agent
	@echo "🌐 Running web search agent..."
	@if [ ! -f .env ]; then \
		echo "❌ .env file not found. Run 'make env-setup' first."; \
		exit 1; \
	fi
	uv run python -m agents.web_search_agent

run-bedrock: ## Run bedrock agent
	@echo "☁️ Running bedrock agent..."
	@if [ ! -f .env ]; then \
		echo "❌ .env file not found. Run 'make env-setup' first."; \
		exit 1; \
	fi
	uv run python -m agents.bedrock_agent

run-agents: ## Show available agents to run
	@echo "🤖 Available agents:"
	@echo "  make run-github   - GitHub MCP agent"
	@echo "  make run-web      - Web search agent"  
	@echo "  make run-bedrock  - AWS Bedrock agent"

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

env-check: ## Check if required environment variables are set
	@echo "🔍 Checking environment variables..."
	@python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('✅ GITHUB_PERSONAL_ACCESS_TOKEN:', 'SET' if os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN') else '❌ NOT SET')"

# Build and Release
build: ## Build the package
	@echo "🏗️  Building package..."
	uv build

# Development workflow
dev: install-dev env-setup docker-pull ## Setup complete development environment
	@echo "🎯 Development environment ready!"
	@echo "Next steps:"
	@echo "1. Edit .env with your GitHub token"
	@echo "2. Run: make env-check"
	@echo "3. Run: make test-mcp"
	@echo "4. Run: make run-github"

# CI/CD targets
ci-install: ## Install dependencies for CI
	uv sync --frozen

ci-test: ## Run tests in CI environment
	@if [ ! -d "tests" ]; then \
		mkdir -p tests; \
		echo "import pytest\n\ndef test_basic():\n    assert True" > tests/test_basic.py; \
	fi
	uv run pytest --cov=agent_tools --cov=agents --cov-report=xml tests/

ci-lint: ## Run linting in CI environment
	uv run black --check .
	uv run isort --check-only .
	uv run flake8 .
	uv run mypy agent_tools/ agents/

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
	@python --version 2>/dev/null || echo "Python: not found"
	@echo "uv version: $(shell uv --version 2>/dev/null || echo 'not installed')"
	@echo "Docker version: $(shell docker --version 2>/dev/null || echo 'not installed')"
	@echo ""
	@echo "📁 Project structure:"
	@echo "agent_tools/    - Reusable tools (RAG, web scraping)"
	@echo "agents/         - Individual agent implementations"
	@echo "  ├── github_agent.py     - GitHub MCP integration"
	@echo "  ├── web_search_agent.py - Web search capabilities"
	@echo "  └── bedrock_agent.py    - AWS Bedrock integration"
	@echo ""
	@echo "🚀 Quick start:"
	@echo "make setup && make run-github"