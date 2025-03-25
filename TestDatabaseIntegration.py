# File: TestDatabaseIntegration.py
# Path: Tests/Unit/TestDatabaseIntegration.py
# Standard: AIDEV-PascalCase-1.6
# Created: March 24, 2025
# Last Modified: March 24, 2025  2:30PM
# Description: Unit tests for the DatabaseIntegration component

"""
Unit tests for DatabaseIntegration component.

This module contains tests that verify the functionality of the DatabaseIntegration
component, which handles database initialization, schema creation, and project 
registration in the Project Himalaya framework.
"""

import os
import sys
import unittest
import tempfile
import sqlite3
from pathlib import Path
from unittest.mock import MagicMock, patch
import shutil

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from Core.DatabaseIntegration import DatabaseIntegration


class TestDatabaseIntegration(unittest.TestCase):
    """Test cases for DatabaseIntegration component."""
    
    def setUp(self):
        """Set up test environment with mock configuration and temporary directories."""
        # Create temporary directories and files
        self.TempDir = Path(tempfile.mkdtemp())
        
        # Output test environment information
        print(f"\n============================================================")
        print(f"Test Environment Information")
        print(f"------------------------------------------------------------")
        print(f"Test directory: {self.TempDir}")
        print(f"Created at: {self.GetCurrentTimestamp()}")
        print(f"============================================================")
        
        # Create temporary database files
        self.HimalayaDbPath = self.TempDir / 'Himalaya.db'
        
        # Create empty Himalaya database for testing
        Connection = sqlite3.connect(self.HimalayaDbPath)
        Connection.close()
        print(f"Created mock Himalaya database at: {self.HimalayaDbPath}")
        
        # Mock ConfigManager
        self.MockConfig = MagicMock()
        self.MockConfig.Get.return_value = str(self.HimalayaDbPath)
        
        # Create DatabaseIntegration with mock config
        self.DatabaseIntegration = DatabaseIntegration(self.MockConfig)
        
        # Sample project config for testing
        self.ProjectConfig = {
            'ProjectName': 'AIDEV-TestProject',
            'Description': 'Test project for DatabaseIntegration',
            'GitHubAccount': 'TestAccount',
            'RepositoryName': 'TestRepo',
            'ProjectPath': str(self.TempDir)
        }
        
        # Create project directory
        self.ProjectPath = self.TempDir / self.ProjectConfig['ProjectName']
        self.ProjectPath.mkdir(exist_ok=True)
        
        # Create Directories folder
        self.DirectoriesPath = self.ProjectPath / 'Directories'
        self.DirectoriesPath.mkdir(exist_ok=True)
    
    def tearDown(self):
        """Clean up test environment after test execution."""
        print(f"\n============================================================")
        print(f"Test Cleanup")
        print(f"------------------------------------------------------------")
        print(f"Removing test directory: {self.TempDir}")
        print(f"Completed at: {self.GetCurrentTimestamp()}")
        print(f"============================================================")
        shutil.rmtree(self.TempDir)
    
    def GetCurrentTimestamp(self):
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def PrintTableInfo(self, Cursor, TableName):
        """Print schema and sample data for a table."""
        print(f"\n  Table: {TableName}")
        print(f"  -----------------------------------------------")
        
        # Print schema
        Cursor.execute(f"PRAGMA table_info({TableName})")
        Columns = Cursor.fetchall()
        print(f"  Schema ({len(Columns)} columns):")
        for Column in Columns:
            # Column structure: (cid, name, type, notnull, dflt_value, pk)
            ColumnId, Name, Type, NotNull, DefaultValue, PrimaryKey = Column
            Constraints = []
            if PrimaryKey:
                Constraints.append("PRIMARY KEY")
            if NotNull:
                Constraints.append("NOT NULL")
            if DefaultValue is not None:
                Constraints.append(f"DEFAULT {DefaultValue}")
                
            ConstraintStr = " ".join(Constraints)
            if ConstraintStr:
                print(f"    - {Name} ({Type}) {ConstraintStr}")
            else:
                print(f"    - {Name} ({Type})")
        
        # Print row count
        Cursor.execute(f"SELECT COUNT(*) FROM {TableName}")
        RowCount = Cursor.fetchone()[0]
        print(f"\n  Data: {RowCount} rows")
        
        # Print sample data if available
        if RowCount > 0:
            print(f"  Sample data (up to 3 rows):")
            Cursor.execute(f"SELECT * FROM {TableName} LIMIT 3")
            Rows = Cursor.fetchall()
            for RowIndex, Row in enumerate(Rows):
                print(f"    Row {RowIndex + 1}: {Row}")
    
    def test_InitializeProjectDatabase(self):
        """Test initializing project database with schema and initial data."""
        # Define project database path
        ProjectDbPath = self.DirectoriesPath / f"{self.ProjectConfig['ProjectName']}.db"
        
        print(f"\n============================================================")
        print(f"Test: Initialize Project Database")
        print(f"------------------------------------------------------------")
        print(f"Project database path: {ProjectDbPath}")
        
        # Initialize database
        Result = self.DatabaseIntegration.InitializeProjectDatabase(ProjectDbPath, self.ProjectConfig)
        
        # Verify initialization result
        self.assertTrue(Result, "Database initialization should return True")
        self.assertTrue(ProjectDbPath.exists(), "Database file should exist")
        print(f"Database initialization successful: {Result}")
        print(f"Database file size: {ProjectDbPath.stat().st_size} bytes")
        
        # Connect to database and verify tables
        Connection = sqlite3.connect(ProjectDbPath)
        Cursor = Connection.cursor()
        
        # Get all tables
        Cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        Tables = [row[0] for row in Cursor.fetchall()]
        
        print(f"\nDatabase contains {len(Tables)} tables:")
        for TableName in Tables:
            self.PrintTableInfo(Cursor, TableName)
        
        # Verify required tables exist
        RequiredTables = [
            'ProjectConfig', 
            'Documentation', 
            'HelpContent', 
            'ProjectState', 
            'SubProjects'
        ]
        
        for Table in RequiredTables:
            self.assertIn(Table, Tables, f"Required table '{Table}' should exist")
        
        # Verify initial data was inserted
        Cursor.execute("SELECT COUNT(*) FROM ProjectConfig")
        ConfigCount = Cursor.fetchone()[0]
        self.assertGreater(ConfigCount, 0, "ProjectConfig should contain initial data")
        
        Cursor.execute("SELECT COUNT(*) FROM ProjectState")
        StateCount = Cursor.fetchone()[0]
        self.assertGreater(StateCount, 0, "ProjectState should contain initial data")
        
        Connection.close()
    
    def test_CreateDatabaseLink(self):
        """Test creating a symbolic link or copy to the Himalaya database."""
        print(f"\n============================================================")
        print(f"Test: Create Database Link")
        print(f"------------------------------------------------------------")
        
        # Call method under test
        Result = self.DatabaseIntegration.CreateDatabaseLink(self.ProjectPath, self.ProjectConfig)
        
        # Verify link was created
        self.assertTrue(Result, "CreateDatabaseLink should return True")
        
        LinkPath = self.DirectoriesPath / 'Himalaya.db'
        self.assertTrue(LinkPath.exists(), "Link to Himalaya database should exist")
        
        print(f"Link creation successful: {Result}")
        print(f"Link path: {LinkPath}")
        print(f"Link type: {'Symbolic link' if os.path.islink(LinkPath) else 'File copy'}")
        print(f"Link size: {LinkPath.stat().st_size} bytes")
    
    def test_RegisterProject(self):
        """Test registering a project in the Himalaya database."""
        print(f"\n============================================================")
        print(f"Test: Register Project")
        print(f"------------------------------------------------------------")
        
        # Call method under test
        Result = self.DatabaseIntegration.RegisterProject(self.ProjectConfig)
        
        # Verify registration
        self.assertTrue(Result, "RegisterProject should return True")
        
        # Connect to Himalaya database to verify project registration
        Connection = sqlite3.connect(self.HimalayaDbPath)
        Cursor = Connection.cursor()
        
        # Check if project table exists
        Cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='project'")
        TableExists = Cursor.fetchone() is not None
        
        self.assertTrue(TableExists, "Project table should be created in Himalaya database")
        
        if TableExists:
            # Check if project was registered
            Cursor.execute("SELECT * FROM project WHERE name=?", (self.ProjectConfig['ProjectName'],))
            ProjectRecord = Cursor.fetchone()
            
            self.assertIsNotNone(ProjectRecord, "Project should be registered in Himalaya database")
            
            if ProjectRecord:
                # Display project record
                Cursor.execute("PRAGMA table_info(project)")
                Columns = [column[1] for column in Cursor.fetchall()]
                
                print(f"Project registered in Himalaya database:")
                for i, Column in enumerate(Columns):
                    print(f"  {Column}: {ProjectRecord[i]}")
        
        Connection.close()


if __name__ == '__main__':
    # Setup output capture to both console and file
    import sys
    from datetime import datetime
    from io import StringIO
    import os
    
    # Create timestamped filename for test report
    Timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ReportFileName = f"test_report_{Timestamp}.txt"
    
    # Use absolute path to project root TestReports directory
    # This ensures reports are saved outside the temporary test directory
    ProjectRoot = os.environ.get('PROJECT_ROOT')
    if not ProjectRoot:
        # Default to a location relative to the script, outside any temp dirs
        ProjectRoot = Path(__file__).resolve().parent.parent.parent
        
    ReportDir = Path(ProjectRoot) / "TestReports"
    ReportPath = ReportDir / ReportFileName
    
    # Ensure TestReports directory exists
    ReportDir.mkdir(exist_ok=True, parents=True)
    
    print(f"\n============================================================")
    print(f"Test Report Configuration")
    print(f"------------------------------------------------------------")
    print(f"Report will be saved to: {ReportPath}")
    print(f"This location persists after test completion")
    print(f"============================================================")
    
    # Create a custom test runner that captures output
    class TestRunner:
        def __init__(self, ReportPath):
            self.ReportPath = ReportPath
            self.OutputStream = StringIO()
            self.OriginalStdout = sys.stdout
            
        def __enter__(self):
            # Redirect stdout to our string buffer
            sys.stdout = self.__class__.TeeOutput(self.OriginalStdout, self.OutputStream)
            return self
            
        def __exit__(self, exc_type, exc_val, exc_tb):
            # Restore original stdout
            sys.stdout = self.OriginalStdout
            
            # Write captured output to file
            with open(self.ReportPath, 'w') as f:
                f.write(self.OutputStream.getvalue())
                
            print(f"\nTest report saved to: {self.ReportPath}")
            
        class TeeOutput:
            """Class to duplicate output to both console and string buffer."""
            def __init__(self, original_stdout, string_buffer):
                self.original_stdout = original_stdout
                self.string_buffer = string_buffer
                
            def write(self, text):
                self.original_stdout.write(text)
                self.string_buffer.write(text)
                
            def flush(self):
                self.original_stdout.flush()
    
    # Run tests with output capture
    with TestRunner(ReportPath):
        unittest.main(exit=False)
