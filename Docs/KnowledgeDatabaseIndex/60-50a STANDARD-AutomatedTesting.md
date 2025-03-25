# STANDARD-AutomatedTesting
**Created: March 24, 2025  3:15PM**
**Last Modified: March 24, 2025  3:15PM**

[Context: Technical_Standards]
[Component: Layer1_Testing]
[Status: Active]
[Version: 1.0]

## 1. Overview

This document defines the standards for automated testing within Project Himalaya and conforming projects. It covers the requirements for test automation, execution, reporting, and integration within the development workflow.

## 2. Automated Testing Requirements

### 2.1 Core Principles

- **Test-First Development**: Tests should be written before or alongside implementation
- **Comprehensive Coverage**: All components must have automated tests
- **Self-Verification**: Tests must assert their own success criteria
- **Output Standardization**: Test output must follow defined formats
- **Report Generation**: Tests must generate machine and human-readable reports
- **Continuous Testing**: Tests must be run automatically on code changes

### 2.2 Test Automation Levels

| Level | Description | Required Coverage | Example Components |
|-------|-------------|-------------------|-------------------|
| L1 | Unit tests | 90% of code | Core module functions |
| L2 | Integration tests | 80% of interfaces | Component interfaces |
| L3 | System tests | All critical paths | End-to-end workflows |
| L4 | Performance tests | Key operations | Database operations |

### 2.3 Test Environment Requirements

- Tests must create and manage their own isolated test environment
- Test environments must be clean before and after test execution
- Environment setup/teardown must be visible in test output
- Tests must not depend on global state or specific machine configurations
- Test outputs (reports, logs) must be stored outside of temporary test environments
- Test environments must be ephemeral while test artifacts must be persistent

## 3. Test Report Requirements

### 3.1 Report Structure

All automated test reports must follow this hierarchical structure:

```
1. Test Execution Summary
   - Test suite name and version
   - Execution timestamp
   - Overall status (Pass/Fail)
   - Test counts (Total, Passed, Failed, Skipped)
   - Execution duration

2. Environment Information
   - Test environment details
   - System configuration
   - Test data locations
   - Relevant configuration settings

3. Test Cases Detail
   For each test case:
   - Test ID and name
   - Status (Pass/Fail/Skip)
   - Execution time
   - Setup information
   - Actions performed
   - Assertions checked
   - Actual vs. expected results
   - Cleanup operations

4. Failure Analysis (if applicable)
   - Failed test details
   - Error messages
   - Stack traces
   - Relevant state information
   - Troubleshooting suggestions

5. Coverage Report
   - Code coverage statistics
   - Component coverage metrics
   - Coverage gaps identified

6. Artifacts References
   - Paths to generated artifacts
   - Log file locations
   - Screenshots (if relevant)
   - Database snapshots (if created)
```

### 3.2 Report Format Standards

#### 3.2.1 Plain Text Format

Text reports must follow these formatting guidelines:

- Clear section headers with separators (e.g., ==== or ----)
- Hierarchical indentation for nested information
- Consistent spacing for readability
- Table-like formatting for structured data
- Standard timestamp format: YYYY-MM-DD HH:MM:SS
- Maximum line width of 100 characters

Example text report formatting:

```
============================================================
TEST EXECUTION SUMMARY
------------------------------------------------------------
Test Suite: DatabaseIntegration Tests
Version: 1.0
Executed: 2025-03-24 10:15:30
Status: PASSED
Tests: 5 total, 5 passed, 0 failed, 0 skipped
Duration: 3.45 seconds

============================================================
ENVIRONMENT INFORMATION
------------------------------------------------------------
Test Directory: /tmp/test_dir_20250324_101530
Python Version: 3.9.12
Database Engine: SQLite 3.36.0

============================================================
TEST CASE DETAIL: test_InitializeProjectDatabase
------------------------------------------------------------
Status: PASSED
Duration: 1.25 seconds

  Setup:
  - Created temporary directory
  - Initialized mock configuration
  
  Actions:
  - Called InitializeProjectDatabase
  - Verified database file created
  - Checked table structure
  - Validated initial data
  
  Results:
  - Database created successfully
  - 5 required tables found
  - Schema validation passed
  - Initial data confirmed
  
  Cleanup:
  - Removed test database
  - Deleted temporary directory
```

#### 3.2.2 JSON Format

Machine-readable reports must be provided in JSON format with the following structure:

```json
{
  "test_suite": {
    "name": "String",
    "version": "String",
    "timestamp": "ISO8601 String"
  },
  "summary": {
    "status": "String",
    "total_tests": Integer,
    "passed_tests": Integer,
    "failed_tests": Integer,
    "skipped_tests": Integer,
    "duration_seconds": Float
  },
  "environment": {
    "test_dir": "String",
    "platform": "String",
    "dependencies": {}
  },
  "test_cases": [
    {
      "id": "String",
      "name": "String",
      "status": "String",
      "duration_seconds": Float,
      "setup": ["String"],
      "actions": ["String"],
      "assertions": ["String"],
      "results": ["String"],
      "cleanup": ["String"],
      "error": {
        "message": "String",
        "trace": "String"
      }
    }
  ],
  "coverage": {
    "statement_coverage": Float,
    "branch_coverage": Float,
    "function_coverage": Float,
    "line_coverage": Float
  },
  "artifacts": {
    "log_file": "String",
    "database_files": ["String"],
    "screenshots": ["String"]
  }
}
```

### 3.3 Report Storage

- Test reports must be saved in a standardized location outside of temporary test directories:
  ```
  ProjectRoot/
  ├── TestReports/
  │   ├── test_report_YYYYMMDD_HHMMSS.txt  (human-readable)
  │   └── test_report_YYYYMMDD_HHMMSS.json (machine-readable)
  ```
- Reports must use timestamped filenames
- Historical reports must be preserved
- Reports must be version controlled
- Reports must NOT be saved within temporary test directories that are cleaned up during tearDown()
- Test implementations must ensure report paths are absolute or resolve to locations outside test environments

## 4. Database Testing Standards

### 4.1 Database Testing Requirements

All database-related components must have automated tests that:

1. Create temporary database files in isolated test directories
2. Initialize database schema(s) with proper tables
3. Insert test data
4. Execute operations against the test database
5. Verify database state changes
6. Document database structure through test output
7. Clean up database files after test completion

### 4.2 Database Test Output

Database test reports must include:

1. **Database Creation Information**
   - Database file paths
   - Database version
   - Connection parameters
   - File sizes

2. **Schema Information**
   - List of all tables
   - For each table:
     - Column names and types
     - Primary and foreign keys
     - Constraints
     - Indexes

3. **Data Samples**
   - Row counts for each table
   - Sample data (up to 5 rows) for each table
   - Data statistics when relevant

4. **Operation Results**
   - Operations performed
   - Affected rows
   - Query performance metrics
   - Transaction details

Example database test output format:

```
Database: /tmp/test_dir/project.db
Size: 24.5 KB
Engine: SQLite 3.36.0

Table: users (3 columns, 5 rows)
  Schema:
    - user_id INTEGER PRIMARY KEY
    - username TEXT NOT NULL
    - created_at TEXT
  
  Data Sample (3 of 5 rows):
    1: (1, 'admin', '2025-03-24T10:15:30')
    2: (2, 'test_user', '2025-03-24T10:15:31')
    3: (3, 'demo_user', '2025-03-24T10:15:32')

Table: settings (4 columns, 2 rows)
  Schema:
    - setting_id INTEGER PRIMARY KEY
    - key TEXT NOT NULL
    - value TEXT
    - user_id INTEGER REFERENCES users(user_id)
  
  Data Sample (2 of 2 rows):
    1: (1, 'theme', 'dark', 1)
    2: (2, 'language', 'en', 1)
```

## 5. Test Implementation Guidelines

### 5.1 Using pytest Framework

pytest is the recommended testing framework for Project Himalaya and conforming projects. The following guidelines ensure optimal usage:

#### 5.1.1 Basic Test Structure

```python
# File: test_component_name.py
# Path: Tests/unit/test_component_name.py
# Standard: AIDEV-PascalCase-1.6
# Created: [Date]
# Last Modified: [Date]  [Time]
# Description: [Test description]

"""
Test module for [ComponentName].

This module contains pytest tests for verifying the functionality
of the [ComponentName] component.
"""

import pytest
# Other imports

# Use fixtures for test environment setup
@pytest.fixture
def test_environment():
    """Create test environment."""
    # Setup code
    yield  # This is where the test runs
    # Cleanup code

def test_functionality(test_environment):
    """Test specific functionality."""
    # Test implementation
    assert result == expected_result
```

#### 5.1.2 Using pytest Fixtures

Use pytest's built-in fixtures for common test resources:

```python
def test_database_operations(tmp_path):
    """Test database operations using pytest's tmp_path fixture."""
    # tmp_path is a pathlib.Path to a temporary directory
    db_path = tmp_path / "test.db"
    
    # Initialize database
    result = DatabaseIntegration.InitializeDatabase(db_path)
    assert result is True
    
    # The temporary directory is automatically cleaned up by pytest
```

#### 5.1.3 Custom Configuration

Create a `conftest.py` file to define project-wide pytest configuration:

```python
# File: conftest.py
# Path: Tests/conftest.py

def pytest_configure(config):
    """Configure pytest for Project Himalaya standards."""
    # Set report format and location
    config.option.htmlpath = "TestReports/report.html"
    
    # Register custom markers
    config.addinivalue_line("markers", 
                            "database: marks tests that require database setup")

@pytest.fixture(scope="session")
def himalaya_db():
    """Create a Himalaya test database for the test session."""
    # Setup code
    db_path = Path(tempfile.mkdtemp()) / "Himalaya.db"
    # Initialize database
    yield db_path
    # Cleanup code
```

### 5.2 Report Generation with pytest

Rather than implementing custom report capture in each test file, use pytest's built-in report generation capabilities:

#### 5.2.1 Using pytest-html Plugin

Install and configure the pytest-html plugin:

```bash
pip install pytest-html
```

Run tests with HTML report generation:

```bash
pytest --html=TestReports/report.html
```

#### 5.2.2 Creating Custom Text Reports

Use pytest hooks in conftest.py to generate custom reports:

```python
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Generate custom reports after all tests complete."""
    # Create timestamped report filename
    from datetime import datetime
    from pathlib import Path
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = Path("TestReports")
    report_dir.mkdir(exist_ok=True)
    report_path = report_dir / f"test_report_{timestamp}.txt"
    
    # Write report using test results
    with open(report_path, "w") as f:
        # Write summary header
        f.write("=" * 60 + "\n")
        f.write("TEST EXECUTION SUMMARY\n")
        f.write("-" * 60 + "\n")
        f.write(f"Timestamp: {datetime.now().isoformat()}\n")
        f.write(f"Status: {'PASSED' if exitstatus == 0 else 'FAILED'}\n")
        
        # Write test counts
        stats = terminalreporter.stats
        f.write(f"Tests: {sum(len(x) for x in stats.values())} total, "
                f"{len(stats.get('passed', []))} passed, "
                f"{len(stats.get('failed', []))} failed, "
                f"{len(stats.get('skipped', []))} skipped\n\n")
        
        # Write detail for each test
        for when in ('setup', 'call', 'teardown'):
            for report in terminalreporter.getreports(when):
                if report.nodeid:
                    f.write(f"{'=' * 60}\n")
                    f.write(f"TEST: {report.nodeid}\n")
                    f.write(f"{'-' * 60}\n")
                    f.write(f"Status: {report.outcome.upper()}\n")
                    if hasattr(report, 'longrepr'):
                        f.write(f"Details:\n{report.longrepr}\n\n")
        
    print(f"\nTest report saved to: {report_path}")
```

#### 5.2.3. Database Test Reports

For database-specific test details, use a custom fixture that captures database information:

```python
@pytest.fixture
def db_reporter():
    """Fixture to capture and report database information."""
    reports = []
    
    def _report_db(db_path, description=""):
        """Capture database information."""
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Build report
        report = {
            "path": str(db_path),
            "description": description,
            "tables": {},
        }
        
        # Get schema and sample data for each table
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            
            cursor.execute(f"SELECT * FROM {table} LIMIT 3")
            rows = cursor.fetchall()
            
            report["tables"][table] = {
                "columns": columns,
                "rows": rows,
                "row_count": len(rows)
            }
        
        reports.append(report)
        conn.close()
    
    yield _report_db
    
    # After test completes, write all reports to a file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = Path("TestReports") / f"db_report_{timestamp}.txt"
    
    with open(report_path, "w") as f:
        for report in reports:
            f.write(f"Database: {report['path']}\n")
            f.write(f"Description: {report['description']}\n")
            f.write(f"{'-' * 60}\n")
            
            for table, data in report["tables"].items():
                f.write(f"Table: {table}\n")
                f.write(f"Columns: {len(data['columns'])}\n")
                f.write(f"Rows: {data['row_count']}\n")
                f.write("Schema:\n")
                
                for col in data["columns"]:
                    f.write(f"  - {col[1]} ({col[2]})\n")
                
                f.write("Sample data:\n")
                for row in data["rows"]:
                    f.write(f"  {row}\n")
                
                f.write("\n")
    
    print(f"Database report saved to: {report_path}")
```

Usage in tests:

```python
def test_database_init(tmp_path, db_reporter):
    """Test database initialization with reporting."""
    db_path = tmp_path / "test.db"
    
    # Initialize database
    result = DatabaseIntegration.InitializeDatabase(db_path)
    assert result is True
    
    # Report database state
    db_reporter(db_path, "After initialization")
```
    
    # Custom TestRunner for output capture
    class TestRunner:
        def __init__(self, ReportPath):
            self.ReportPath = ReportPath
            self.OutputStream = StringIO()
            self.OriginalStdout = sys.stdout
            
        def __enter__(self):
            # Redirect stdout to capture output
            sys.stdout = self.__class__.TeeOutput(
                self.OriginalStdout, 
                self.OutputStream
            )
            return self
            
        def __exit__(self, exc_type, exc_val, exc_tb):
            # Restore original stdout
            sys.stdout = self.OriginalStdout
            
            # Write captured output to file
            with open(self.ReportPath, 'w') as f:
                f.write(self.OutputStream.getvalue())
                
            print(f"\nTest report saved to: {self.ReportPath}")
            
        class TeeOutput:
            """Class to duplicate output to console and file."""
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
```

## 6. Implementation Roadmap

### 6.1 Phase 1: Basic Test Automation
- Implement test structure template
- Create automated test output capture
- Generate basic test reports

### 6.2 Phase 2: Enhanced Reporting
- Add detailed schema reporting
- Implement performance metrics
- Create JSON report format

### 6.3 Phase 3: Continuous Integration
- Integrate with CI/CD pipeline
- Implement automatic test execution
- Build test result dashboard

## 7. References

- [20-30] STANDARD-FoundationDesignPrinciples
- [60-10] PLAN-TestStrategy
- [60-50] TEMPLATE-TestCase
- [50-10] IMPL-DocumentManager

---

*"Code is not merely functional—it is a visual medium that developers interact with for extended periods. The choices made in these standards prioritize the axis of symmetry, character distinction, readability at scale, and visual hierarchy."*

— Herbert J. Bowers
