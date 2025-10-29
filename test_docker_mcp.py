#!/usr/bin/env python3
"""
Test script for Docker MCP client specifically
"""

import os
import sys

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent_tools.github_tools import DockerMCPClient

def test_docker_mcp_client():
    """Test the Docker MCP client initialization and startup"""
    print("🧪 Testing Docker MCP Client...")
    
    try:
        # Create client
        client = DockerMCPClient()
        print("✅ DockerMCPClient created successfully")
        
        # Try to start the server
        success = client.start_docker_mcp_server()
        
        if success:
            print("✅ Docker MCP server started successfully")
            
            # Try to list tools
            try:
                tools = client.list_tools()
                print(f"📋 Available tools: {len(tools)}")
                for tool in tools[:3]:  # Show first 3 tools
                    print(f"   - {tool.get('name', 'Unknown')}")
                if len(tools) > 3:
                    print(f"   ... and {len(tools) - 3} more")
            except Exception as e:
                print(f"❌ Error listing tools: {str(e)}")
            
            # Clean up
            client.stop_docker_server()
            print("🛑 Docker server stopped")
        else:
            print("❌ Failed to start Docker MCP server")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    
    return True


def main():
    """Main function for CLI usage"""
    return test_docker_mcp_client()

if __name__ == "__main__":
    test_docker_mcp_client()