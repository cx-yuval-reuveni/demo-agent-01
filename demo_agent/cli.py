#!/usr/bin/env python3
"""
CLI interface for the demo agent
"""

import argparse
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agents.github_agent import create_github_agent


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Demo Agent 01 - AI Agent using Docker-based MCP for GitHub integration"
    )
    
    parser.add_argument(
        "--version", 
        action="version", 
        version="demo-agent-01 0.1.0"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # GitHub agent command
    github_parser = subparsers.add_parser("github", help="Run GitHub analysis agent")
    github_parser.add_argument(
        "prompt", 
        help="Prompt for the GitHub agent"
    )
    github_parser.add_argument(
        "--max-tokens", 
        type=int, 
        default=30000, 
        help="Maximum tokens for the model (default: 30000)"
    )
    
    # Test MCP command
    test_parser = subparsers.add_parser("test-mcp", help="Test MCP Docker connection")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    if args.command == "github":
        return run_github_agent(args.prompt, args.max_tokens)
    elif args.command == "test-mcp":
        return test_mcp_connection()
    
    return 0


def run_github_agent(prompt: str, max_tokens: int = 30000):
    """Run the GitHub agent with the given prompt"""
    try:
        print("🤖 Starting GitHub Agent...")
        github_agent = create_github_agent()
        response = github_agent(prompt)
        print("\n" + "="*50)
        print("🎯 Agent Response:")
        print("="*50)
        print(response)
        return 0
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1


def test_mcp_connection():
    """Test the MCP Docker connection"""
    try:
        print("🧪 Testing MCP Docker connection...")
        # Import and run the test
        from test_docker_mcp import test_docker_mcp_client
        success = test_docker_mcp_client()
        return 0 if success else 1
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())