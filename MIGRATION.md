# Migration to UV

This project has been successfully migrated from pip to UV package manager.

## What Changed

### New Files
- `pyproject.toml` - Modern Python project configuration
- `uv.lock` - Lock file for reproducible builds (auto-generated)
- `demo_agent/` - CLI package with proper entry points
- `Makefile` - Common development tasks
- Updated `README.md` - Comprehensive documentation

### Removed Files
- `requirements.txt` - Replaced by pyproject.toml dependencies

### Enhanced Features
- ✅ Modern Python packaging with `pyproject.toml`
- ✅ Fast dependency resolution with UV
- ✅ CLI interface with `uv run demo-agent`
- ✅ Development dependencies (`uv sync --extra dev`)
- ✅ Code quality tools (black, isort, flake8, mypy)
- ✅ Testing setup with pytest
- ✅ Makefile for common tasks

## Usage

```bash
# Install dependencies
uv sync

# Run tests
uv run demo-agent test-mcp

# Run GitHub agent
uv run demo-agent github "your prompt here"

# Development commands
make help          # Show available commands
make dev           # Setup development environment
make test          # Run tests
make format        # Format code
make lint          # Lint code
```

## Benefits of UV

1. **Speed**: 10-100x faster than pip
2. **Reliability**: Consistent dependency resolution
3. **Modern**: Built-in support for pyproject.toml
4. **Compatibility**: Drop-in replacement for pip
5. **Isolation**: Better virtual environment management

## Migration Steps Taken

1. Created `pyproject.toml` from `requirements.txt`
2. Set up proper package structure
3. Added CLI entry points
4. Configured development tools
5. Added comprehensive documentation
6. Created Makefile for common tasks