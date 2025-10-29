# MCP Docker GitHub Integration

This project integrates with GitHub using the Model Context Protocol (MCP) via Docker.

## Setup Instructions

### 1. Prerequisites
- Docker installed and running
- GitHub Personal Access Token

### 2. Environment Setup

1. Copy the template file:
   ```bash
   cp .env.template .env
   ```

2. Edit `.env` and add your GitHub token:
   ```bash
   GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_actual_token_here
   ```

3. Get a GitHub token from: https://github.com/settings/tokens
   - Required scopes: `repo`, `read:org`, `read:user`

### 3. Docker Image

The GitHub MCP server Docker image should already be pulled. If not, run:
```bash
docker pull ghcr.io/github/github-mcp-server
```

### 4. Testing

Run the test script to verify everything works:
```bash
python test_mcp.py
```

## Logging

Logs are written to both console and `mcp_docker.log` file in the project root.

## Features

- ✅ Docker container management with cleanup
- ✅ Comprehensive logging to file and console  
- ✅ Automatic Docker image verification and pulling
- ✅ MCP protocol communication
- ✅ GitHub API integration via MCP tools

## Available Functions

- `mcp_get_repository(owner, repo)` - Get repository info
- `mcp_search_repositories(query, limit)` - Search repositories  
- `mcp_get_file_contents(owner, repo, path)` - Get file contents
- `mcp_list_tools()` - List available MCP tools
- `mcp_create_issue(owner, repo, title, body)` - Create GitHub issue
- `mcp_get_issues(owner, repo, state, limit)` - Get repository issues

## Troubleshooting

1. **"Docker image not found"** - Run `docker pull ghcr.io/github/github-mcp-server`
2. **"Container already exists"** - The code automatically cleans up existing containers
3. **"No logs visible"** - Check `mcp_docker.log` file for detailed logs
4. **"GitHub token error"** - Verify your token in `.env` file has correct permissions

## Log File Location

Logs are saved to: `mcp_docker.log` in the project root directory.