#!/usr/bin/env python3
# File: test_github_token.py
# Path: AIDEV-ProjectSetup/test_github_token.py
# Standard: AIDEV-PascalCase-1.6
# Created: 2025-03-24
# Last Modified: 2025-03-24  8:00PM
# Description: Test script for checking GitHub token access

"""
Test script for GitHub token access.

This script tests whether the GitHub Personal Access Token (PAT) is
properly loaded and can be used to access the GitHub API.
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
ProjectRoot = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ProjectRoot)

# Import project modules
from Utils.ConfigManager import ConfigManager
import requests

def Main():
    """Main entry point for the script."""
    print("\n====== GitHub Token Test ======\n")
    
    # Create config manager and load environment variables
    Config = ConfigManager()
    
    # Check if token exists
    Token = Config.GetGitHubToken()
    if not Token:
        print("ERROR: GitHub token not found in environment or configuration.")
        print("Make sure you have a GITHUB_PAT environment variable or a .env file with GITHUB_PAT=your_token")
        return False
    
    # Mask token for display
    MaskedToken = Token[:4] + "..." + Token[-4:] if len(Token) > 8 else "****"
    print(f"GitHub token found: {MaskedToken}")
    
    # Test token with a simple API call
    Headers = {
        "Authorization": f"token {Token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Get user information
    print("\nTesting token with GitHub API...")
    try:
        Response = requests.get("https://api.github.com/user", headers=Headers)
        
        if Response.status_code == 200:
            UserData = Response.json()
            print(f"Success! Authenticated as: {UserData.get('login')}")
            print(f"User Name: {UserData.get('name', 'Not provided')}")
            print(f"User Email: {UserData.get('email', 'Not provided')}")
            return True
        else:
            print(f"API Error: Status code {Response.status_code}")
            print(f"Response: {Response.text}")
            return False
    
    except Exception as E:
        print(f"Error testing GitHub token: {str(E)}")
        return False

if __name__ == "__main__":
    Success = Main()
    if Success:
        print("\n✅ GitHub token is valid and working.")
    else:
        print("\n❌ GitHub token test failed.")
