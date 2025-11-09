# README for session 4b9e7c31

## Demo Agent 01 - AI Agent with GitHub Integration

This repository contains an AI agent system that demonstrates integration with GitHub using Docker-based MCP (Model Context Protocol) for seamless GitHub operations. The agent leverages the Strands framework and provides multiple specialized agents for different use cases.

## 🚀 Overview

**demo-agent-01** is an advanced AI agent system featuring:
- **GitHub MCP Integration**: Direct GitHub API access through Docker-containerized MCP server
- **Multi-Agent Architecture**: Specialized agents for GitHub, web search, and AWS Bedrock
- **Strands Framework**: Built on the modern Strands agents framework
- **Observability**: Integrated Langfuse tracing and monitoring
- **Production Ready**: Comprehensive testing, linting, and CI/CD setup

## 📋 Prerequisites

Before running the agent, ensure you have the following installed:

- **Python 3.10+** (Required)
- **Docker** (Required for GitHub MCP server)
- **uv** (Package manager - will be auto-installed if missing)
- **Git** (For repository operations)

### System Requirements
- Operating System: Linux, macOS, or Windows with WSL2
- Memory: At least 4GB RAM recommended
- Storage: 2GB free space for Docker images and dependencies

## 🛠️ Quick Setup

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/cx-yuval-reuveni/demo-agent-01.git
cd demo-agent-01

# Complete setup (installs uv, dependencies, Docker image)
make setup
```

### 2. Configure Environment

```bash
# Edit the .env file with your credentials
nano .env
```

**Required Configuration:**
```env
# GitHub Integration (Required)
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token_here

# AI Model Access (Required)  
AIPROXY_API_KEY=your_aiproxy_key_here
```

**Optional Configuration:**
```env
# Langfuse Observability
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
LANGFUSE_BASE_URL=https://your-langfuse-instance.com

# Model Configuration
MODEL_ID=bedrock/claude-sonnet-4
MAX_TOKENS=30000
TEMPERATURE=0.7
```

### 3. Get GitHub Token

1. Go to [GitHub Settings > Personal Access Tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select the following scopes:
   - `repo` (Full control of private repositories)
   - `read:org` (Read org and team membership)
   - `read:user` (Read user profile data)
4. Copy the token and add it to your `.env` file

### 4. Verify Setup

```bash
# Check environment variables
make env-check

# Test MCP connection
make test-mcp
```

## 🤖 Running the Agents

### GitHub Agent (Primary)

The GitHub agent provides comprehensive GitHub integration capabilities:

```bash
# Run the GitHub agent
make run-github
```

**Capabilities:**
- Repository analysis and management
- Issue and pull request operations
- Code search and review
- Branch and commit operations
- Release management
- Organization and team management

### Web Search Agent

```bash
# Run the web search agent
make run-web
```

### AWS Bedrock Agent

```bash
# Run the bedrock agent  
make run-bedrock
```

### Show All Available Agents

```bash
# List all available agents
make run-agents
```

## 📁 Project Structure

```
demo-agent-01/
├── agents/                     # Agent implementations
│   ├── github_agent.py        # GitHub MCP integration agent
│   ├── web_search_agent.py     # Web search capabilities
│   ├── bedrock_agent.py        # AWS Bedrock integration
│   ├── agent.py                # Base agent class
│   └── config_base_model.py    # Model configuration
├── agent_tools/                # Reusable tools and utilities
│   ├── web_tools.py           # Web scraping and search tools
│   └── rag_tools.py           # RAG (Retrieval Augmented Generation) tools
├── .env.template              # Environment configuration template
├── pyproject.toml             # Project configuration and dependencies
├── Makefile                   # Build and development automation
└── README for session 4b9e7c31.md  # This documentation
```

## 🔧 Development

### Setup Development Environment

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

# Lint code
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

### Building

```bash
# Build the package
make build

# Clean build artifacts
make clean
```

## 🐳 Docker Integration

The project uses Docker for the GitHub MCP server:

```bash
# Pull the GitHub MCP server image
make docker-pull

# Clean up Docker containers
make docker-clean
```

The GitHub MCP server runs in a Docker container and provides:
- Secure GitHub API access
- Standardized MCP protocol interface
- Isolated execution environment
- Easy deployment and scaling

## 📊 Monitoring and Observability

### Langfuse Integration

The agent supports Langfuse for comprehensive tracing and monitoring:

1. **Setup Langfuse** (Optional):
   - Sign up at [Langfuse](https://langfuse.com)
   - Get your public and secret keys
   - Add them to your `.env` file

2. **Features**:
   - Request tracing and logging
   - Performance monitoring
   - Cost tracking
   - Session management
   - User analytics

### Telemetry

The agent includes built-in telemetry using OpenTelemetry:
- Automatic request/response logging
- Performance metrics
- Error tracking
- Custom trace attributes

## 🔒 Security Considerations

### Token Security
- Store GitHub tokens securely in `.env` file
- Never commit tokens to version control
- Use minimal required token scopes
- Rotate tokens regularly

### Docker Security
- MCP server runs in isolated container
- No persistent data storage in container
- Environment variables passed securely
- Regular image updates recommended

## 📚 Usage Examples

### Basic GitHub Operations

```python
# The GitHub agent can perform operations like:
# - "Create a new issue in repository X"
# - "List all pull requests in my repositories"
# - "Analyze the code structure of repository Y"
# - "Create a branch and make changes"
# - "Review and merge pull requests"
```

### Advanced Workflows

```python
# Complex multi-step operations:
# - "Analyze repository, create issues for improvements, and assign them"
# - "Review all open PRs and provide automated feedback"
# - "Generate release notes from commit history"
# - "Audit repository security and compliance"
```

## 🛠️ Troubleshooting

### Common Issues

1. **Docker not running**:
   ```bash
   # Start Docker service
   sudo systemctl start docker  # Linux
   # or start Docker Desktop on macOS/Windows
   ```

2. **GitHub token issues**:
   ```bash
   # Verify token has correct scopes
   curl -H "Authorization: token $GITHUB_PERSONAL_ACCESS_TOKEN" https://api.github.com/user
   ```

3. **Python version conflicts**:
   ```bash
   # Ensure Python 3.10+ is installed
   python --version
   # Use uv to manage Python versions
   uv python install 3.11
   ```

4. **MCP connection failures**:
   ```bash
   # Check Docker image
   docker images | grep github-mcp-server
   # Test MCP connection
   make test-mcp
   ```

### Debug Mode

Enable debug logging by setting:
```env
DEBUG=true
LOG_LEVEL=debug
```

### Getting Help

1. Check the [GitHub Issues](https://github.com/cx-yuval-reuveni/demo-agent-01/issues)
2. Review the Makefile for available commands: `make help`
3. Check project info: `make info`

## 🤝 Contributing

### Development Workflow

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run quality checks: `make check`
5. Run tests: `make test`
6. Submit a pull request

### Code Standards

- Follow PEP 8 style guidelines
- Use type hints
- Write comprehensive docstrings
- Add tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Strands Framework**: For the powerful agent foundation
- **GitHub MCP Server**: For seamless GitHub integration
- **Docker**: For containerization and isolation
- **Langfuse**: For observability and monitoring
- **uv**: For fast and reliable Python package management

## 📞 Support

For support and questions:
- **Repository**: [https://github.com/cx-yuval-reuveni/demo-agent-01](https://github.com/cx-yuval-reuveni/demo-agent-01)
- **Issues**: [https://github.com/cx-yuval-reuveni/demo-agent-01/issues](https://github.com/cx-yuval-reuveni/demo-agent-01/issues)
- **Author**: Yuval Reuveni (yuval.reuveni@checkmarx.com)

---

**Session ID**: 4b9e7c31  
**Generated**: $(date)  
**Version**: 0.1.0

## 🚀 Quick Start Summary

```bash
# 1. Clone and setup
git clone https://github.com/cx-yuval-reuveni/demo-agent-01.git
cd demo-agent-01
make setup

# 2. Configure environment
# Edit .env with your GitHub token and AI proxy key

# 3. Verify setup
make env-check
make test-mcp

# 4. Run the GitHub agent
make run-github
```

That's it! Your AI agent is ready to help with GitHub operations. 🎉