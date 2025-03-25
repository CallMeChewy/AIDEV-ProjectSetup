# File: test_integration.py
# Path: AIDEV-ProjectSetup/Tests/IntegrationTests/test_integration.py
# Standard: AIDEV-PascalCase-1.6
# Created: 2025-03-23
# Last Modified: 2025-03-23  4:20PM
# Description: Integration tests for AIDEV-ProjectSetup application

"""
Integration test suite for AIDEV-ProjectSetup.

This module contains integration tests that verify the interaction between
multiple components of the AIDEV-ProjectSetup application.
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
from Core.GitHubManager import GitHubManager
from Core.DatabaseIntegration import DatabaseIntegration
from Core.ProjectInitializer import ProjectInitializer


class TestEndToEndProjectCreation(unittest.TestCase):
    """Integration test for end-to-end project creation process."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directories
        self.TempProjectDir = Path(tempfile.mkdtemp())
        self.TempConfigDir = Path(tempfile.mkdtemp())
        
        # Create mock Himalaya database
        self.HimalayaDbPath = self.TempConfigDir / 'Himalaya.db'
        
        # Mock configuration
        self.MockConfig = MagicMock()
        self.MockConfig.Get.side_effect = self.mock_config_get
        self.MockConfig.GetGitHubToken.return_value = 'mock_token'
        
        # Sample project config
        self.ProjectConfig = {
            'ProjectName': 'AIDEV-TestIntegration',
            'Description': 'Integration test project',
            'GitHubAccount': 'TestAccount',
            'RepositoryName': 'TestRepo',
            'ProjectPath': str(self.TempProjectDir),
            'DirectoryStructure': {
                'Core': {},
                'Docs': {'API': {}},
                'Utils': {},
                'Tests': {'UnitTests': {}, 'IntegrationTests': {}}
            }
        }
        
        # Create initializer with mock config
        self.Initializer = ProjectInitializer(self.MockConfig)
        
        # Mock GitHub responses
        self.github_patcher = patch('requests.get')
        self.mock_github_get = self.github_patcher.start()
        self.mock_github_response = MagicMock()
        self.mock_github_response.status_code = 200
        self.mock_github_response.json.return_value = {'size': 0}
        self.mock_github_get.return_value = self.mock_github_response
        
        # Mock subprocess for git operations
        self.subprocess_patcher = patch('subprocess.run')
        self.mock_subprocess = self.subprocess_patcher.start()
        self.mock_subprocess.return_value = MagicMock()
    
    def mock_config_get(self, key, default=None):
        """Mock implementation of ConfigManager.Get."""
        if key == 'DatabasePath':
            return str(self.HimalayaDbPath)
        elif key == 'TemplatesPath':
            return str(Path(__file__).parent.parent.parent / 'Resources' / 'Templates')
        elif key == 'DefaultStructure':
            return """
            .
            ├── Core
            ├── Docs
            │   └── API
            ├── Utils
            └── Tests
            """
        return default
    
    def tearDown(self):
        """Clean up test environment."""
        # Stop patchers
        self.github_patcher.stop()
        self.subprocess_patcher.stop()
        
        # Remove temporary directories
        shutil.rmtree(self.TempProjectDir)
        shutil.rmtree(self.TempConfigDir)
    
    def test_end_to_end_project_creation(self):
        """Test end-to-end project creation process."""
        # Initialize project
        Result = self.Initializer.InitializeProject(self.ProjectConfig)
        
        # Verify result
        self.assertTrue(Result, "Project initialization failed")
        
        # Verify project directory structure
        ProjectPath = self.TempProjectDir / 'AIDEV-TestIntegration'
        self.assertTrue(ProjectPath.exists(), "Project directory not created")
        self.assertTrue((ProjectPath / 'Core').exists(), "Core directory not created")
        self.assertTrue((ProjectPath / 'Docs' / 'API').exists(), "Docs/API directory not created")
        self.assertTrue((ProjectPath / 'Utils').exists(), "Utils directory not created")
        self.assertTrue((ProjectPath / 'Tests' / 'UnitTests').exists(), "Tests/UnitTests directory not created")
        self.assertTrue((ProjectPath / 'Tests' / 'IntegrationTests').exists(), "Tests/IntegrationTests directory not created")
        
        # Verify project files
        self.assertTrue((ProjectPath / 'README.md').exists(), "README.md not created")
        self.assertTrue((ProjectPath / 'LICENSE').exists(), "LICENSE not created")
        self.assertTrue((ProjectPath / '.gitignore').exists(), ".gitignore not created")
        
        # Verify Directories folder was created
        self.assertTrue((ProjectPath / 'Directories').exists(), "Directories folder not created")
        
        # Verify git operations were called
        self.mock_subprocess.assert_called(), "Git operations not performed"


class TestDatabaseIntegrationFlow(unittest.TestCase):
    """Integration test for database integration flow."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directories
        self.TempProjectDir = Path(tempfile.mkdtemp())
        self.TempConfigDir = Path(tempfile.mkdtemp())
        
        # Create Himalaya database
        self.HimalayaDbPath = self.TempConfigDir / 'Himalaya.db'
        Connection = sqlite3.connect(self.HimalayaDbPath)
        Connection.close()
        
        # Mock configuration
        self.MockConfig = MagicMock()
        self.MockConfig.Get.return_value = str(self.HimalayaDbPath)
        
        # Create DatabaseIntegration with mock config
        self.DatabaseIntegration = DatabaseIntegration(self.MockConfig)
        
        # Sample project config
        self.ProjectConfig = {
            'ProjectName': 'AIDEV-DBTest',
            'Description': 'Database integration test',
            'GitHubAccount': 'TestAccount',
            'RepositoryName': 'TestRepo',
            'ProjectPath': str(self.TempProjectDir)
        }
        
        # Create project directory
        self.ProjectPath = self.TempProjectDir / 'AIDEV-DBTest'
        self.ProjectPath.mkdir(parents=True)
        
        # Create Directories folder
        self.DirectoriesPath = self.ProjectPath / 'Directories'
        self.DirectoriesPath.mkdir()
    
    def tearDown(self):
        """Clean up test environment."""
        # Remove temporary directories
        shutil.rmtree(self.TempProjectDir)
        shutil.rmtree(self.TempConfigDir)
    
    def test_database_integration_flow(self):
        """Test full database integration flow."""
        # Create project-specific database
        ProjectDbPath = self.DirectoriesPath / 'AIDEV-DBTest.db'
        Result = self.DatabaseIntegration.InitializeProjectDatabase(ProjectDbPath, self.ProjectConfig)
        self.assertTrue(Result, "Project database initialization failed")
        self.assertTrue(ProjectDbPath.exists(), "Project database file not created")
        
        # Create symbolic link (or copy on Windows) to Himalaya.db
        LinkResult = self.DatabaseIntegration.CreateDatabaseLink(self.ProjectPath, self.ProjectConfig)
        self.assertTrue(LinkResult, "Database link creation failed")
        
        # Check if link (or copy) exists
        self.assertTrue((self.DirectoriesPath / 'Himalaya.db').exists(), "Himalaya.db link not created")
        
        # Register project in Himalaya database
        RegisterResult = self.DatabaseIntegration.RegisterProject(self.ProjectConfig)
        self.assertTrue(RegisterResult, "Project registration failed")
        
        # Verify project registration in Himalaya database
        Connection = sqlite3.connect(self.HimalayaDbPath)
        Cursor = Connection.cursor()
        
        # Check if project table exists
        Cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='project'")
        TableExists = Cursor.fetchone() is not None
        self.assertTrue(TableExists, "Project table not created in Himalaya.db")
        
        # Check if project is registered
        if TableExists:
            Cursor.execute("SELECT * FROM project WHERE name=?", (self.ProjectConfig['ProjectName'],))
            ProjectData = Cursor.fetchone()
            self.assertIsNotNone(ProjectData, "Project not registered in Himalaya.db")
        
        Connection.close()
        
        # Verify project database has required tables
        Connection = sqlite3.connect(ProjectDbPath)
        Cursor = Connection.cursor()
        
        # Check for required tables
        Cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        Tables = [row[0] for row in Cursor.fetchall()]
        
        self.assertIn('ProjectConfig', Tables, "ProjectConfig table not created")
        self.assertIn('Documentation', Tables, "Documentation table not created")
        self.assertIn('HelpContent', Tables, "HelpContent table not created")
        self.assertIn('ProjectState', Tables, "ProjectState table not created")
        self.assertIn('SubProjects', Tables, "SubProjects table not created")
        
        # Check if initial data was inserted
        Cursor.execute("SELECT * FROM ProjectConfig WHERE ConfigKey='ProjectName'")
        ConfigData = Cursor.fetchone()
        self.assertIsNotNone(ConfigData, "Project name not stored in ProjectConfig")
        
        Cursor.execute("SELECT * FROM ProjectState")
        StateData = Cursor.fetchone()
        self.assertIsNotNone(StateData, "Initial state not created in ProjectState")
        
        Cursor.execute("SELECT * FROM Documentation")
        DocData = Cursor.fetchone()
        self.assertIsNotNone(DocData, "Initial documentation not created")
        
        Connection.close()


if __name__ == '__main__':
    unittest.main()
