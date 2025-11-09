# README for repo demo-agent-01 session 436

## Setup

To set up the project, you need to install `uv` and `make`. You can install them using the following commands:

```bash
pip install uv
sudo apt-get install make
```

## Environment Variables

Set the following environment variables:

```bash
export GITHUB_TOKEN=your_github_token
export MCP_CONFIG=your_mcp_config
```

## How to Run

To run the GitHub agent, use the following command:

```bash
make run
```

## GitHub MCP Usage

### Manual Usage

To use GitHub MCP manually, you can run the following command:

```bash
make mcp-manual
```

### Managed Usage

To use GitHub MCP in a managed way, you can run the following command:

```bash
make mcp-managed
```

## Troubleshooting

### Network Errors

If you encounter network errors, ensure that your internet connection is stable and that you have the correct permissions to access the GitHub API. You can also try restarting your network connection or using a different network.
