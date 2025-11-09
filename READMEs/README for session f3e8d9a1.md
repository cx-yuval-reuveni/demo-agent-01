# Demo Agent 01 - AI Agent with GitHub Integration

> **Session ID: f3e8d9a1**

An AI agent demonstration project that showcases Docker-based MCP (Model Context Protocol) integration with GitHub, featuring multiple specialized agents for different tasks.

## 🚀 Quick Start

```bash
# Complete setup in one command
make setup

# Configure your environment
# Edit .env with your GitHub token and AI proxy key

# Test the connection
make test-mcp

# Run the GitHub agent
make run-github
```

## 📋 Overview

This project demonstrates how to build AI agents using the Strands framework with MCP (Model Context Protocol) for seamless integration with external services. The main focus is on GitHub integration through Docker-containerized MCP servers.

### Key Features

- **Docker-based MCP Integration**: Uses GitHub's official MCP server in a Docker container
- **Multiple Agent Types**: GitHub, Web Search, and AWS Bedrock agents
- **Observability**: Langfuse integration for tracing and monitoring
- **Modern Python**: Built with Python 3.10+ using `uv` for dependency management
- **Development Tools**: Complete CI/CD setup with testing, linting, and formatting

## 🏗️ Architecture

```
demo-agent-01/
├── agents/                 # Individual agent implementations
│   ├── github_agent.py    # GitHub MCP integration agent
│   ├── web_search_agent.py # Web search capabilities
│   ├── bedrock_agent.py   # AWS Bedrock integration
│   └── config_base_model.py # Shared model configuration
├── agent_tools/           # Reusable tools and utilities
│   ├── rag_tools.py       # RAG (Retrieval Augmented Generation)
│   └── web_tools.py       # Web scraping utilities
└── pyproject.toml         # Project configuration and dependencies
```

## 🛠️ Prerequisites

### Required Software

1. **Python 3.10+**
   ```bash
   python --version  # Should be 3.10 or higher
   ```

2. **uv** (Python package manager)
   ```bash
   # Install uv if not already installed
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Docker**
   ```bash
   docker --version  # Required for MCP server
   ```

### Required Accounts & Tokens

1. **GitHub Personal Access Token**
   - Go to [GitHub Settings > Tokens](https://github.com/settings/tokens)
   - Create a new token with scopes: `repo`, `read:org`, `read:user`
   - Save the token (starts with `ghp_`)

2. **AI Proxy API Key**
   - Contact your administrator for the AI proxy API key
   - This provides access to the language models

3. **Langfuse (Optional)**
   - For observability and tracing
   - Sign up at [Langfuse](https://langfuse.com) or use your organization's instance

## 📦 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/cx-yuval-reuveni/demo-agent-01.git
cd demo-agent-01
```

### 2. Complete Setup

```bash
# This will install uv, dependencies, pull Docker image, and create .env
make setup
```

### 3. Configure Environment

Edit the `.env` file with your credentials:

```bash
# Required
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token_here
AIPROXY_API_KEY=your_aiproxy_key_here

# Optional (for observability)
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
LANGFUSE_BASE_URL=https://your-langfuse-instance.com

# Optional (model configuration)
MODEL_ID=bedrock/claude-sonnet-4
MAX_TOKENS=30000
TEMPERATURE=0.7
```

### 4. Verify Setup

```bash
# Check environment variables
make env-check

# Test MCP connection
make test-mcp
```

## 🤖 Running the Agents

### GitHub Agent

The main agent that can interact with GitHub repositories:

```bash
make run-github
```

This agent can:
- Analyze repositories
- Create and modify files
- Manage issues and pull requests
- Search code and repositories
- Generate documentation

### Web Search Agent

For web research and information gathering:

```bash
make run-web
```

### AWS Bedrock Agent

For AWS Bedrock model integration:

```bash
make run-bedrock
```

### View All Available Agents

```bash
make run-agents
```

## 🔧 Development

### Development Environment Setup

```bash
# Setup complete development environment
make dev
```

This will:
- Install development dependencies
- Setup environment files
- Pull Docker images
- Configure pre-commit hooks

### Code Quality

```bash
# Format code
make format

# Run linting
make lint

# Run all quality checks
make check
```

### Testing

```bash
# Run basic tests
make test

# Run tests with coverage
make test-cov

# Test MCP connection
make test-mcp
```

### Build Package

```bash
make build
```

## 📚 Usage Examples

### Example 1: Repository Analysis

The GitHub agent can analyze repositories and generate documentation:

```python
# This is what the agent does when you run `make run-github`
result = agent("analyze the repository https://github.com/cx-yuval-reuveni/demo-agent-01 and create readme.md file")
```

### Example 2: Custom Agent Usage

```python
import asyncio
from agents.github_agent import main

# Run the GitHub agent programmatically
asyncio.run(main())
```

### Example 3: Direct MCP Integration

```python
from mcp import StdioServerParameters, stdio_client
from strands.tools.mcp import MCPClient

# Setup GitHub MCP client
github_mcp_client = MCPClient(lambda: stdio_client(github_server_params()))
```

## 🔍 Troubleshooting

### Common Issues

1. **Docker Permission Denied**
   ```bash
   sudo usermod -aG docker $USER
   # Then logout and login again
   ```

2. **GitHub Token Issues**
   ```bash
   # Verify your token has the right scopes
   curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user
   ```

3. **uv Not Found**
   ```bash
   # Add uv to PATH or reinstall
   curl -LsSf https://astral.sh/uv/install.sh | sh
   source ~/.bashrc
   ```

4. **Docker Image Pull Fails**
   ```bash
   # Manually pull the image
   docker pull ghcr.io/github/github-mcp-server
   ```

### Debug Mode

Enable debug logging by setting:

```bash
export DEBUG=1
```

### Logs

Check the logs in:
- `mcp_docker.log` - MCP Docker container logs
- Console output for agent interactions

## 🚀 Advanced Usage

### Custom Model Configuration

Modify `agents/config_base_model.py` to use different models:

```python
def get_base_model(max_tokens=30000):
    return YourCustomModel(
        api_key=os.getenv("YOUR_API_KEY"),
        model_id="your-model-id",
        max_tokens=max_tokens
    )
```

### Adding New Tools

Create new tools in `agent_tools/`:

```python
# agent_tools/my_tool.py
def my_custom_tool():
    """Your custom tool implementation"""
    pass
```

### Extending Agents

Create new agents in `agents/`:

```python
# agents/my_agent.py
from strands import Agent
from .config_base_model import get_base_model

async def main():
    model = get_base_model()
    agent = Agent(
        model=model,
        system_prompt="Your custom system prompt",
        tools=[your_tools]
    )
    result = agent("Your prompt")
```

## 📊 Monitoring & Observability

### Langfuse Integration

When properly configured, the agents automatically send traces to Langfuse:

- **Session Tracking**: Each run gets a unique session ID
- **Tool Usage**: All MCP tool calls are tracked
- **Performance Metrics**: Response times and token usage
- **Error Tracking**: Failures and exceptions

### Viewing Traces

1. Go to your Langfuse dashboard
2. Look for sessions with ID pattern: `first-github-agent-session-{random_number}`
3. Drill down into individual tool calls and responses

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run quality checks: `make check`
5. Run tests: `make test`
6. Commit and push your changes
7. Create a pull request

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/cx-yuval-reuveni/demo-agent-01/issues)
- **Documentation**: [Project Documentation](https://github.com/cx-yuval-reuveni/demo-agent-01/blob/main/README.md)
- **Contact**: yuval.reuveni@checkmarx.com

## 🔗 Related Projects

- [Strands Agents](https://github.com/strands-ai/strands-agents) - The underlying agent framework
- [GitHub MCP Server](https://github.com/github/github-mcp-server) - Official GitHub MCP implementation
- [Model Context Protocol](https://modelcontextprotocol.io/) - MCP specification

---

**Happy Agent Building! 🤖✨**

> Generated for session f3e8d9a1 - $(date)