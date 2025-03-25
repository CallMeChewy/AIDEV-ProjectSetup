# File: test_database_integration.py
# Path: Tests/Unit/test_database_integration.py
# Standard: AIDEV-PascalCase-1.6
# Created: March 24, 2025
# Last Modified: March 24, 2025  4:15PM
# Description: pytest tests for DatabaseIntegration component

"""
pytest tests for DatabaseIntegration component.

This module contains tests that verify the functionality of the DatabaseIntegration
component, which handles database initialization, schema creation, and project 
registration in the Project Himalaya framework.
"""

import os
import sys
import sqlite3
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from Core.DatabaseIntegration import DatabaseIntegration


@pytest.fixture
def mock_config():
    """Create a mock configuration object for testing."""
    MockConfig = MagicMock()
    return MockConfig


@pytest.fixture
def himalaya_db(tmp_path):
    """Create a temporary Himalaya database for testing."""
    # Create temporary Himalaya database file
    HimalayaDbPath = tmp_path / 'Himalaya.db'
    
    # Initialize with empty schema
    Connection = sqlite3.connect(HimalayaDbPath)
    Connection.close()
    
    return HimalayaDbPath


@pytest.fixture
def database_integration(mock_config, himalaya_db):
    """Create a DatabaseIntegration instance for testing."""
    # Configure mock to return path to test Himalaya DB
    mock_config.Get.return_value = str(himalaya_db)
    
    # Create instance
    return DatabaseIntegration(mock_config)


@pytest.fixture
def project_config(tmp_path):
    """Create a sample project configuration for testing."""
    return {
        'ProjectName': 'AIDEV-TestProject',
        'Description': 'Test project for DatabaseIntegration',
        'GitHubAccount': 'TestAccount',
        'RepositoryName': 'TestRepo',
        'ProjectPath': str(tmp_path)
    }


@pytest.fixture
def project_structure(tmp_path, project_config):
    """Create project directory structure for testing."""
    # Create project directory
    ProjectPath = tmp_path / project_config['ProjectName']
    ProjectPath.mkdir(exist_ok=True)
    
    # Create Directories folder
    DirectoriesPath = ProjectPath / 'Directories'
    DirectoriesPath.mkdir(exist_ok=True)
    
    return {
        'ProjectPath': ProjectPath,
        'DirectoriesPath': DirectoriesPath
    }


@pytest.fixture
def db_reporter():
    """Fixture to capture and report database information."""
    Reports = []
    
    def _report_db(DbPath, Description=""):
        """Capture database information for reporting."""
        # Connect to database
        Connection = sqlite3.connect(DbPath)
        Cursor = Connection.cursor()
        
        # Get tables
        Cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        Tables = [row[0] for row in Cursor.fetchall()]
        
        # Build report
        Report = {
            "path": str(DbPath),
            "description": Description,
            "tables": {},
        }
        
        # Get schema and sample data for each table
        for Table in Tables:
            Cursor.execute(f"PRAGMA table_info({Table})")
            Columns = Cursor.fetchall()
            
            Cursor.execute(f"SELECT COUNT(*) FROM {Table}")
            RowCount = Cursor.fetchone()[0]
            
            Cursor.execute(f"SELECT * FROM {Table} LIMIT 3")
            Rows = Cursor.fetchall()
            
            Report["tables"][Table] = {
                "columns": Columns,
                "row_count": RowCount,
                "rows": Rows
            }
        
        Reports.append(Report)
        Connection.close()
        
        # Print some basic info for console output
        print(f"\nDatabase: {DbPath}")
        print(f"Description: {Description}")
        print(f"Tables: {', '.join(Tables)}")
    
    yield _report_db
    
    # After all tests, write detailed report to file
    from datetime import datetime
    
    # Create timestamped report filename
    Timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ReportDir = Path("TestReports")
    ReportDir.mkdir(exist_ok=True)
    ReportPath = ReportDir / f"db_report_{Timestamp}.txt"
    
    # Write report
    with open(ReportPath, "w") as File:
        File.write("=" * 80 + "\n")
        File.write("DATABASE TEST REPORT\n")
        File.write("=" * 80 + "\n")
        File.write(f"Generated: {datetime.now().isoformat()}\n")
        File.write(f"Number of databases: {len(Reports)}\n\n")
        
        for Index, Report in enumerate(Reports, 1):
            File.write("=" * 80 + "\n")
            File.write(f"DATABASE {Index}: {Report['path']}\n")
            File.write("-" * 80 + "\n")
            File.write(f"Description: {Report['description']}\n\n")
            
            for Table, Data in Report["tables"].items():
                File.write(f"TABLE: {Table}\n")
                File.write("-" * 40 + "\n")
                File.write(f"Row count: {Data['row_count']}\n")
                File.write(f"Columns: {len(Data['columns'])}\n\n")
                
                File.write("Schema:\n")
                for Column in Data["columns"]:
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
                        File.write(f"  - {Name} ({Type}) {ConstraintStr}\n")
                    else:
                        File.write(f"  - {Name} ({Type})\n")
                
                File.write("\nSample data:\n")
                if Data["row_count"] > 0:
                    for RowIndex, Row in enumerate(Data["rows"]):
                        File.write(f"  Row {RowIndex + 1}: {Row}\n")
                else:
                    File.write("  No data\n")
                
                File.write("\n")
    
    print(f"\nDatabase report saved to: {ReportPath}")


def test_initialize_project_database(database_integration, project_config, 
                                    project_structure, db_reporter):
    """Test initializing project database with schema and initial data."""
    # Define project database path
    ProjectDbPath = project_structure['DirectoriesPath'] / f"{project_config['ProjectName']}.db"
    
    # Initialize database
    Result = database_integration.InitializeProjectDatabase(ProjectDbPath, project_config)
    
    # Report database state for detailed output
    db_reporter(ProjectDbPath, "After initialization")
    
    # Verify initialization result
    assert Result is True
    assert ProjectDbPath.exists()
    
    # Connect to database and verify tables
    Connection = sqlite3.connect(ProjectDbPath)
    Cursor = Connection.cursor()
    
    # Get all tables
    Cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    Tables = [row[0] for row in Cursor.fetchall()]
    
    # Verify required tables exist
    RequiredTables = [
        'ProjectConfig', 
        'Documentation', 
        'HelpContent', 
        'ProjectState', 
        'SubProjects'
    ]
    
    for Table in RequiredTables:
        assert Table in Tables, f"Required table '{Table}' should exist"
    
    # Verify initial data was inserted
    Cursor.execute("SELECT COUNT(*) FROM ProjectConfig")
    ConfigCount = Cursor.fetchone()[0]
    assert ConfigCount > 0, "ProjectConfig should contain initial data"
    
    Cursor.execute("SELECT COUNT(*) FROM ProjectState")
    StateCount = Cursor.fetchone()[0]
    assert StateCount > 0, "ProjectState should contain initial data"
    
    Connection.close()


def test_create_database_link(database_integration, project_config, 
                             project_structure, himalaya_db):
    """Test creating a symbolic link or copy to the Himalaya database."""
    # Call method under test
    Result = database_integration.CreateDatabaseLink(
        project_structure['ProjectPath'], 
        project_config
    )
    
    # Verify link was created
    assert Result is True
    
    LinkPath = project_structure['DirectoriesPath'] / 'Himalaya.db'
    assert LinkPath.exists(), "Link to Himalaya database should exist"
    
    # Check if it's a link or copy - either is acceptable
    LinkType = "Symbolic link" if os.path.islink(LinkPath) else "File copy"
    print(f"Link type: {LinkType}")


def test_register_project(database_integration, project_config, himalaya_db, db_reporter):
    """Test registering a project in the Himalaya database."""
    # Call method under test
    Result = database_integration.RegisterProject(project_config)
    
    # Report Himalaya database state for detailed output
    db_reporter(himalaya_db, "After project registration")
    
    # Verify registration result
    assert Result is True
    
    # Connect to Himalaya database to verify project registration
    Connection = sqlite3.connect(himalaya_db)
    Cursor = Connection.cursor()
    
    # Check if project table exists
    Cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='project'")
    TableExists = Cursor.fetchone() is not None
    
    assert TableExists, "Project table should be created in Himalaya database"
    
    if TableExists:
        # Check if project was registered
        Cursor.execute("SELECT * FROM project WHERE name=?", (project_config['ProjectName'],))
        ProjectRecord = Cursor.fetchone()
        
        assert ProjectRecord is not None, "Project should be registered in Himalaya database"
    
    Connection.close()


def test_full_workflow(database_integration, project_config, 
                      project_structure, himalaya_db, db_reporter):
    """Test full workflow of project database setup and registration."""
    # Define project database path
    ProjectDbPath = project_structure['DirectoriesPath'] / f"{project_config['ProjectName']}.db"
    
    # Step 1: Initialize project database
    Result1 = database_integration.InitializeProjectDatabase(ProjectDbPath, project_config)
    assert Result1 is True
    
    # Step 2: Create database link
    Result2 = database_integration.CreateDatabaseLink(
        project_structure['ProjectPath'], 
        project_config
    )
    assert Result2 is True
    
    # Step 3: Register project
    Result3 = database_integration.RegisterProject(project_config)
    assert Result3 is True
    
    # Report database states
    db_reporter(ProjectDbPath, "Project database after full workflow")
    db_reporter(himalaya_db, "Himalaya database after full workflow")
    
    # Verify end state
    assert ProjectDbPath.exists()
    assert (project_structure['DirectoriesPath'] / 'Himalaya.db').exists()
    
    # Verify Himalaya DB registration
    Connection = sqlite3.connect(himalaya_db)
    Cursor = Connection.cursor()
    Cursor.execute("SELECT * FROM project WHERE name=?", (project_config['ProjectName'],))
    assert Cursor.fetchone() is not None
    Connection.close()


if __name__ == "__main__":
    print("This script contains pytest tests and should be run using the pytest command.")
    print("To run these tests, use:")
    print("  pytest Tests/Unit/test_database_integration.py -v")
    print("\nTo generate HTML reports, use:")
    print("  pytest Tests/Unit/test_database_integration.py --html=TestReports/report.html")
