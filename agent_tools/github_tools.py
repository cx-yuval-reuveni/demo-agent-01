import json
import subprocess
import os
from typing import Dict, Any, Optional, List
import time
from dotenv import load_dotenv, find_dotenv
import threading
import queue
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
import atexit


class DockerMCPClient:
    """MCP client that communicates with Docker-based GitHub MCP server"""
    
    def __init__(self):
        # Always load the .env file from the project root or nearest location
        dotenv_path = find_dotenv()
        load_dotenv(dotenv_path)
        self.github_token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
        if not self.github_token:
            raise ValueError("GITHUB_PERSONAL_ACCESS_TOKEN environment variable is required")
        
        self.docker_process = None
        self.request_id = 0
        self.is_initialized = False
    
    def start_docker_mcp_server(self) -> bool:
        """Start the Docker-based MCP GitHub server"""
        try:
            print("🐳 STARTING Docker MCP GitHub server...")
            logging.info("🐳 Starting Docker MCP GitHub server...")
            
            # Debug: Check if token is loaded
            print(f"🔑 GitHub token loaded: {'✅ Yes' if self.github_token else '❌ No'}")
            if self.github_token:
                print(f"🔑 Token length: {len(self.github_token)} characters")
                print(f"🔑 Token starts with: {self.github_token[:8]}...")
            
            # Docker command as configured in your mcp.json
            docker_cmd = [
                "docker", "run", "-i", "--name", "github-mcp-server",
                "-e", f"GITHUB_PERSONAL_ACCESS_TOKEN={self.github_token}",
                "ghcr.io/github/github-mcp-server"
            ]
            print(f"🔧 Docker command: {' '.join(docker_cmd)}")
            
            # Start Docker process with stdin/stdout pipes
            self.docker_process = subprocess.Popen(
                docker_cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=0
            )
            
            # Initialize MCP connection
            init_success = self._initialize_mcp_connection()
            
            if init_success:
                print("✅ Docker MCP GitHub server started successfully")
                logging.info("✅ Docker MCP GitHub server started successfully")
                self.is_initialized = True
                return True
            else:
                print("❌ Failed to initialize MCP connection")
                logging.warning("❌ Failed to initialize MCP connection")
                self.stop_docker_server()
                return False
                
        except Exception as e:
            logging.error(f"Failed to start Docker MCP server: {str(e)}")
            return False
    
    def _initialize_mcp_connection(self) -> bool:
        """Initialize MCP connection with handshake"""
        try:
            # Send initialize request
            init_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "clientInfo": {
                        "name": "strands-github-agent",
                        "version": "1.0.0"
                    }
                }
            }
            
            response = self._send_request(init_request)
            
            if response and "result" in response:
                logging.info("🤝 MCP initialization successful")

                # Send initialized notification
                initialized_notification = {
                    "jsonrpc": "2.0",
                    "method": "notifications/initialized"
                }
                
                self._send_notification(initialized_notification)
                return True
            
            return False
            
        except Exception as e:
            logging.error(f"Failed to initialize MCP connection: {str(e)}")
            return False
    
    def _send_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Send JSON-RPC request to Docker MCP server"""
        if not self.docker_process:
            raise Exception("Docker MCP server not started")
        
        try:
            # Send request
            request_json = json.dumps(request) + "\n"
            logging.info(f"📤 Sending: {request_json.strip()}")
            
            self.docker_process.stdin.write(request_json)
            self.docker_process.stdin.flush()
            
            # Read response
            response_line = self.docker_process.stdout.readline()
            if response_line:
                logging.info(f"📥 Received: {response_line.strip()}")
                return json.loads(response_line)
            else:
                logging.warning("📥 Received empty response")
            return None
            
        except Exception as e:
            logging.error(f"Error sending MCP request: {str(e)}")
            return None
    
    def _send_notification(self, notification: Dict[str, Any]) -> None:
        """Send JSON-RPC notification to Docker MCP server"""
        if not self.docker_process:
            return
        
        try:
            notification_json = json.dumps(notification) + "\n"
            logging.info(f"📤 Sending notification: {notification_json.strip()}")
            
            self.docker_process.stdin.write(notification_json)
            self.docker_process.stdin.flush()
            
        except Exception as e:
            logging.error(f"Error sending MCP notification: {str(e)}")
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List available tools from MCP server"""
        if not self.is_initialized:
            if not self.start_docker_mcp_server():
                raise Exception("Failed to start MCP server")
        
        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/list"
        }
        
        response = self._send_request(request)
        
        if response and "result" in response:
            return response["result"].get("tools", [])
        
        return []
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Call a tool using MCP protocol"""
        if not self.is_initialized:
            if not self.start_docker_mcp_server():
                raise Exception("Failed to start MCP server")
        
        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        response = self._send_request(request)
        
        if response:
            if "error" in response:
                error = response["error"]
                return json.dumps({"error": f"MCP Error {error.get('code')}: {error.get('message')}"}, indent=2)
            
            result = response.get("result", {})
            
            # Extract content from MCP response
            content = result.get("content", [])
            if content and len(content) > 0:
                if content[0].get("type") == "text":
                    return content[0].get("text", "")
            
            return json.dumps(result, indent=2)
        
        return json.dumps({"error": "No response from MCP server"}, indent=2)
    
    def stop_docker_server(self):
        """Stop the Docker MCP server"""
        if self.docker_process:
            try:
                self.docker_process.terminate()
                self.docker_process.wait(timeout=5)
                logging.info("🛑 Docker MCP server stopped")
                
                # Clean up the named container
                try:
                    subprocess.run(["docker", "rm", "github-mcp-server"], 
                                 capture_output=True, check=False)
                except Exception as e:
                    logging.warning(f"Error removing Docker container 'github-mcp-server': {str(e)}")
                    
            except subprocess.TimeoutExpired:
                self.docker_process.kill()
                logging.warning("🔪 Docker MCP server killed")
                # Force remove container if killed
                try:
                    subprocess.run(["docker", "rm", "-f", "github-mcp-server"], 
                                 capture_output=True, check=False)
                except Exception as e:
                    logging.warning(f"Error force-removing Docker container 'github-mcp-server': {str(e)}")
            except Exception as e:
                logging.error(f"Error stopping Docker MCP server: {str(e)}")
            finally:
                self.docker_process = None
                self.is_initialized = False

# Global MCP client instance
mcp_client = DockerMCPClient()

def mcp_get_repository(owner: str, repo: str) -> str:
    """Get repository information using Docker MCP"""
    try:
        return mcp_client.call_tool("get_repository", {"owner": owner, "repo": repo})
    except Exception as e:
        logging.error(f"Error getting repository {owner}/{repo}: {str(e)}")
        return json.dumps({"error": str(e)}, indent=2)

mcp_get_repository.__annotations__ = {
    'owner': str, 
    'repo': str, 
    'return': str
}

def mcp_search_repositories(query: str, limit: int = 5) -> str:
    """Search repositories using Docker MCP"""
    try:
        return mcp_client.call_tool("search_repositories", {"query": query, "limit": limit})
    except Exception as e:
        logging.error(f"Error searching repositories with query '{query}': {str(e)}")
        return json.dumps({"error": str(e)}, indent=2)
    

def mcp_get_file_contents(owner: str, repo: str, path: str) -> str:
    """Get file contents using Docker MCP"""
    try:
        return mcp_client.call_tool("get_file_contents", {"owner": owner, "repo": repo, "path": path})
    except Exception as e:
        logging.error(f"Error getting file contents {owner}/{repo}:{path}: {str(e)}")
        return json.dumps({"error": str(e)}, indent=2)


def mcp_list_tools() -> str:
    """List available MCP tools"""
    try:
        tools = mcp_client.list_tools()
        return json.dumps({"available_tools": tools}, indent=2)
    except Exception as e:
        logging.error(f"Error listing MCP tools: {str(e)}")
        return json.dumps({"error": str(e)}, indent=2)

def mcp_create_issue(owner: str, repo: str, title: str, body: str = "") -> str:
    """Create an issue using Docker MCP"""
    try:
        return mcp_client.call_tool("create_issue", {
            "owner": owner, 
            "repo": repo, 
            "title": title, 
            "body": body
        })
    except Exception as e:
        logging.error(f"Error creating issue '{title}' in {owner}/{repo}: {str(e)}")
        return json.dumps({"error": str(e)}, indent=2)

def mcp_get_issues(owner: str, repo: str, state: str = "open", limit: int = 10) -> str:
    """Get repository issues using Docker MCP"""
    try:
        return mcp_client.call_tool("get_issues", {
            "owner": owner, 
            "repo": repo, 
            "state": state, 
            "limit": limit
        })
    except Exception as e:
        logging.error(f"Error getting issues from {owner}/{repo} (state: {state}): {str(e)}")
        return json.dumps({"error": str(e)}, indent=2)

# Cleanup function
def cleanup_mcp_client():
    """Clean up MCP client resources"""
    global mcp_client
    if mcp_client:
        try:
            mcp_client.stop_docker_server()
        except Exception as e:
            logging.error(f"Error during MCP client cleanup: {str(e)}")

# Register cleanup on exit
atexit.register(cleanup_mcp_client)