# Demo Agent 01

🤖 **AI Agent Demo using Docker-based MCP for GitHub integration**

A modern AI agent framework demonstrating integration with GitHub through the Model Context Protocol (MCP) using Docker containers. Built with the Strands framework and featuring multiple agent types including GitHub integration, web search, and AWS Bedrock support.

## 🌟 Features

- **🐳 Docker-based MCP Integration**: Seamless GitHub API access through containerized MCP servers
- **🚀 Multiple Agent Types**: GitHub agent, web search agent, and Bedrock agent
- **📊 Observability**: Built-in Langfuse integration for tracing and monitoring
- **⚡ Modern Python Packaging**: Uses UV for fast dependency management
- **🔧 Developer-Friendly**: Comprehensive Makefile with common development tasks
- **🧪 Testing & Quality**: Pytest, Black, isort, flake8, and mypy integration
- **📝 CLI Interface**: Easy-to-use command-line interface

## 🏗️ Architecture

```
demo-agent-01/
├── agents/                     # Agent implementations
│   ├── github_agent.py        # GitHub integration agent
│   ├── web_search_agent.py     # Web search capabilities
│   ├── bedrock_agent.py        # AWS Bedrock integration
│   └── config_base_model.py    # Model configuration
├── agent_tools/                # Custom agent tools
│   └── web_tools.py           # Web scraping utilities
├── pyproject.toml             # Modern Python project config
├── Makefile                   # Development automation
└── MCP_SETUP.md              # MCP integration guide
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **Docker** (for MCP GitHub integration)
- **UV package manager** (automatically installed during setup)

### 1. Complete Setup

Run the automated setup command:

```bash
make setup
```

This will:
- Install UV package manager if not present
- Install all dependencies
- Pull the GitHub MCP server Docker image
- Set up the development environment

### 2. Environment Configuration

Create your environment file:

```bash
make env-setup
```

Edit `.env` and configure the following variables:

```bash
# Required: GitHub Integration
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token_here

# Required: AI Model Access
AIPROXY_API_KEY=your_aiproxy_key_here

# Optional: Langfuse Observability
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
LANGFUSE_BASE_URL=https://your-langfuse-instance.com
```

#### Getting Your GitHub Token

1. Go to [GitHub Settings > Personal Access Tokens](https://github.com/settings/tokens)
2. Generate a new token with these scopes:
   - `repo` - Repository access
   - `read:org` - Organization read access
   - `read:user` - User profile read access

### 3. Test the Setup

Verify everything is working:

```bash
make test-mcp
```

### 4. Run Your First Agent

Test the GitHub agent:

```bash
make run-github
```

Or run with a custom prompt:

```bash
uv run demo-agent github "List the recent commits in the microsoft/vscode repository"
```

## 🎯 Usage Examples

### GitHub Agent

```bash
# Analyze a repository
uv run demo-agent github "Analyze the repository facebook/react and summarize its key features"

# Create an issue
uv run demo-agent github "Create an issue in my test repository about improving documentation"

# Search repositories
uv run demo-agent github "Find popular Python machine learning repositories with more than 10k stars"

# Get file contents
uv run demo-agent github "Show me the README.md file from the tensorflow/tensorflow repository"
```

### Web Search Agent

```bash
# Search and analyze web content
uv run demo-agent web-search "What are the latest trends in AI agent development?"
```

### Bedrock Agent

```bash
# Use AWS Bedrock models
uv run demo-agent bedrock "Explain the benefits of serverless architecture"
```

## 🛠️ Development

### Development Environment Setup

Set up a complete development environment:

```bash
make dev
```

This installs development dependencies, sets up pre-commit hooks, and prepares your environment.

### Available Commands

```bash
make help                    # Show all available commands
make install                 # Install dependencies
make install-dev            # Install with dev dependencies
make test                   # Run tests
make test-cov               # Run tests with coverage
make format                 # Format code with black and isort
make lint                   # Lint code with flake8 and mypy
make check                  # Run all code quality checks
make clean                  # Clean up build artifacts
make build                  # Build the package
make docker-pull            # Pull GitHub MCP Docker image
make docker-clean           # Clean up Docker containers
```

### Code Quality

This project maintains high code quality standards:

```bash
# Format your code
make format

# Run linting
make lint

# Run all quality checks
make check
```

### Testing

```bash
# Run tests
make test

# Run tests with coverage report
make test-cov

# Test MCP connection specifically
make test-mcp
```

## 🔧 Configuration

### Model Configuration

The agents use configurable AI models through the `config_base_model.py` module:

```python
model = get_base_model(
    model_id="bedrock/claude-sonnet-4",  # Model to use
    max_tokens=30000,                    # Response length
    temperature=0.7,                     # Creativity level
    stream=True                          # Streaming responses
)
```

### MCP Integration

The GitHub MCP integration runs in Docker containers for isolation and reliability:

```python
def github_server_params() -> StdioServerParameters:
    return StdioServerParameters(
        command="docker",
        args=[
            "run", "-i", "--rm",
            "-e", f"GITHUB_PERSONAL_ACCESS_TOKEN={github_token}",
            "ghcr.io/github/github-mcp-server"
        ]
    )
```

## 📊 Observability & Monitoring

### Langfuse Integration

The project includes built-in observability through Langfuse:

- **Trace all agent interactions**
- **Monitor performance metrics**
- **Debug conversation flows**
- **Track usage patterns**

Configure Langfuse in your `.env` file to enable detailed monitoring.

## 🐳 Docker Integration

### GitHub MCP Server

The project uses the official GitHub MCP server Docker image:

```bash
# Pull the image
docker pull ghcr.io/github/github-mcp-server

# The agent automatically manages container lifecycle
```

### Container Management

- Containers are automatically created and cleaned up
- Logs are captured to `mcp_docker.log`
- Environment variables are securely passed to containers

## 🔍 Available Agent Tools

### GitHub Agent Tools

- `get_repository(owner, repo)` - Get repository information
- `search_repositories(query, limit)` - Search GitHub repositories
- `get_file_contents(owner, repo, path)` - Retrieve file contents
- `create_issue(owner, repo, title, body)` - Create GitHub issues
- `get_issues(owner, repo, state, limit)` - List repository issues
- `list_commits(owner, repo, branch)` - Get commit history
- `create_pull_request(...)` - Create pull requests

### Web Search Tools

- Web content scraping and analysis
- Search result processing
- Content summarization

## 🚨 Troubleshooting

### Common Issues

**Docker image not found:**
```bash
make docker-pull
```

**Container already exists:**
```bash
make docker-clean
```

**GitHub token error:**
- Verify your token in `.env` has the required scopes
- Check token hasn't expired

**UV not found:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**MCP connection issues:**
- Check Docker is running
- Verify GitHub token permissions
- Check `mcp_docker.log` for detailed error messages

### Logs

Detailed logs are available in:
- Console output (real-time)
- `mcp_docker.log` (persistent file)

## 📚 Documentation

- [`MCP_SETUP.md`](MCP_SETUP.md) - Detailed MCP integration guide
- [`MIGRATION.md`](MIGRATION.md) - UV migration documentation
- [Strands Framework](https://github.com/strands-ai/strands) - Core agent framework
- [GitHub MCP Server](https://github.com/github/github-mcp-server) - Official GitHub MCP integration

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Run quality checks**: `make check`
5. **Run tests**: `make test`
6. **Commit your changes**: `git commit -m 'Add amazing feature'`
7. **Push to the branch**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[Strands AI](https://github.com/strands-ai)** - Core agent framework
- **[GitHub](https://github.com/github/github-mcp-server)** - MCP server implementation
- **[Anthropic](https://github.com/anthropics/mcp)** - Model Context Protocol
- **[Astral](https://github.com/astral-sh/uv)** - UV package manager

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/cx-yuval-reuveni/demo-agent-01/issues)
- **Documentation**: [Project Wiki](https://github.com/cx-yuval-reuveni/demo-agent-01/wiki)
- **Email**: yuval.reuveni@checkmarx.com

---

⭐ **Star this repository if you find it helpful!**