# File: test_project_setup.py
# Path: AIDEV-ProjectSetup/Tests/UnitTests/test_project_setup.py
# Standard: AIDEV-PascalCase-1.6
# Created: 2025-03-23
# Last Modified: 2025-03-23  4:00PM
# Description: Automated tests for AIDEV-ProjectSetup application

"""
Automated test suite for AIDEV-ProjectSetup.

This module contains tests for core components of the AIDEV-ProjectSetup application,
including directory structure parsing, configuration management, GitHub integration,
and database operations.
"""

import os
import sys
import shutil
import tempfile
import unittest
import sqlite3
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path to import application modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from Utils.ConfigManager import ConfigManager
from Utils.DirectoryParser import DirectoryParser
from Core.GitHubManager import GitHubManager
from Core.DatabaseIntegration import DatabaseIntegration
from Core.ProjectInitializer import ProjectInitializer


class TestDirectoryParser(unittest.TestCase):
    """Test cases for DirectoryParser utility."""
    
    def setUp(self):
        """Set up test environment."""
        self.Parser = DirectoryParser()
        
        # Sample directory structure
        self.SampleStructure = """
        .
        ├── Core
        ├── Docs
        │   └── API
        ├── Utils
        └── Tests
        """
    
    def test_parse_structure(self):
        """Test parsing directory structure from text."""
        # Parse sample structure
        Structure = self.Parser.ParseStructure(self.SampleStructure)
        
        # Verify structure
        self.assertIn('Core', Structure)
        self.assertIn('Docs', Structure)
        self.assertIn('Utils', Structure)
        self.assertIn('Tests', Structure)
        self.assertIn('API', Structure['Docs'])
    
    def test_format_structure(self):
        """Test formatting structure to text."""
        # Parse and then format
        Structure = self.Parser.ParseStructure(self.SampleStructure)
        FormattedLines = self.Parser.FormatStructureToText(Structure)
        
        # Verify formatted text
        self.assertTrue(any('Core' in line for line in FormattedLines))
        self.assertTrue(any('Docs' in line for line in FormattedLines))
        self.assertTrue(any('API' in line for line in FormattedLines))


class TestConfigManager(unittest.TestCase):
    """Test cases for ConfigManager utility."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary config file
        self.TempFile = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.TempFile.write(b'{"TestKey": "TestValue"}')
        self.TempFile.close()
        
        # Create ConfigManager with test file
        self.ConfigManager = ConfigManager(self.TempFile.name)
    
    def tearDown(self):
        """Clean up test environment."""
        os.unlink(self.TempFile.name)
    
    def test_load_from_file(self):
        """Test loading configuration from file."""
        self.assertEqual(self.ConfigManager.Get('TestKey'), 'TestValue')
    
    def test_get_default(self):
        """Test getting value with default."""
        self.assertEqual(self.ConfigManager.Get('NonExistentKey', 'DefaultValue'), 'DefaultValue')
    
    def test_set_value(self):
        """Test setting configuration value."""
        self.ConfigManager.Set('NewKey', 'NewValue')
        self.assertEqual(self.ConfigManager.Get('NewKey'), 'NewValue')
    
    def test_get_user_config_dir(self):
        """Test getting user config directory."""
        ConfigDir = self.ConfigManager.GetUserConfigDir()
        self.assertTrue(isinstance(ConfigDir, Path))
        self.assertTrue(ConfigDir.exists())


class TestDatabaseIntegration(unittest.TestCase):
    """Test cases for DatabaseIntegration component."""
    
    def setUp(self):
        """Set up test environment."""
        # Mock ConfigManager
        self.MockConfig = MagicMock()
        self.MockConfig.Get.return_value = ':memory:'  # Use in-memory database for testing
        
        # Create DatabaseIntegration with mock config
        self.DatabaseIntegration = DatabaseIntegration(self.MockConfig)
        
        # Create temporary directory for project
        self.TempDir = Path(tempfile.mkdtemp())
        
        # Sample project config
        self.ProjectConfig = {
            'ProjectName': 'AIDEV-TestProject',
            'Description': 'Test project description',
            'GitHubAccount': 'TestAccount',
            'RepositoryName': 'TestRepo',
            'ProjectPath': str(self.TempDir)
        }
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.TempDir)
    
    def test_initialize_project_database(self):
        """Test initializing project database."""
        # Create in-memory database for testing
        DbPath = ':memory:'
        
        # Initialize database
        Result = self.DatabaseIntegration.InitializeProjectDatabase(DbPath, self.ProjectConfig)
        
        # Verify initialization
        self.assertTrue(Result)
        
        # Connect to database and verify tables
        Connection = sqlite3.connect(DbPath)
        Cursor = Connection.cursor()
        
        # Check if tables exist
        Cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        Tables = [row[0] for row in Cursor.fetchall()]
        
        self.assertIn('ProjectConfig', Tables)
        self.assertIn('Documentation', Tables)
        self.assertIn('HelpContent', Tables)
        self.assertIn('ProjectState', Tables)
        self.assertIn('SubProjects', Tables)
        
        Connection.close()


class TestGitHubManager(unittest.TestCase):
    """Test cases for GitHubManager component."""
    
    def setUp(self):
        """Set up test environment."""
        # Mock ConfigManager
        self.MockConfig = MagicMock()
        self.MockConfig.GetGitHubToken.return_value = 'mock_token'
        
        # Create GitHubManager with mock config
        self.GitHubManager = GitHubManager(self.MockConfig)
    
    @patch('requests.get')
    def test_validate_repository_not_found(self, MockGet):
        """Test repository validation when repo doesn't exist."""
        # Mock response for non-existent repository
        MockResponse = MagicMock()
        MockResponse.status_code = 404
        MockGet.return_value = MockResponse
        
        # Validate repository
        Result = self.GitHubManager.ValidateRepository('TestAccount', 'NonExistentRepo')
        
        # Verify result
        self.assertEqual(Result['Status'], 'NotFound')
    
    @patch('requests.get')
    def test_validate_repository_non_empty(self, MockGet):
        """Test repository validation when repo is not empty."""
        # Mock response for non-empty repository
        MockResponse = MagicMock()
        MockResponse.status_code = 200
        MockResponse.json.return_value = {'size': 100}
        MockGet.return_value = MockResponse
        
        # Validate repository
        Result = self.GitHubManager.ValidateRepository('TestAccount', 'NonEmptyRepo')
        
        # Verify result
        self.assertEqual(Result['Status'], 'NotEmpty')
    
    @patch('requests.get')
    def test_validate_repository_valid(self, MockGet):
        """Test repository validation when repo is valid."""
        # Mock response for valid repository
        MockResponse = MagicMock()
        MockResponse.status_code = 200
        MockResponse.json.return_value = {'size': 0}
        MockGet.return_value = MockResponse
        
        # Validate repository
        Result = self.GitHubManager.ValidateRepository('TestAccount', 'ValidRepo')
        
        # Verify result
        self.assertEqual(Result['Status'], 'Valid')


class TestProjectInitializer(unittest.TestCase):
    """Test cases for ProjectInitializer component."""
    
    def setUp(self):
        """Set up test environment."""
        # Mock dependencies
        self.MockConfig = MagicMock()
        self.MockGitHub = MagicMock()
        self.MockDatabase = MagicMock()
        
        # Patch dependencies
        self.GitHubPatcher = patch('Core.ProjectInitializer.GitHubManager', return_value=self.MockGitHub)
        self.DatabasePatcher = patch('Core.ProjectInitializer.DatabaseIntegration', return_value=self.MockDatabase)
        
        # Start patchers
        self.MockGitHubClass = self.GitHubPatcher.start()
        self.MockDatabaseClass = self.DatabasePatcher.start()
        
        # Create ProjectInitializer
        self.Initializer = ProjectInitializer(self.MockConfig)
        
        # Create temporary directory for project
        self.TempDir = Path(tempfile.mkdtemp())
        
        # Sample project config
        self.ProjectConfig = {
            'ProjectName': 'AIDEV-TestProject',
            'Description': 'Test project description',
            'GitHubAccount': 'TestAccount',
            'RepositoryName': 'TestRepo',
            'ProjectPath': str(self.TempDir),
            'DirectoryStructure': {
                'Core': {},
                'Docs': {'API': {}},
                'Utils': {}
            }
        }
    
    def tearDown(self):
        """Clean up test environment."""
        # Stop patchers
        self.GitHubPatcher.stop()
        self.DatabasePatcher.stop()
        
        # Remove temporary directory
        shutil.rmtree(self.TempDir)
    
    @patch('Core.ProjectInitializer.subprocess.run')
    def test_initialize_project(self, MockRun):
        """Test project initialization."""
        # Mock subprocess.run
        MockRun.return_value = MagicMock()
        
        # Mock database operations
        self.MockDatabase.InitializeProjectDatabase.return_value = True
        self.MockDatabase.CreateDatabaseLink.return_value = True
        self.MockDatabase.RegisterProject.return_value = True
        
        # Initialize project
        Result = self.Initializer.InitializeProject(self.ProjectConfig)
        
        # Verify result
        self.assertTrue(Result)
        
        # Verify directories were created
        ProjectPath = self.TempDir / 'AIDEV-TestProject'
        self.assertTrue((ProjectPath / 'Core').exists())
        self.assertTrue((ProjectPath / 'Docs').exists())
        self.assertTrue((ProjectPath / 'Docs' / 'API').exists())
        self.assertTrue((ProjectPath / 'Utils').exists())
        
        # Verify database operations were called
        self.MockDatabase.InitializeProjectDatabase.assert_called_once()
        self.MockDatabase.CreateDatabaseLink.assert_called_once()
        self.MockDatabase.RegisterProject.assert_called_once()
        
        # Verify git operations were called
        MockRun.assert_called()  # git init, add, commit


if __name__ == '__main__':
    unittest.main()
