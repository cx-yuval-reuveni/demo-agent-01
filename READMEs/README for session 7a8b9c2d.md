# README for session 7a8b9c2d

# Demo Agent 01 - AI Agent with GitHub Integration

An AI Agent demonstration using Docker-based MCP (Model Context Protocol) for seamless GitHub integration. This project showcases how to build intelligent agents that can interact with GitHub repositories, perform web searches, and integrate with AWS Bedrock services.

## 🚀 Features

- **GitHub Integration**: Full GitHub API access through MCP Docker container
- **Multiple Agent Types**: GitHub, Web Search, and AWS Bedrock agents
- **Modern Python Stack**: Built with `uv`, `strands-agents`, and `mcp`
- **Observability**: Integrated Langfuse tracing and monitoring
- **Developer-Friendly**: Comprehensive Makefile with common tasks
- **Type Safety**: Full type hints and mypy support

## 📋 Prerequisites

Before running the agent, ensure you have the following installed:

- **Python 3.10+** - Required for the project
- **Docker** - For running the GitHub MCP server
- **uv** - Fast Python package manager (will be installed automatically)
- **Git** - For version control

## 🛠️ Quick Setup

### 1. Complete Automated Setup

Run the complete setup with a single command:

```bash
make setup
```

This will:
- Install `uv` if not present
- Install all Python dependencies
- Pull the GitHub MCP Docker image
- Create `.env` file from template

### 2. Configure Environment Variables

Edit the `.env` file and add your credentials:

```bash
# Required: GitHub Personal Access Token
# Get from: https://github.com/settings/tokens
# Required scopes: repo, read:org, read:user
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token_here

# Required: AI Proxy API Key
# Contact your administrator for this key
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

## 🏃‍♂️ Running the Agents

### GitHub Agent

The main GitHub agent can analyze repositories, create files, manage issues, and more:

```bash
make run-github
```

### Web Search Agent

For web scraping and search capabilities:

```bash
make run-web
```

### AWS Bedrock Agent

For AWS Bedrock integration:

```bash
make run-bedrock
```

### View All Available Agents

```bash
make run-agents
```

## 🔧 Manual Setup (Alternative)

If you prefer manual setup:

### 1. Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install Dependencies

```bash
uv sync
```

### 3. Pull Docker Image

```bash
docker pull ghcr.io/github/github-mcp-server
```

### 4. Setup Environment

```bash
cp .env.template .env
# Edit .env with your credentials
```

## 📁 Project Structure

```
demo-agent-01/
├── agents/                     # Individual agent implementations
│   ├── github_agent.py        # GitHub MCP integration
│   ├── web_search_agent.py    # Web search capabilities  
│   ├── bedrock_agent.py       # AWS Bedrock integration
│   └── config_base_model.py   # Model configuration
├── agent_tools/               # Reusable tools and utilities
│   ├── web_tools.py          # Web scraping tools
│   └── rag_tools.py          # RAG implementation tools
├── .env.template             # Environment variables template
├── pyproject.toml           # Project configuration
├── Makefile                 # Development commands
└── README for session 7a8b9c2d.md  # This file
```

## 🧪 Development Workflow

### Code Quality

Format and lint your code:

```bash
make format  # Format with black and isort
make lint    # Lint with flake8 and mypy
make check   # Run all quality checks
```

### Testing

Run tests:

```bash
make test      # Basic tests
make test-cov  # Tests with coverage
make test-mcp  # Test MCP connection
```

### Development Environment

Setup complete development environment:

```bash
make dev
```

This installs development dependencies and sets up the environment.

## 🐳 Docker Integration

The project uses Docker to run the GitHub MCP server. The Docker container provides:

- Isolated GitHub API access
- Secure token handling
- Consistent environment across systems

### Docker Commands

```bash
make docker-pull   # Pull latest GitHub MCP image
make docker-clean  # Clean up old containers
```

## 🔍 Environment Variables Reference

### Required Variables

| Variable | Description | Where to Get |
|----------|-------------|--------------|
| `GITHUB_PERSONAL_ACCESS_TOKEN` | GitHub API access | [GitHub Settings](https://github.com/settings/tokens) |
| `AIPROXY_API_KEY` | AI model access | Contact administrator |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LANGFUSE_PUBLIC_KEY` | Langfuse observability | - |
| `LANGFUSE_SECRET_KEY` | Langfuse observability | - |
| `LANGFUSE_BASE_URL` | Langfuse instance URL | - |
| `MODEL_ID` | AI model identifier | `bedrock/claude-sonnet-4` |
| `MAX_TOKENS` | Maximum response tokens | `30000` |
| `TEMPERATURE` | Model creativity | `0.7` |

## 🚨 Troubleshooting

### Common Issues

1. **"uv not found"**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   source ~/.bashrc  # or restart terminal
   ```

2. **"Docker image not found"**
   ```bash
   make docker-pull
   ```

3. **"GitHub token invalid"**
   - Check token has required scopes: `repo`, `read:org`, `read:user`
   - Verify token is not expired
   - Ensure no extra spaces in `.env` file

4. **"MCP connection failed"**
   ```bash
   make docker-clean
   make docker-pull
   make test-mcp
   ```

### Debugging

Enable debug logging:

```bash
export DEBUG=1
make run-github
```

Check logs:

```bash
tail -f *.log
```

## 📊 Monitoring and Observability

The project includes Langfuse integration for:

- Request tracing
- Performance monitoring
- Error tracking
- Usage analytics

Configure Langfuse variables in `.env` to enable monitoring.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run quality checks: `make check`
5. Run tests: `make test`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Yuval Reuveni** - *Initial work* - [yuval.reuveni@checkmarx.com](mailto:yuval.reuveni@checkmarx.com)

## 🔗 Links

- [Repository](https://github.com/cx-yuval-reuveni/demo-agent-01)
- [Issues](https://github.com/cx-yuval-reuveni/demo-agent-01/issues)
- [GitHub MCP Server](https://github.com/github/github-mcp-server)
- [Strands Agents](https://github.com/strands-ai/strands-agents)

## 🎯 Example Usage

Here's a quick example of what the GitHub agent can do:

```python
# The agent can analyze repositories, create files, manage issues
result = agent("analyze the repository https://github.com/cx-yuval-reuveni/demo-agent-01 and create readme.md file")
```

The agent will:
1. Connect to GitHub via MCP
2. Analyze the repository structure
3. Examine code and configuration files
4. Generate comprehensive documentation
5. Create or update files as needed

---

**Ready to get started?** Run `make setup` and follow the configuration steps above!