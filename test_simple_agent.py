#!/usr/bin/env python3
"""
Simple test for the GitHub agent
"""
import os
from dotenv import load_dotenv
from agents.config_base_model import get_base_model
from strands import Agent

load_dotenv()

def test_basic_agent():
    """Test basic agent without MCP tools"""
    try:
        print("🔧 Creating basic model...")
        model = get_base_model(max_tokens=1000)
        
        print("🤖 Creating agent...")
        agent = Agent(
            model=model,
            system_prompt="You are a helpful assistant. Be concise.",
            tools=[]  # No tools for now
        )
        
        print("💬 Testing agent...")
        result = agent("Just say 'Hello from demo-agent-01!' and nothing else.")
        print(f"✅ Agent Result: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_basic_agent()
    print(f"🎯 Test {'PASSED' if success else 'FAILED'}")