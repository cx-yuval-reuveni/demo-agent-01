# Demo Agent 01

> AI Agent using Docker-based MCP (Model Context Protocol) for GitHub integration

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![UV](https://img.shields.io/badge/uv-package%20manager-green.svg)](https://github.com/astral-sh/uv)
[![MCP](https://img.shields.io/badge/MCP-1.13.1-purple.svg)](https://github.com/modelcontextprotocol/python-sdk)
[![Docker](https://img.shields.io/badge/docker-required-blue.svg)](https://www.docker.com/)

## Overview

This project demonstrates an AI agent that uses Docker-based Model Context Protocol (MCP) to interact with GitHub repositories. The agent can analyze repositories, create comprehensive README files, manage issues, and perform various GitHub operations through a containerized MCP server.

## Features

- 🐳 **Docker-based MCP Integration**: Uses GitHub's official MCP server in a Docker container
- 🤖 **AI-Powered Analysis**: Leverages Strands agents for intelligent repository analysis
- 📊 **Comprehensive Logging**: File and console logging with detailed operation tracking
- 🔧 **Modern Python Tooling**: Built with `uv` for fast, reliable dependency management
- 🚀 **CLI Interface**: Easy-to-use command-line interface for various operations
- 🔒 **Secure**: Environment-based configuration with proper token management

## Quick Start

### Prerequisites

- Python 3.10 or higher
- Docker Desktop running
- [uv](https://github.com/astral-sh/uv) package manager
- GitHub Personal Access Token

### Installation

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone and setup**:
   ```bash
   git clone https://github.com/cx-yuval-reuveni/demo-agent-01
   cd demo-agent-01
   
   # Create virtual environment and install dependencies
   uv sync
   
   # Activate the virtual environment
   source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
   ```

3. **Configure environment**:
   ```bash
   cp .env.template .env
   # Edit .env and add your GitHub Personal Access Token
   ```

4. **Pull Docker image**:
   ```bash
   docker pull ghcr.io/github/github-mcp-server
   ```

### Usage

#### CLI Commands

```bash
# Test MCP connection
uv run demo-agent test-mcp

# Run GitHub analysis
uv run demo-agent github "Analyze the microsoft/playwright repository"

# Or use module execution
uv run python -m agents.github_agent
uv run python test_docker_mcp.py
```

#### Available Scripts

- `github-agent`: Run the GitHub analysis agent
- `test-mcp`: Test Docker MCP connection
- `demo-agent`: Main CLI interface

## Project Structure

```
demo-agent-01/
├── agent_tools/           # MCP tool implementations
│   ├── __init__.py
│   ├── github_tools.py    # Docker MCP GitHub client
│   ├── rag_tools.py       # RAG utilities
│   └── web_tools.py       # Web scraping tools
├── agents/                # AI agent implementations  
│   ├── __init__.py
│   ├── github_agent.py    # Main GitHub agent
│   ├── config_base_model.py
│   └── swarm/            # Swarm agent implementations
├── demo_agent/           # CLI interface
│   ├── __init__.py
│   └── cli.py
├── tests/                # Test suite (coming soon)
├── pyproject.toml        # Modern Python project config
├── .env.template         # Environment variables template
├── README.md             # This file
└── MCP_SETUP.md         # Detailed MCP setup guide
```

## Development

### Installing Development Dependencies

```bash
# Install with development dependencies
uv sync --extra dev

# Install specific extra groups
uv sync --extra test --extra docs
```

### Code Quality

```bash
# Format code
uv run black .
uv run isort .

# Lint code  
uv run flake8 .
uv run mypy .

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov
```

### Adding Dependencies

```bash
# Add runtime dependency
uv add requests

# Add development dependency  
uv add --dev pytest

# Add optional dependency
uv add --optional test pytest-mock
```

## Configuration

### Environment Variables

Create a `.env` file based on `.env.template`:

```bash
# GitHub Integration
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token_here

# AI Models (Checkmarx internal)
AIPROXY_API_KEY=your_api_key_here

# AWS Bedrock (optional)
AWS_REGION=eu-west-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### GitHub Token Setup

1. Go to [GitHub Settings > Personal Access Tokens](https://github.com/settings/tokens)
2. Generate a new token with these scopes:
   - `repo` (Full repository access)
   - `read:org` (Read organization data)  
   - `read:user` (Read user profile data)
3. Copy the token to your `.env` file

## Available MCP Tools

The agent has access to 40+ GitHub MCP tools including:

- **Repository Management**: Get repository info, search repositories, fork repositories
- **File Operations**: Get file contents, create/update files, delete files
- **Issue Management**: Create issues, get issues, add comments, manage labels
- **Pull Request Operations**: Create PRs, get PR details, merge PRs, manage reviews
- **Search Capabilities**: Search code, issues, pull requests, users, repositories
- **Branch Management**: List branches, create branches, get commits
- **Release Management**: Get releases, create releases, manage tags

## Logging

The application provides comprehensive logging:

- **Console Logs**: Real-time output with emoji indicators
- **File Logs**: Detailed logs saved to `mcp_docker.log`
- **Structured Logging**: JSON format logs for production use

## Docker Integration

The MCP server runs in a Docker container using the official GitHub image:

```bash
# The container is managed automatically, but you can also run manually:
docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN=your_token ghcr.io/github/github-mcp-server
```

## Troubleshooting

### Common Issues

1. **"GITHUB_PERSONAL_ACCESS_TOKEN not set"**
   - Ensure your `.env` file has the correct token
   - Check that the `.env` file is in the project root

2. **Docker image not found**
   - Run: `docker pull ghcr.io/github/github-mcp-server`

3. **Tool specification warnings**
   - These are harmless warnings from the Strands framework
   - The tools still work correctly

4. **Permission errors**
   - Ensure your GitHub token has the required scopes
   - Check that Docker is running with proper permissions

### Debug Mode

Enable detailed logging:

```bash
LOG_LEVEL=DEBUG uv run demo-agent github "your prompt"
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run the quality checks: `uv run black . && uv run pytest`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [GitHub MCP Server](https://github.com/github/github-mcp-server) - Official GitHub MCP implementation
- [Strands AI](https://strands.ai) - AI agent framework
- [UV](https://github.com/astral-sh/uv) - Fast Python package manager
- [Model Context Protocol](https://modelcontextprotocol.io) - Protocol for AI-tool integration

---

**Built with ❤️ using UV, Docker, and MCP**