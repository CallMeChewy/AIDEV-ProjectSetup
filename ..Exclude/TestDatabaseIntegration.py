# Test class for DatabaseIntegration
# You can add this to your test_project_setup.py file

import os
import tempfile
import sqlite3
from pathlib import Path
from unittest.mock import MagicMock
import unittest
import shutil
from Core.DatabaseIntegration import DatabaseIntegration

class TestDatabaseIntegration(unittest.TestCase):
    """Test cases for DatabaseIntegration component."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directories and files
        self.TempDir = Path(tempfile.mkdtemp())
        
        # Create temporary database files
        self.HimalayaDbPath = self.TempDir / 'Himalaya.db'
        
        # Mock ConfigManager
        self.MockConfig = MagicMock()
        self.MockConfig.Get.return_value = str(self.HimalayaDbPath)
        
        # Create DatabaseIntegration with mock config
        self.database_integration = DatabaseIntegration(self.MockConfig)
        
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
        # Create project database file path
        ProjectDbPath = self.TempDir / 'AIDEV-TestProject.db'
        
        # Initialize database
        Result = self.database_integration.InitializeProjectDatabase(ProjectDbPath, self.ProjectConfig)
        
        # Verify initialization
        self.assertTrue(Result)
        
        # Connect to database and verify tables
        Connection = sqlite3.connect(ProjectDbPath)
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
