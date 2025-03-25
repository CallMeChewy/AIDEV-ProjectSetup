#!/usr/bin/env python3
# File: create_github_repo.py
# Path: AIDEV-ProjectSetup/create_github_repo.py
# Standard: AIDEV-PascalCase-1.6
# Created: 2025-03-24
# Last Modified: 2025-03-24  8:30PM
# Description: Script to create a GitHub repository

"""
Script to create a GitHub repository.

This script creates a new GitHub repository using the GitHub API
and a Personal Access Token.
"""

import os
import sys
import requests
from pathlib import Path

# Add the project root to the Python path
ProjectRoot = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ProjectRoot)

# Import project modules
from Utils.ConfigManager import ConfigManager

def CreateRepository(Token, RepoName, Description="Repository created by AIDEV-ProjectSetup"):
    """
    Create a new GitHub repository.
    
    Args:
        Token: GitHub Personal Access Token
        RepoName: Name for the new repository
        Description: Repository description
        
    Returns:
        bool: True if created successfully
    """
    Headers = {
        "Authorization": f"token {Token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    Data = {
        "name": RepoName,
        "description": Description,
        "private": False,
        "auto_init": False
    }
    
    URL = "https://api.github.com/user/repos"
    
    try:
        Response = requests.post(URL, headers=Headers, json=Data)
        
        if Response.status_code == 201:
            RepoData = Response.json()
            print(f"Repository created successfully: {RepoData['html_url']}")
            return True
        else:
            print(f"Error creating repository: {Response.status_code}")
            print(f"Response: {Response.text}")
            return False
            
    except Exception as E:
        print(f"Error creating repository: {str(E)}")
        return False

def CheckRepositoryExists(Token, Username, RepoName):
    """
    Check if a repository already exists.
    
    Args:
        Token: GitHub Personal Access Token
        Username: GitHub username
        RepoName: Repository name
        
    Returns:
        bool: True if repository exists
    """
    Headers = {
        "Authorization": f"token {Token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    URL = f"https://api.github.com/repos/{Username}/{RepoName}"
    
    try:
        Response = requests.get(URL, headers=Headers)
        
        if Response.status_code == 200:
            print(f"Repository {Username}/{RepoName} already exists.")
            return True
        elif Response.status_code == 404:
            print(f"Repository {Username}/{RepoName} does not exist.")
            return False
        else:
            print(f"Error checking repository: {Response.status_code}")
            print(f"Response: {Response.text}")
            return False
            
    except Exception as E:
        print(f"Error checking repository: {str(E)}")
        return False

def Main():
    """Main entry point for the script."""
    print("\n====== GitHub Repository Creator ======\n")
    
    # Create config manager and load environment variables
    Config = ConfigManager()
    
    # Get GitHub token
    Token = Config.GetGitHubToken()
    if not Token:
        print("ERROR: GitHub token not found.")
        return False
    
    # Get GitHub username
    Response = requests.get("https://api.github.com/user", 
                           headers={"Authorization": f"token {Token}"})
    if Response.status_code != 200:
        print(f"Error getting user information: {Response.status_code}")
        return False
        
    Username = Response.json()['login']
    print(f"Authenticated as: {Username}")
    
    # Get repository name
    RepoName = input("Enter repository name: ")
    if not RepoName:
        print("Repository name cannot be empty.")
        return False
    
    # Check if repository already exists
    if CheckRepositoryExists(Token, Username, RepoName):
        Overwrite = input("Repository already exists. Delete and recreate? (y/n): ")
        if Overwrite.lower() == 'y':
            # Delete repository
            print(f"Deleting repository {Username}/{RepoName}...")
            DeleteURL = f"https://api.github.com/repos/{Username}/{RepoName}"
            DeleteResponse = requests.delete(DeleteURL, 
                                            headers={"Authorization": f"token {Token}"})
            
            if DeleteResponse.status_code != 204:
                print(f"Error deleting repository: {DeleteResponse.status_code}")
                print(f"Response: {DeleteResponse.text}")
                return False
                
            print("Repository deleted successfully.")
        else:
            print("Keeping existing repository.")
            return True
    
    # Get repository description
    Description = input("Enter repository description (press Enter for default): ")
    if not Description:
        Description = f"Repository created by AIDEV-ProjectSetup"
    
    # Create repository
    Success = CreateRepository(Token, RepoName, Description)
    
    if Success:
        print(f"\nRepository created: https://github.com/{Username}/{RepoName}")
        print(f"Clone URL: https://github.com/{Username}/{RepoName}.git")
    
    return Success

if __name__ == "__main__":
    Success = Main()
    if Success:
        print("\n✅ GitHub repository setup completed.")
    else:
        print("\n❌ GitHub repository setup failed.")
