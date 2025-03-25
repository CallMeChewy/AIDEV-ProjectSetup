# File: GitHubManager.py
# Path: AIDEV-ProjectSetup/Core/GitHubManager.py
# Standard: AIDEV-PascalCase-1.6
# Created: 2025-03-23
# Last Modified: 2025-03-24  1:10PM
# Description: GitHub repository management functionality

"""
GitHub repository management functionality.

This module provides functionality for interacting with GitHub repositories,
including validation, creation, and updating.
"""

import os
import subprocess
import requests
from pathlib import Path

class GitHubManager:
    """GitHub repository management functionality."""
    
    def __init__(self, ConfigManager):
        """
        Initialize GitHubManager.
        
        Args:
            ConfigManager: Configuration manager instance
        """
        self.Config = ConfigManager
    
    def ValidateRepository(self, Account, RepoName, Token=None):
        """
        Validate GitHub repository.
        
        Args:
            Account: GitHub account name
            RepoName: Repository name
            Token: GitHub PAT (optional)
            
        Returns:
            dict: Validation results with status and message
        """
        # Use token from config if not provided
        if not Token:
            Token = self.Config.GetGitHubToken()
        
        # Prepare headers
        Headers = {}
        if Token:
            Headers['Authorization'] = f"token {Token}"
        
        # Check if repository exists
        Url = f"https://api.github.com/repos/{Account}/{RepoName}"
        try:
            Response = requests.get(Url, headers=Headers)
            
            if Response.status_code == 404:
                # Repository doesn't exist
                return {
                    'Status': 'NotFound',
                    'Message': f"Repository {Account}/{RepoName} not found. You'll need to create it first."
                }
            
            if Response.status_code != 200:
                # Error checking repository
                return {
                    'Status': 'Error',
                    'Message': f"Error checking repository: {Response.status_code} - {Response.text}"
                }
            
            # Repository exists, check if it's empty
            RepoData = Response.json()
            if RepoData.get('size', 0) > 0:
                # Repository is not empty
                return {
                    'Status': 'NotEmpty',
                    'Message': f"Repository {Account}/{RepoName} is not empty. Please use an empty repository."
                }
            
            # Repository exists and is empty
            return {
                'Status': 'Valid',
                'Message': f"Repository {Account}/{RepoName} is valid and empty."
            }
            
        except Exception as E:
            return {
                'Status': 'Error',
                'Message': f"Error validating repository: {str(E)}"
            }
    
    def PushToRemote(self, ProjectPath, Account, RepoName, Token, Branch="main"):
        """
        Push to remote GitHub repository.
        
        Args:
            ProjectPath: Path to project directory
            Account: GitHub account name
            RepoName: Repository name
            Token: GitHub personal access token
            Branch: Branch name to push (default: main)
            
        Returns:
            bool: True if push was successful
        """
        try:
            # Create URL with token for push
            RemoteUrl = f"https://{Account}:{Token}@github.com/{Account}/{RepoName}.git"
            
            # Set remote URL with token
            subprocess.run(
                ['git', 'remote', 'set-url', 'origin', RemoteUrl],
                cwd=ProjectPath,
                check=True,
                capture_output=True  # Hide output to avoid showing token
            )
            
            # Push to remote using the specified branch
            Result = subprocess.run(
                ['git', 'push', '-u', 'origin', Branch], 
                cwd=ProjectPath,
                check=True,
                capture_output=True
            )
            
            # Reset remote URL without token
            PublicRemoteUrl = f"https://github.com/{Account}/{RepoName}.git"
            subprocess.run(
                ['git', 'remote', 'set-url', 'origin', PublicRemoteUrl],
                cwd=ProjectPath,
                check=True,
                capture_output=True
            )
            
            print(f"Successfully pushed to remote repository: {Account}/{RepoName}")
            return True
            
        except subprocess.CalledProcessError as E:
            print(f"Error pushing to remote: {E.stderr.decode('utf-8')}")
            return False
        except Exception as E:
            print(f"Error pushing to remote: {str(E)}")
            return False
    
    def CreateRepository(self, Account, RepoName, Description, Token):
        """
        Create new GitHub repository.
        
        Args:
            Account: GitHub account name
            RepoName: Repository name
            Description: Repository description
            Token: GitHub personal access token
            
        Returns:
            dict: Creation results with status and message
        """
        # Prepare headers
        Headers = {
            'Authorization': f"token {Token}",
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Prepare data
        Data = {
            'name': RepoName,
            'description': Description,
            'private': False,
            'auto_init': False
        }
        
        # Create repository
        Url = f"https://api.github.com/user/repos"
        try:
            Response = requests.post(Url, headers=Headers, json=Data)
            
            if Response.status_code != 201:
                return {
                    'Status': 'Error',
                    'Message': f"Error creating repository: {Response.status_code} - {Response.text}"
                }
            
            return {
                'Status': 'Created',
                'Message': f"Repository {Account}/{RepoName} created successfully."
            }
            
        except Exception as E:
            return {
                'Status': 'Error',
                'Message': f"Error creating repository: {str(E)}"
            }
    
    def CreateUpdateScript(self, ProjectPath):
        """
        Create update script for the project.
        
        Args:
            ProjectPath: Path to project directory
            
        Returns:
            Path: Path to created script
        """
        ScriptPath = ProjectPath / 'Scripts' / 'update-repo.sh'
        
        # Ensure Scripts directory exists
        (ProjectPath / 'Scripts').mkdir(exist_ok=True)
        
        # Create script content
        Content = """#!/bin/bash
# update-repo.sh - Script for updating repository
# Created by AIDEV-ProjectSetup

# Get current date in MM/DD/YY format
DATE=$(date +"%m/%d/%y %I:%M%p")

# Default commit message
DEFAULT_MESSAGE="Update $DATE"

# Use provided message or default
MESSAGE=${1:-$DEFAULT_MESSAGE}

echo "Committing changes with message: $MESSAGE"

# Add all files to staging
git add .

# Commit changes
git commit -m "$MESSAGE"

# Push to remote
git push

echo "Repository updated successfully."
"""
        
        # Write script file
        with open(ScriptPath, 'w') as File:
            File.write(Content)
        
        # Make script executable
        os.chmod(ScriptPath, 0o755)
        
        return ScriptPath


# For testing this module directly
if __name__ == "__main__":
    from Utils.ConfigManager import ConfigManager
    
    # Create config manager
    Config = ConfigManager()
    
    # Create GitHubManager instance
    Manager = GitHubManager(Config)
    
    # Example usage
    print("GitHub Manager Test")
    
    # Validate repository
    Account = "YourGitHubUsername"  # Replace with your GitHub username
    RepoName = "AIDEV-TestRepo"     # Replace with your test repo name
    
    Result = Manager.ValidateRepository(Account, RepoName)
    print(f"Repository validation result: {Result['Status']}")
    print(f"Message: {Result['Message']}")
