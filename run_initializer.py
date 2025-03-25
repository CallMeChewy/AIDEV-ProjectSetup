#!/usr/bin/env python3
# File: run_initializer.py
# Path: AIDEV-ProjectSetup/run_initializer.py
# Standard: AIDEV-PascalCase-1.6
# Created: 2025-03-24
# Last Modified: 2025-03-24  7:30PM
# Description: Runner script for project initialization

"""
Runner script for project initialization.

This script provides a convenient way to initialize a new project using
the ProjectInitializer. It sets up proper Python path handling to avoid
import errors when running from any location.
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
ProjectRoot = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ProjectRoot)

# Import project modules
from Core.ProjectInitializer import ProjectInitializer
from Utils.ConfigManager import ConfigManager

def Main():
    """Main entry point for the script."""
    # Create config manager
    Config = ConfigManager()
    
    # Create initializer
    Initializer = ProjectInitializer(Config)
    
    # Define the project configuration
    ProjectConfig = {
        'ProjectName': 'AIDEV-MyNewProject',  # Change this to your project name
        'Description': 'A new project created with AIDEV-ProjectSetup',
        'ProjectPath': os.path.expanduser('~/Projects'),  # Change to your preferred path
        'GitHubAccount': 'Your-GitHub-Username',  # Change to your GitHub username
        'RepositoryName': 'AIDEV-MyNewProject'  # Should match ProjectName typically
    }
    
    # Customize configuration as needed
    # Prompt for project name
    ProjectName = input("Enter project name (default: AIDEV-MyNewProject): ")
    if ProjectName:
        ProjectConfig['ProjectName'] = ProjectName
        if ProjectConfig['RepositoryName'] == 'AIDEV-MyNewProject':
            ProjectConfig['RepositoryName'] = ProjectName
    
    # Prompt for project path
    DefaultPath = ProjectConfig['ProjectPath']
    ProjectPath = input(f"Enter project path (default: {DefaultPath}): ")
    if ProjectPath:
        ProjectConfig['ProjectPath'] = ProjectPath
    
    # Prompt for GitHub account
    GithubAccount = input(f"Enter GitHub username (default: {ProjectConfig['GitHubAccount']}): ")
    if GithubAccount:
        ProjectConfig['GitHubAccount'] = GithubAccount
    
    # Confirm settings
    print("\nProject Configuration:")
    print(f"  Project Name: {ProjectConfig['ProjectName']}")
    print(f"  Description: {ProjectConfig['Description']}")
    print(f"  Project Path: {ProjectConfig['ProjectPath']}")
    print(f"  GitHub Account: {ProjectConfig['GitHubAccount']}")
    print(f"  Repository Name: {ProjectConfig['RepositoryName']}")
    
    Confirm = input("\nProceed with these settings? (y/n): ")
    if Confirm.lower() != 'y':
        print("Initialization cancelled.")
        return
    
    # Initialize project
    print("\nStarting project initialization...")
    Result = Initializer.InitializeProject(ProjectConfig)
    
    # Report result
    if Result:
        print(f"\nProject initialization successful!")
        print(f"Project created at: {os.path.join(ProjectConfig['ProjectPath'], ProjectConfig['ProjectName'])}")
    else:
        print("\nProject initialization failed. Please check the error messages above.")

if __name__ == "__main__":
    Main()
