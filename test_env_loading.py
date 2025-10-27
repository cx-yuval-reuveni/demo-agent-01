#!/usr/bin/env python3
"""
Test script to verify .env loading
"""

import os
from dotenv import load_dotenv, find_dotenv

def test_env_loading():
    """Test if .env file is being loaded correctly"""
    print("🧪 Testing environment variable loading...")
    
    # Find and load .env
    dotenv_path = find_dotenv()
    print(f"📁 Found .env file at: {dotenv_path}")
    
    load_result = load_dotenv(dotenv_path)
    print(f"📝 load_dotenv() result: {load_result}")
    
    # Check the token
    token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    print(f"🔑 GitHub token loaded: {'✅ Yes' if token else '❌ No'}")
    
    if token:
        print(f"🔑 Token length: {len(token)} characters")
        print(f"🔑 Token starts with: {token[:8]}...")
    else:
        print("❌ GITHUB_PERSONAL_ACCESS_TOKEN not found in environment")
        
        # Check what variables are available
        print("🔍 Available environment variables starting with 'GITHUB':")
        for key, value in os.environ.items():
            if key.startswith('GITHUB'):
                print(f"   {key}: {value[:8]}..." if value else f"   {key}: (empty)")

if __name__ == "__main__":
    test_env_loading()