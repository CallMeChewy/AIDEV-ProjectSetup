# File: DatabaseIntegration.py
# Path: AIDEV-ProjectSetup/Core/DatabaseIntegration.py
# Standard: AIDEV-PascalCase-1.6
# Created: 2025-03-23
# Last Modified: 2025-03-24  1:15PM
# Description: Database integration functionality

"""
Database integration functionality.

This module provides functionality for interacting with the Himalaya database
and setting up project-specific databases.
"""

import os
import sqlite3
from pathlib import Path
from datetime import datetime
import platform

class DatabaseIntegration:
    """Database integration functionality."""
    
    def __init__(self, ConfigManager):
        """
        Initialize DatabaseIntegration.
        
        Args:
            ConfigManager: Configuration manager instance
        """
        self.Config = ConfigManager
        self.HimalayaDbPath = self.Config.Get('DatabasePath')
        
        # Initialize Himalaya database if it doesn't exist
        self.InitializeHimalayaDatabase()
    
    def InitializeHimalayaDatabase(self):
        """Initialize Himalaya core database if it doesn't exist."""
        if not os.path.exists(self.HimalayaDbPath):
            try:
                # Ensure parent directory exists
                os.makedirs(os.path.dirname(self.HimalayaDbPath), exist_ok=True)
                
                # Connect to database (creates if not exists)
                Connection = sqlite3.connect(self.HimalayaDbPath)
                Cursor = Connection.cursor()
                
                # Create core tables according to the schema in STANDARD-DatabaseSchema.md
                self.CreateProjectTable(Cursor)
                self.CreateComponentTable(Cursor)
                self.CreateStandardTable(Cursor)
                self.CreateValidationRuleTable(Cursor)
                
                # Commit changes
                Connection.commit()
                Connection.close()
                
                print(f"Initialized Himalaya database at {self.HimalayaDbPath}")
                
            except Exception as E:
                print(f"Error initializing Himalaya database: {str(E)}")
    
    def CreateProjectTable(self, Cursor):
        """Create project table in Himalaya database."""
        Cursor.execute('''
        CREATE TABLE IF NOT EXISTS project (
            project_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            path TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            version INTEGER NOT NULL DEFAULT 1,
            is_active INTEGER NOT NULL DEFAULT 1,
            
            UNIQUE(name)
        )
        ''')
    
    def CreateComponentTable(self, Cursor):
        """Create component table in Himalaya database."""
        Cursor.execute('''
        CREATE TABLE IF NOT EXISTS component (
            component_id TEXT PRIMARY KEY,
            project_id_fk TEXT NOT NULL,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            layer INTEGER NOT NULL,
            description TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            version INTEGER NOT NULL DEFAULT 1,
            is_active INTEGER NOT NULL DEFAULT 1,
            
            FOREIGN KEY (project_id_fk) REFERENCES project(project_id),
            UNIQUE(project_id_fk, name)
        )
        ''')
    
    def CreateStandardTable(self, Cursor):
        """Create standard table in Himalaya database."""
        Cursor.execute('''
        CREATE TABLE IF NOT EXISTS standard (
            standard_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            version TEXT NOT NULL,
            description TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            is_active INTEGER NOT NULL DEFAULT 1,
            
            UNIQUE(name, version)
        )
        ''')
    
    def CreateValidationRuleTable(self, Cursor):
        """Create validation rule table in Himalaya database."""
        Cursor.execute('''
        CREATE TABLE IF NOT EXISTS validation_rule (
            rule_id TEXT PRIMARY KEY,
            standard_id_fk TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            rule_type TEXT NOT NULL,
            rule_pattern TEXT NOT NULL,
            severity TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            is_active INTEGER NOT NULL DEFAULT 1,
            
            FOREIGN KEY (standard_id_fk) REFERENCES standard(standard_id),
            UNIQUE(standard_id_fk, name)
        )
        ''')
    
    def InitializeProjectDatabase(self, DbPath, ProjectConfig):
        """
        Initialize project-specific database.
        
        Args:
            DbPath: Path to project database
            ProjectConfig: Project configuration
            
        Returns:
            bool: True if initialization was successful
        """
        try:
            # Ensure parent directory exists
            os.makedirs(os.path.dirname(DbPath), exist_ok=True)
            
            # Connect to database (creates if not exists)
            Connection = sqlite3.connect(DbPath)
            Cursor = Connection.cursor()
            
            # Enable foreign keys
            Cursor.execute("PRAGMA foreign_keys = ON")
            
            # Create schema version table first
            Cursor.execute('''
            CREATE TABLE IF NOT EXISTS schema_version (
                version INTEGER PRIMARY KEY,
                applied_at TEXT NOT NULL,
                description TEXT NOT NULL
            )
            ''')
            
            # Insert initial schema version
            Cursor.execute(
                "INSERT OR IGNORE INTO schema_version (version, applied_at, description) VALUES (?, ?, ?)",
                (1, datetime.now().isoformat(), "Initial schema creation")
            )
            
            # Create core tables
            self.CreateProjectConfigTable(Cursor)
            self.CreateDocumentationTable(Cursor)
            self.CreateHelpContentTable(Cursor)
            self.CreateProjectStateTable(Cursor)
            self.CreateSubProjectsTable(Cursor)
            
            # Insert initial data
            self.InsertInitialData(Cursor, ProjectConfig)
            
            # Commit changes
            Connection.commit()
            Connection.close()
            
            return True
            
        except Exception as E:
            print(f"Error initializing project database: {str(E)}")
            return False
    
    def CreateProjectConfigTable(self, Cursor):
        """
        Create project configuration table.
        
        Args:
            Cursor: Database cursor
        """
        Cursor.execute('''
        CREATE TABLE IF NOT EXISTS ProjectConfig (
            ConfigId INTEGER PRIMARY KEY AUTOINCREMENT,
            ConfigKey TEXT NOT NULL UNIQUE,
            ConfigValue TEXT NOT NULL,
            ConfigType TEXT NOT NULL,
            Description TEXT,
            LastModified TEXT NOT NULL
        )
        ''')
    
    def CreateDocumentationTable(self, Cursor):
        """
        Create documentation table.
        
        Args:
            Cursor: Database cursor
        """
        Cursor.execute('''
        CREATE TABLE IF NOT EXISTS Documentation (
            DocId INTEGER PRIMARY KEY AUTOINCREMENT,
            DocType TEXT NOT NULL,
            Title TEXT NOT NULL,
            Content TEXT NOT NULL,
            Format TEXT NOT NULL,
            Tags TEXT,
            CreationDate TEXT NOT NULL,
            LastModified TEXT NOT NULL
        )
        ''')
    
    def CreateHelpContentTable(self, Cursor):
        """
        Create help content table.
        
        Args:
            Cursor: Database cursor
        """
        Cursor.execute('''
        CREATE TABLE IF NOT EXISTS HelpContent (
            HelpId INTEGER PRIMARY KEY AUTOINCREMENT,
            Topic TEXT NOT NULL,
            Content TEXT NOT NULL,
            Keywords TEXT,
            RelatedTopics TEXT,
            ContextTriggers TEXT,
            LastModified TEXT NOT NULL
        )
        ''')
    
    def CreateProjectStateTable(self, Cursor):
        """
        Create project state table.
        
        Args:
            Cursor: Database cursor
        """
        Cursor.execute('''
        CREATE TABLE IF NOT EXISTS ProjectState (
            StateId INTEGER PRIMARY KEY AUTOINCREMENT,
            StateName TEXT NOT NULL,
            CurrentPhase TEXT NOT NULL,
            StateData TEXT NOT NULL,
            CreationDate TEXT NOT NULL,
            LastModified TEXT NOT NULL
        )
        ''')
    
    def CreateSubProjectsTable(self, Cursor):
        """
        Create sub-projects table.
        
        Args:
            Cursor: Database cursor
        """
        Cursor.execute('''
        CREATE TABLE IF NOT EXISTS SubProjects (
            SubProjectId INTEGER PRIMARY KEY AUTOINCREMENT,
            SubProjectName TEXT NOT NULL,
            GitHubRepo TEXT,
            Relationship TEXT NOT NULL,
            Active INTEGER NOT NULL DEFAULT 1
        )
        ''')
    
    def InsertInitialData(self, Cursor, ProjectConfig):
        """
        Insert initial data into the database.
        
        Args:
            Cursor: Database cursor
            ProjectConfig: Project configuration
        """
        # Current timestamp
        Now = datetime.now().isoformat()
        
        # Insert project configuration
        Cursor.execute(
            """
            INSERT INTO ProjectConfig 
            (ConfigKey, ConfigValue, ConfigType, Description, LastModified)
            VALUES (?, ?, ?, ?, ?)
            """,
            ('ProjectName', ProjectConfig.get('ProjectName', ''), 'STRING', 
             'Project name', Now)
        )
        
        Cursor.execute(
            """
            INSERT INTO ProjectConfig 
            (ConfigKey, ConfigValue, ConfigType, Description, LastModified)
            VALUES (?, ?, ?, ?, ?)
            """,
            ('ProjectDescription', ProjectConfig.get('Description', ''), 'STRING', 
             'Project description', Now)
        )
        
        Cursor.execute(
            """
            INSERT INTO ProjectConfig 
            (ConfigKey, ConfigValue, ConfigType, Description, LastModified)
            VALUES (?, ?, ?, ?, ?)
            """,
            ('GitHubRepo', f"{ProjectConfig.get('GitHubAccount', '')}/{ProjectConfig.get('RepositoryName', '')}", 
             'STRING', 'GitHub repository', Now)
        )
        
        # Insert initial project state
        Cursor.execute(
            """
            INSERT INTO ProjectState 
            (StateName, CurrentPhase, StateData, CreationDate, LastModified)
            VALUES (?, ?, ?, ?, ?)
            """,
            ('Initial', 'Setup', '{}', Now, Now)
        )
        
        # Insert initial documentation
        Cursor.execute(
            """
            INSERT INTO Documentation 
            (DocType, Title, Content, Format, Tags, CreationDate, LastModified)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            ('Setup', 'Project Setup Documentation', 
             f"# {ProjectConfig.get('ProjectName', '')}\n\nProject setup completed on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.", 
             'Markdown', 'setup,documentation', Now, Now)
        )
    
    def CreateDatabaseLink(self, ProjectPath, ProjectConfig):
        """
        Create symbolic link to Himalaya database.
        
        Args:
            ProjectPath: Path to project directory
            ProjectConfig: Project configuration
            
        Returns:
            bool: True if link creation was successful
        """
        try:
            # Target directory for link
            DirectoriesPath = ProjectPath / 'Directories'
            DirectoriesPath.mkdir(exist_ok=True)
            
            # Link path
            LinkPath = DirectoriesPath / 'Himalaya.db'
            
            # Check if we're running on Windows
            if platform.system() == 'Windows':
                # Windows requires admin privileges for symlinks, use copy instead
                import shutil
                shutil.copy2(self.HimalayaDbPath, LinkPath)
                print(f"Created copy of Himalaya database at {LinkPath}")
            else:
                # Create symbolic link
                if LinkPath.exists():
                    LinkPath.unlink()
                os.symlink(self.HimalayaDbPath, LinkPath)
                print(f"Created symbolic link to Himalaya database at {LinkPath}")
            
            return True
            
        except Exception as E:
            print(f"Error creating database link: {str(E)}")
            return False
    
    def RegisterProject(self, ProjectConfig):
        """
        Register project in Himalaya database.
        
        Args:
            ProjectConfig: Project configuration
            
        Returns:
            bool: True if registration was successful
        """
        try:
            # Connect to Himalaya database
            Connection = sqlite3.connect(self.HimalayaDbPath)
            Cursor = Connection.cursor()
            
            # Enable foreign keys
            Cursor.execute("PRAGMA foreign_keys = ON")
            
            # Check if projects table exists, create if not
            Cursor.execute('''
            CREATE TABLE IF NOT EXISTS project (
                project_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                path TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                version INTEGER NOT NULL DEFAULT 1,
                is_active INTEGER NOT NULL DEFAULT 1,
                
                UNIQUE(name)
            )
            ''')
            
            # Generate unique project ID
            import uuid
            ProjectId = f"project-{uuid.uuid4().hex[:8]}"
            
            # Current timestamp
            Now = datetime.now().isoformat()
            
            # Insert project
            Cursor.execute(
                """
                INSERT OR REPLACE INTO project 
                (project_id, name, description, path, created_at, updated_at, version, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    ProjectId, 
                    ProjectConfig.get('ProjectName', ''),
                    ProjectConfig.get('Description', ''),
                    str(Path(ProjectConfig.get('ProjectPath', '')) / ProjectConfig.get('ProjectName', '')),
                    Now,
                    Now,
                    1,
                    1
                )
            )
            
            # Commit changes
            Connection.commit()
            Connection.close()
            
            return True
            
        except Exception as E:
            print(f"Error registering project in Himalaya database: {str(E)}")
            return False
