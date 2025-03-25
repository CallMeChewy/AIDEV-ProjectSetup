# File: ProjectInitializer.py
# Path: AIDEV-ProjectSetup/Core/ProjectInitializer.py
# Standard: AIDEV-PascalCase-1.6
# Created: 2025-03-23
# Last Modified: 2025-03-24  1:30PM
# Description: Core project initialization functionality

"""
Core project initialization functionality.

This module provides the main functionality for initializing new projects,
including directory structure creation, database setup, and GitHub integration.
"""

import os
import sys
import subprocess
import shutil
import sqlite3
from pathlib import Path
from datetime import datetime
from string import Template

# Add the parent directory to the Python path to fix import issues
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from Core.GitHubManager import GitHubManager
from Core.DatabaseIntegration import DatabaseIntegration
from Utils.DirectoryParser import DirectoryParser

class ProjectInitializer:
    """Project initialization functionality."""
    
    def __init__(self, ConfigManager):
        """
        Initialize ProjectInitializer.
        
        Args:
            ConfigManager: Configuration manager instance
        """
        self.Config = ConfigManager
        self.GitHubManager = GitHubManager(ConfigManager)
        self.DatabaseIntegration = DatabaseIntegration(ConfigManager)
        self.DirectoryParser = DirectoryParser()
    
    def InitializeProject(self, ProjectConfig):
        """
        Initialize a new project.
        
        Args:
            ProjectConfig: Project configuration dictionary
            
        Returns:
            bool: True if initialization was successful
        """
        try:
            # Extract configuration
            ProjectName = ProjectConfig.get('ProjectName')
            ProjectPath = ProjectConfig.get('ProjectPath')
            if not ProjectPath:
                return False
            
            # Create full project path - ensure Path object is used
            ProjectPath = Path(ProjectPath)
            FullProjectPath = ProjectPath / ProjectName
            
            # Check if project directory already exists
            if FullProjectPath.exists():
                print(f"Project directory already exists: {FullProjectPath}")
                return False
            
            # Create project directory
            FullProjectPath.mkdir(parents=True, exist_ok=True)
            
            # Create directory structure
            self.CreateDirectoryStructure(FullProjectPath, ProjectConfig)
            
            # Setup project database
            self.SetupDatabase(FullProjectPath, ProjectConfig)
            
            # Create initial files
            self.CreateInitialFiles(FullProjectPath, ProjectConfig)
            
            # Initialize git repository
            self.InitializeGit(FullProjectPath, ProjectConfig)
            
            # Register project in Himalaya database
            self.RegisterProject(ProjectConfig)
            
            return True
            
        except Exception as E:
            print(f"Error initializing project: {str(E)}")
            return False
    
    def CreateDirectoryStructure(self, ProjectPath, ProjectConfig):
        """
        Create directory structure for project.
        
        Args:
            ProjectPath: Full path to project directory
            ProjectConfig: Project configuration
        """
        # Get directory structure from config
        Structure = ProjectConfig.get('DirectoryStructure')
        
        if not Structure:
            # Use default structure
            Content = self.Config.Get('DefaultStructure')
            Structure = self.DirectoryParser.ParseStructure(Content)
        
        # Create directories
        self.CreateDirectories(ProjectPath, Structure)
        
        # Create special directories
        DirectoriesPath = ProjectPath / 'Directories'
        DirectoriesPath.mkdir(exist_ok=True)
    
    def CreateDirectories(self, BasePath, Structure, CurrentPath=None):
        """
        Recursively create directories from structure.
        
        Args:
            BasePath: Base project path
            Structure: Directory structure dictionary
            CurrentPath: Current path for recursion
        """
        if CurrentPath is None:
            CurrentPath = BasePath
        
        for Name, Children in Structure.items():
            # Skip files
            if '.' in Name and not Name.startswith('.'):
                continue
            
            # Create directory
            NewPath = CurrentPath / Name
            NewPath.mkdir(exist_ok=True)
            
            # Process children
            if Children:
                self.CreateDirectories(BasePath, Children, NewPath)
    
    def SetupDatabase(self, ProjectPath, ProjectConfig):
        """
        Setup project database.
        
        Args:
            ProjectPath: Full path to project directory
            ProjectConfig: Project configuration
        """
        ProjectName = ProjectConfig.get('ProjectName')
        
        # Create project database
        DirectoriesPath = ProjectPath / 'Directories'
        DirectoriesPath.mkdir(exist_ok=True)
        ProjectDbPath = DirectoriesPath / f"{ProjectName}.db"
        
        # Initialize database
        self.DatabaseIntegration.InitializeProjectDatabase(ProjectDbPath, ProjectConfig)
        
        # Create symbolic link to Himalaya database
        self.DatabaseIntegration.CreateDatabaseLink(ProjectPath, ProjectConfig)
    
    def CreateInitialFiles(self, ProjectPath, ProjectConfig):
        """
        Create initial project files.
        
        Args:
            ProjectPath: Full path to project directory
            ProjectConfig: Project configuration
        """
        # Get template path - ensure it's a Path object
        TemplatesPath = Path(self.Config.Get('TemplatesPath'))
        
        # Create README.md
        self.CreateFileFromTemplate(
            TemplatesPath / 'README.md.template',
            ProjectPath / 'README.md',
            ProjectConfig
        )
        
        # Create LICENSE
        self.CreateFileFromTemplate(
            TemplatesPath / 'LICENSE.template',
            ProjectPath / 'LICENSE',
            ProjectConfig
        )
        
        # Create .gitignore
        self.CreateFileFromTemplate(
            TemplatesPath / 'gitignore.template',
            ProjectPath / '.gitignore',
            ProjectConfig
        )
        
        # Create initial requirements.txt
        with open(ProjectPath / 'requirements.txt', 'w') as File:
            File.write("# Project dependencies\n")
            File.write("# Add your dependencies here\n")
            File.write("sqlite3\n")
            File.write("pyside6\n")
            File.write("python-dotenv\n")
    
    def CreateFileFromTemplate(self, TemplatePath, OutputPath, ProjectConfig):
        """
        Create file from template.
        
        Args:
            TemplatePath: Path to template file
            OutputPath: Path to output file
            ProjectConfig: Project configuration
        """
        # If template doesn't exist, create with hardcoded defaults
        if not os.path.exists(TemplatePath):
            print(f"Template file not found: {TemplatePath}")
            if TemplatePath.name == 'README.md.template':
                self.CreateDefaultReadme(OutputPath, ProjectConfig)
            elif TemplatePath.name == 'LICENSE.template':
                self.CreateDefaultLicense(OutputPath, ProjectConfig)
            elif TemplatePath.name == 'gitignore.template':
                self.CreateDefaultGitignore(OutputPath)
            return
        
        try:
            # Read template
            with open(TemplatePath, 'r') as File:
                TemplateContent = File.read()
            
            # Prepare template variables
            TemplateVars = {
                'ProjectName': ProjectConfig.get('ProjectName', ''),
                'Description': ProjectConfig.get('Description', ''),
                'Author': 'Herbert J. Bowers',
                'Date': datetime.now().strftime('%Y-%m-%d'),
                'Year': datetime.now().strftime('%Y'),
                'GitHubAccount': ProjectConfig.get('GitHubAccount', ''),
                'RepositoryName': ProjectConfig.get('RepositoryName', '')
            }
            
            # Apply template
            Template_ = Template(TemplateContent)
            Content = Template_.safe_substitute(TemplateVars)
            
            # Write output file
            with open(OutputPath, 'w') as File:
                File.write(Content)
                
        except Exception as E:
            print(f"Error creating file from template: {str(E)}")
    
    def CreateDefaultReadme(self, OutputPath, ProjectConfig):
        """Create default README.md if template is missing."""
        Content = f"""# {ProjectConfig.get('ProjectName', '')}

## Overview

{ProjectConfig.get('Description', '')}

## Project Structure

This project follows the Project Himalaya organization standards.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/{ProjectConfig.get('GitHubAccount', '')}/{ProjectConfig.get('RepositoryName', '')}.git
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## License

This project is licensed under the terms specified in the LICENSE file.

## Author

Herbert J. Bowers

---

*"Code is not merely functional—it is a visual medium that developers interact with for extended periods. The choices made in these standards prioritize the axis of symmetry, character distinction, readability at scale, and visual hierarchy."*

— Herbert J. Bowers
"""
        with open(OutputPath, 'w') as File:
            File.write(Content)
    
    def CreateDefaultLicense(self, OutputPath, ProjectConfig):
        """Create default LICENSE if template is missing."""
        # Check if the output path exists and is a directory
        if os.path.exists(OutputPath) and os.path.isdir(OutputPath):
            # If it's a directory, remove it and create a file instead
            try:
                os.rmdir(OutputPath)
            except Exception as E:
                print(f"Error removing LICENSE directory: {str(E)}")
                return
        
        Content = f"""MIT License

Copyright (c) {datetime.now().strftime('%Y')} Herbert J. Bowers

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
        try:
            with open(OutputPath, 'w') as File:
                File.write(Content)
            print(f"Created LICENSE file at: {OutputPath}")
        except Exception as E:
            print(f"Error writing LICENSE file: {str(E)}")
    
    def CreateDefaultGitignore(self, OutputPath):
        """Create default .gitignore if template is missing."""
        Content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
*.manifest
*.spec

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# IDE specific files
.idea/
.vscode/
*.swp
*.swo

# OS specific files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
**/local_settings.py
db.sqlite3
"""
        with open(OutputPath, 'w') as File:
            File.write(Content)
    
    def InitializeGit(self, ProjectPath, ProjectConfig):
        """
        Initialize Git repository.
        
        Args:
            ProjectPath: Full path to project directory
            ProjectConfig: Project configuration
        """
        try:
            # Initialize repository
            subprocess.run(['git', 'init'], cwd=ProjectPath, check=True)
            
            # Add all files
            subprocess.run(['git', 'add', '.'], cwd=ProjectPath, check=True)
            
            # Initial commit
            CommitMessage = f"Initial commit for {ProjectConfig.get('ProjectName')}"
            subprocess.run(['git', 'commit', '-m', CommitMessage], cwd=ProjectPath, check=True)
            
            # Check what the default branch name is
            try:
                BranchResult = subprocess.run(['git', 'branch', '--show-current'], 
                              cwd=ProjectPath, check=True, capture_output=True, text=True)
                DefaultBranch = BranchResult.stdout.strip()
                print(f"Using default branch: {DefaultBranch}")
            except Exception as E:
                # Default to main if we can't determine the branch
                DefaultBranch = "main"
                print(f"Could not determine branch name, using '{DefaultBranch}'")
            
            # Add remote if GitHub settings are provided
            GitHubAccount = ProjectConfig.get('GitHubAccount')
            RepoName = ProjectConfig.get('RepositoryName')
            if GitHubAccount and RepoName:
                RemoteUrl = f"https://github.com/{GitHubAccount}/{RepoName}.git"
                subprocess.run(['git', 'remote', 'add', 'origin', RemoteUrl], cwd=ProjectPath, check=True)
                
                # Push to remote if GitHub PAT is provided
                GitHubPAT = ProjectConfig.get('GitHubPAT') or self.Config.GetGitHubToken()
                if GitHubPAT:
                    print(f"Pushing to remote using branch: {DefaultBranch}")
                    self.GitHubManager.PushToRemote(ProjectPath, GitHubAccount, RepoName, GitHubPAT, DefaultBranch)
        
        except Exception as E:
            print(f"Error initializing Git repository: {str(E)}")
    
    def RegisterProject(self, ProjectConfig):
        """
        Register project in Himalaya database.
        
        Args:
            ProjectConfig: Project configuration
        """
        self.DatabaseIntegration.RegisterProject(ProjectConfig)


# Add this code to make the file runnable directly
if __name__ == "__main__":
    # Example code to test the initializer
    from Utils.ConfigManager import ConfigManager
    
    # Create config manager
    Config = ConfigManager()
    
    # Create initializer
    Initializer = ProjectInitializer(Config)
    
    # Example usage - modify these values for your environment
    ProjectConfig = {
        'ProjectName': 'AIDEV-TestProject',
        'Description': 'Test project created by ProjectInitializer',
        'ProjectPath': os.path.expanduser('~/Projects'),  # Adjust this path for your system
        'GitHubAccount': 'YourGitHubUsername',
        'RepositoryName': 'AIDEV-TestProject'
    }
    
    # Initialize project
    print("Starting project initialization...")
    Result = Initializer.InitializeProject(ProjectConfig)
    print(f"Project initialization result: {Result}")
