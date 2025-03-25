# File: ConfigManager.py
# Path: AIDEV-ProjectSetup/Utils/ConfigManager.py
# Standard: AIDEV-PascalCase-1.6
# Created: 2025-03-23
# Last Modified: 2025-03-24  3:45PM
# Description: Configuration management utility

"""
Configuration management utility.

This module provides functionality for managing application configuration,
including loading from files and environment variables.
"""

import os
import json
import re
from pathlib import Path
from dotenv import load_dotenv

class ConfigManager:
    """Configuration management utility."""
    
    def __init__(self, ConfigFile=None):
        """
        Initialize configuration manager.
        
        Args:
            ConfigFile: Optional path to configuration file
        """
        # Determine base path - the root directory of the application
        self.BasePath = Path(__file__).parent.parent
        
        # Create Resources/Templates directory if it doesn't exist
        self.TemplatesPath = self.BasePath / "Resources" / "Templates"
        os.makedirs(self.TemplatesPath, exist_ok=True)
        
        # Default configuration
        self.Config = {
            "DefaultGitHubAccount": "CallMeChewy",
            "DefaultStructure": self.GetDefaultStructure(),
            "DatabasePath": str(self.GetUserConfigDir() / "Himalaya.db"),
            "TemplatesPath": str(self.TemplatesPath)
        }
        
        # Load environment variables - make sure to load from project root
        EnvPath = self.BasePath / ".env"
        print(f"Looking for .env file at: {EnvPath}")
        if os.path.exists(EnvPath):
            load_dotenv(dotenv_path=EnvPath)
            print("Loaded .env file")
        else:
            load_dotenv()  # Load from default locations
            print("No .env file found at project root, checking default locations")
        
        # Check if GITHUB_PAT is loaded
        GitHubPAT = os.environ.get('GITHUB_PAT')
        if GitHubPAT:
            print("GitHub PAT found in environment variables")
        else:
            print("GitHub PAT not found in environment variables")
            
        # Load configuration file if provided
        if ConfigFile and os.path.exists(ConfigFile):
            self.LoadFromFile(ConfigFile)
        
        # Override with environment variables
        self.LoadFromEnvironment()
    
    def GetUserConfigDir(self):
        """
        Get user configuration directory.
        
        Returns:
            Path: Path to user configuration directory
        """
        # Use platform-specific user config directory
        if os.name == 'nt':  # Windows
            ConfigDir = Path(os.environ.get('APPDATA', '.')) / "ProjectHimalaya"
        else:  # Linux/Mac
            ConfigDir = Path.home() / ".config" / "ProjectHimalaya"
        
        # Create directory if it doesn't exist
        os.makedirs(ConfigDir, exist_ok=True)
        
        return ConfigDir
    
    def GetDefaultStructure(self):
        """
        Get default directory structure.
        
        Returns:
            str: Default directory structure
        """
        return """
.
├── Core
├── Docs
│   └── API
├── GUI
├── LICENSE
├── Models
├── README.md
├── requirements.txt
├── Scripts
├── SysUtils
├── Tests
└── Utils
"""
    
    def LoadFromFile(self, FilePath):
        """
        Load configuration from JSON file.
        
        Args:
            FilePath: Path to configuration file
        """
        try:
            with open(FilePath, 'r') as File:
                FileConfig = json.load(File)
                self.Config.update(FileConfig)
        except Exception as E:
            print(f"Error loading configuration file: {str(E)}")
    
    def LoadFromEnvironment(self):
        """Load configuration from environment variables."""
        # Pattern for environment variables: AIDEV_PROJECT_SETUP_*
        EnvPattern = re.compile(r'^AIDEV_PROJECT_SETUP_(.+)$')
        
        for Key, Value in os.environ.items():
            Match = EnvPattern.match(Key)
            if Match:
                # Convert to camel case
                ConfigKey = Match.group(1).lower()
                ConfigKey = ''.join(
                    word.capitalize() if i > 0 else word.lower()
                    for i, word in enumerate(ConfigKey.split('_'))
                )
                
                # Update configuration
                self.Config[ConfigKey] = Value
        
        # Special handling for GitHub PAT
        if 'GITHUB_PAT' in os.environ:
            self.Config['GitHubPAT'] = os.environ['GITHUB_PAT']
    
    def Get(self, Key, Default=None):
        """
        Get configuration value.
        
        Args:
            Key: Configuration key
            Default: Default value if key doesn't exist
            
        Returns:
            Configuration value or default if not found
        """
        return self.Config.get(Key, Default)
    
    def Set(self, Key, Value):
        """
        Set configuration value.
        
        Args:
            Key: Configuration key
            Value: Configuration value
        """
        self.Config[Key] = Value
    
    def GetGitHubToken(self):
        """
        Get GitHub personal access token.
        
        Returns:
            str: GitHub PAT from environment or None
        """
        # Try to get from Config first (which may have loaded from .env)
        Token = self.Config.get('GitHubPAT')
        if Token:
            return Token
            
        # Try environment directly as fallback
        return os.environ.get('GITHUB_PAT')
    
    def SaveToFile(self, FilePath):
        """
        Save configuration to JSON file.
        
        Args:
            FilePath: Path to configuration file
        """
        try:
            with open(FilePath, 'w') as File:
                json.dump(self.Config, File, indent=2)
        except Exception as E:
            print(f"Error saving configuration file: {str(E)}")


# For testing
if __name__ == "__main__":
    config = ConfigManager()
    print("\nConfiguration Test:")
    print(f"GitHub Token: {'Found' if config.GetGitHubToken() else 'Not Found'}")
    print(f"Templates Path: {config.Get('TemplatesPath')}")
    print(f"Database Path: {config.Get('DatabasePath')}")
