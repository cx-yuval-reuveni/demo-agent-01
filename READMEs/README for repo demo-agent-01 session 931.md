# Demo Agent 01 - GitHub MCP Integration

> AI Agent Demo using Docker-based MCP for GitHub integration

## Overview

This project demonstrates an AI agent system that integrates with GitHub through the Model Control Protocol (MCP). The agent can analyze repositories, create documentation, and interact with GitHub APIs using both manual and managed MCP configurations.

## Features

- 🤖 **GitHub Agent**: Analyze repositories, create documentation, interact with GitHub APIs
- 🌐 **Web Search Agent**: Web scraping and search capabilities  
- ☁️ **Bedrock Agent**: AWS Bedrock integration
- 🔧 **MCP Integration**: Docker-based GitHub MCP server
- 📊 **Observability**: Langfuse integration for monitoring and tracing
- 🛠️ **Development Tools**: Comprehensive testing, linting, and formatting

## Prerequisites

- **Python 3.10+**
- **Docker** (for GitHub MCP server)
- **uv** package manager (will be installed automatically)
- **GitHub Personal Access Token** with `repo`, `read:org`, `read:user` scopes
- **AI Proxy API Key** (contact your administrator)

## Quick Setup

### 1. Complete Setup (Recommended)
```bash
make setup
```
This will:
- Install `uv` if not present
- Install all dependencies
- Pull the GitHub MCP Docker image
- Create `.env` from template

### 2. Manual Setup
```bash
# Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Pull Docker image
docker pull ghcr.io/github/github-mcp-server

# Setup environment
cp .env.template .env
```

## Environment Variables

Create and configure your `.env` file:

```bash
# Required - GitHub Integration
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token_here

# Required - AI Model Access  
AIPROXY_API_KEY=your_aiproxy_key_here

# Optional - Langfuse Observability
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
LANGFUSE_BASE_URL=https://your-langfuse-instance.com

# Optional - Model Configuration
MODEL_ID=bedrock/claude-sonnet-4
MAX_TOKENS=30000
TEMPERATURE=0.7

# Optional - Request Tracking
X_REQUEST_ID=demo-request-strands-123
X_FEATURE=yuval-demo-strands
```

### Getting Your GitHub Token

1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `read:org`, `read:user`
4. Copy the token to your `.env` file

### Verify Environment Setup
```bash
make env-check
```

## Running the GitHub Agent

### Basic Test (Recommended First Run)
```bash
make run-github
# or
make test-mcp
```
This runs a simple agent test without MCP tools to verify basic functionality.

### Full GitHub MCP Agent
```bash
make run-github-mcp
# or
uv run python -m agents.github_agent
```
This runs the full GitHub agent with MCP tools (may have Docker connection issues in some environments).

### Other Agents
```bash
# Web search agent
make run-web

# AWS Bedrock agent  
make run-bedrock

# See all available agents
make run-agents
```

## GitHub MCP Usage

### Manual vs Managed MCP

**Manual MCP (Current Implementation):**
- Uses Docker container: `ghcr.io/github/github-mcp-server`
- Requires Docker to be running
- Agent manages MCP client lifecycle
- More control but requires Docker setup

**Managed MCP (Alternative):**
- Could use hosted MCP services
- Less setup required
- May have different authentication flows
- Currently not implemented in this demo

### MCP Architecture

```
Agent → MCPClient → Docker Container → GitHub API
```

1. **Agent**: Uses Strands framework with MCP tools
2. **MCPClient**: Manages communication with MCP server
3. **Docker Container**: Runs GitHub MCP server
4. **GitHub API**: Actual GitHub integration

## Troubleshooting

### Network Errors

**Docker Connection Issues:**
```bash
# Check if Docker is running
docker ps

# Test Docker image manually
docker run -it --rm -e GITHUB_PERSONAL_ACCESS_TOKEN=your_token ghcr.io/github/github-mcp-server

# Clean up containers
make docker-clean
```

**MCP Connection Failures:**
- Ensure Docker daemon is running
- Check that GitHub token has correct scopes
- Verify network connectivity
- Try running basic test first: `make run-github`

**Environment Issues:**
```bash
# Check environment variables
make env-check

# Recreate environment file
rm .env && make env-setup
```

**Permission Errors:**
- Ensure GitHub token has required scopes
- Check repository access permissions
- Verify token hasn't expired

### Common Error Messages

| Error | Solution |
|-------|----------|
| `GITHUB_PERSONAL_ACCESS_TOKEN environment variable is required` | Add token to `.env` file |
| `Docker daemon not running` | Start Docker service |
| `Permission denied` | Check GitHub token scopes |
| `Network timeout` | Check internet connection, try different network |
| `Module not found` | Run `uv sync` to install dependencies |

### Debug Mode

Enable verbose logging:
```bash
# Set debug environment
export DEBUG=1

# Run with more detailed output
uv run python -m agents.github_agent --verbose
```

## Development

### Development Setup
```bash
make dev
```

### Code Quality
```bash
# Format code
make format

# Lint code  
make lint

# Run all checks
make check
```

### Testing
```bash
# Basic tests
make test

# Test with coverage
make test-cov

# Test MCP connection
make test-mcp-docker
```

### Project Structure

```
demo-agent-01/
├── agents/                 # Agent implementations
│   ├── github_agent.py    # Main GitHub MCP agent
│   ├── web_search_agent.py # Web search capabilities
│   └── bedrock_agent.py   # AWS Bedrock integration
├── agent_tools/           # Reusable tools
│   ├── web_tools.py      # Web scraping utilities
│   └── rag_tools.py      # RAG implementations
├── READMEs/              # Documentation
├── .env.template         # Environment template
├── Makefile             # Development commands
└── pyproject.toml       # Project configuration
```

## Available Make Commands

| Command | Description |
|---------|-------------|
| `make setup` | Complete project setup |
| `make install` | Install dependencies |
| `make run-github` | Run basic GitHub agent test |
| `make run-github-mcp` | Run full GitHub MCP agent |
| `make test-mcp` | Test MCP connection |
| `make env-check` | Verify environment setup |
| `make docker-pull` | Pull GitHub MCP Docker image |
| `make clean` | Clean build artifacts |
| `make help` | Show all available commands |

## Examples

### Analyze a Repository
The GitHub agent can analyze repositories and create documentation:

```python
# The agent will:
# 1. List important files in the repository
# 2. Summarize their purpose  
# 3. Create comprehensive documentation
# 4. Save files to specified locations
```

### Basic Agent Usage
```python
from strands import Agent
from agents.config_base_model import get_base_model

model = get_base_model(max_tokens=1000)
agent = Agent(model=model, system_prompt="You are helpful assistant.")
result = agent("Hello!")
```

## Dependencies

### Core Dependencies
- `strands-agents>=1.8.0` - Agent framework
- `strands-agents-tools>=0.2.7` - Agent tooling
- `mcp==1.13.1` - Model Control Protocol
- `python-dotenv` - Environment management
- `openai` - AI model integration

### Development Dependencies
- `pytest` - Testing framework
- `black` - Code formatting
- `isort` - Import sorting
- `flake8` - Linting
- `mypy` - Type checking

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the [GitHub Issues](https://github.com/cx-yuval-reuveni/demo-agent-01/issues)
3. Run `make info` for system information
4. Try the basic test first: `make run-github`

---

**Quick Start Summary:**
```bash
git clone https://github.com/cx-yuval-reuveni/demo-agent-01
cd demo-agent-01
make setup
# Edit .env with your GitHub token
make env-check  
make run-github
```