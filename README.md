# Demo Agent 01

AI Agent Demo using Docker-based MCP (Model Context Protocol) for GitHub integration, built with the Strands framework.

## 🚀 Overview

This project demonstrates how to build AI agents that can interact with GitHub repositories using the Model Context Protocol (MCP). The agents can analyze repositories, create files, manage issues, pull requests, and perform various GitHub operations through a containerized MCP server.

### Key Features

- **GitHub Integration**: Full GitHub API access through MCP Docker container
- **Multiple Agent Types**: GitHub, Web Search, and AWS Bedrock agents
- **Observability**: Langfuse integration for monitoring and tracing
- **Modern Python**: Built with Python 3.10+ using `uv` for dependency management
- **Production Ready**: Includes linting, formatting, testing, and CI/CD setup

## 📁 Project Structure

```
demo-agent-01/
├── agents/                     # Individual agent implementations
│   ├── github_agent.py        # GitHub MCP integration agent
│   ├── web_search_agent.py    # Web search capabilities
│   ├── bedrock_agent.py       # AWS Bedrock integration
│   └── config_base_model.py   # Model configuration utilities
├── agent_tools/               # Reusable tools and utilities
│   ├── web_tools.py          # Web scraping and search tools
│   └── rag_tools.py          # RAG (Retrieval Augmented Generation) tools
├── .env.template             # Environment variables template
├── pyproject.toml           # Project configuration and dependencies
├── Makefile                 # Development and deployment commands
└── README.md               # This file
```

## 🛠️ Prerequisites

Before running the agents, ensure you have:

1. **Python 3.10+** installed
2. **Docker** installed and running
3. **uv** package manager (will be installed automatically if missing)
4. **GitHub Personal Access Token** with appropriate scopes

## ⚡ Quick Start

### 1. Complete Setup (Recommended)

Run the complete setup command that handles everything:

```bash
make setup
```

This will:
- Install `uv` if not present
- Install all dependencies
- Pull the GitHub MCP Docker image
- Create `.env` file from template

### 2. Configure Environment

Edit the `.env` file with your credentials:

```bash
# Required: Get your token from https://github.com/settings/tokens
# Required scopes: repo, read:org, read:user
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token_here

# Required: Contact your administrator for the AI proxy API key
AIPROXY_API_KEY=your_aiproxy_key_here

# Optional: Langfuse for observability
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
LANGFUSE_BASE_URL=https://your-langfuse-instance.com
```

### 3. Verify Setup

Check that everything is configured correctly:

```bash
make env-check
make test-mcp
```

### 4. Run Your First Agent

```bash
make run-github
```

## 🤖 Available Agents

### GitHub Agent
Interacts with GitHub repositories using MCP:
```bash
make run-github
```

**Capabilities:**
- Repository analysis
- File creation and modification
- Issue and PR management
- Branch operations
- Commit history analysis

### Web Search Agent
Performs web searches and content extraction:
```bash
make run-web
```

### AWS Bedrock Agent
Integrates with AWS Bedrock services:
```bash
make run-bedrock
```

## 🔧 Development

### Manual Setup (Alternative)

If you prefer manual setup:

```bash
# 1. Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Install dependencies
uv sync

# 3. Pull Docker image
docker pull ghcr.io/github/github-mcp-server

# 4. Setup environment
cp .env.template .env
# Edit .env with your credentials

# 5. Test the setup
uv run python -m agents.github_agent
```

### Development Environment

For development with additional tools:

```bash
make dev
```

This installs development dependencies including:
- pytest (testing)
- black (code formatting)
- isort (import sorting)
- flake8 (linting)
- mypy (type checking)
- pre-commit (git hooks)

### Code Quality

Format and lint your code:

```bash
make format  # Format with black and isort
make lint    # Lint with flake8 and mypy
make check   # Run both format and lint
```

### Testing

Run tests:

```bash
make test      # Basic tests
make test-cov  # Tests with coverage report
make test-mcp  # Test MCP connection
```

## 🐳 Docker Integration

The project uses GitHub's official MCP server Docker image:

```bash
# Pull the image
make docker-pull

# Clean old containers
make docker-clean
```

The GitHub agent automatically starts the MCP server in a Docker container when needed.

## 📊 Observability

### Langfuse Integration

The agents support Langfuse for observability and tracing. Configure in `.env`:

```bash
LANGFUSE_PUBLIC_KEY=your_public_key
LANGFUSE_SECRET_KEY=your_secret_key
LANGFUSE_BASE_URL=https://your-langfuse-instance.com
```

### Request Tracking

Add request tracking headers:

```bash
X_REQUEST_ID=your-request-id
X_FEATURE=your-feature-name
```

## 🔑 GitHub Token Setup

1. Go to [GitHub Settings > Tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select scopes:
   - `repo` (Full control of private repositories)
   - `read:org` (Read org and team membership)
   - `read:user` (Read user profile data)
4. Copy the token to your `.env` file

## 🚀 Usage Examples

### Analyzing a Repository

```python
# The GitHub agent can analyze repositories and create documentation
agent("analyze the repository https://github.com/user/repo and create a summary")
```

### Creating Files

```python
# Create or update files in repositories
agent("create a Python script that demonstrates the main functionality")
```

### Managing Issues

```python
# Work with GitHub issues and pull requests
agent("create an issue for improving the documentation with priority labels")
```

## 📋 Available Make Commands

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make setup` | Complete project setup |
| `make install` | Install dependencies |
| `make run-github` | Run GitHub agent |
| `make run-web` | Run web search agent |
| `make run-bedrock` | Run bedrock agent |
| `make test-mcp` | Test MCP connection |
| `make format` | Format code |
| `make lint` | Lint code |
| `make clean` | Clean build artifacts |
| `make info` | Show project information |

## 🔧 Configuration

### Model Configuration

Customize the AI model in `.env`:

```bash
MODEL_ID=bedrock/claude-sonnet-4  # AI model to use
MAX_TOKENS=30000                  # Maximum response tokens
TEMPERATURE=0.7                   # Response creativity (0.0-1.0)
```

### Supported Models

The system supports various models through the AI proxy:
- `bedrock/claude-sonnet-4`
- `bedrock/claude-haiku-3`
- Other models as configured in your AI proxy

## 🐛 Troubleshooting

### Common Issues

**"Docker not found" error:**
```bash
# Install Docker and ensure it's running
docker --version
```

**"GitHub token not set" error:**
```bash
# Check your .env file
make env-check
```

**"MCP connection failed" error:**
```bash
# Test the MCP connection
make test-mcp

# Pull the latest Docker image
make docker-pull
```

**Permission denied errors:**
```bash
# Ensure your GitHub token has the required scopes
# repo, read:org, read:user
```

### Debug Mode

Enable verbose logging by setting environment variables:

```bash
export STRANDS_DEBUG=1
export MCP_DEBUG=1
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting: `make check test`
5. Submit a pull request

### Development Workflow

```bash
# Setup development environment
make dev

# Make changes to code
# ...

# Format and lint
make check

# Run tests
make test

# Build package
make build
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/cx-yuval-reuveni/demo-agent-01/issues)
- **Documentation**: [Project Documentation](https://github.com/cx-yuval-reuveni/demo-agent-01/blob/main/README.md)
- **Repository**: [GitHub Repository](https://github.com/cx-yuval-reuveni/demo-agent-01)

## 🔮 What's Next?

- Add more agent types (Slack, Jira, etc.)
- Implement RAG capabilities
- Add web UI for agent interaction
- Expand testing coverage
- Add more comprehensive documentation

---

**Happy coding! 🚀**

For quick start: `make setup && make run-github`