# File: conftest.py
# Path: Tests/conftest.py
# Standard: AIDEV-PascalCase-1.6
# Created: March 24, 2025
# Last Modified: March 24, 2025  4:20PM
# Description: pytest configuration for Project Himalaya tests

"""
pytest configuration for Project Himalaya tests.

This module contains fixtures and hooks for pytest that apply to all
test modules in the Project Himalaya framework.
"""

import os
import sys
import pytest
from pathlib import Path
from datetime import datetime


def pytest_configure(config):
    """Configure pytest settings for Project Himalaya."""
    # Register custom markers
    config.addinivalue_line(
        "markers", 
        "database: marks tests that interact with databases"
    )
    config.addinivalue_line(
        "markers", 
        "integration: marks tests that require multiple components"
    )
    
    # Set default HTML report path if --html not specified
    if not config.getoption("--html", None):
        ReportDir = Path("TestReports")
        ReportDir.mkdir(exist_ok=True)
        Timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        HtmlReportPath = ReportDir / f"html_report_{Timestamp}.html"
        config.option.htmlpath = str(HtmlReportPath)


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Generate custom text report after tests complete."""
    # Create timestamped report filename
    Timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ReportDir = Path("TestReports")
    ReportDir.mkdir(exist_ok=True)
    TextReportPath = ReportDir / f"test_report_{Timestamp}.txt"
    
    # Write report using test results
    with open(TextReportPath, "w") as File:
        # Write header
        File.write("=" * 80 + "\n")
        File.write("PROJECT HIMALAYA TEST REPORT\n")
        File.write("=" * 80 + "\n")
        File.write(f"Generated: {datetime.now().isoformat()}\n")
        File.write(f"Test Status: {'PASSED' if exitstatus == 0 else 'FAILED'}\n\n")
        
        # Write test summary
        Stats = terminalreporter.stats
        File.write("Test Summary:\n")
        File.write("-" * 40 + "\n")
        File.write(f"Total tests: {sum(len(x) for x in Stats.values())}\n")
        File.write(f"Passed tests: {len(Stats.get('passed', []))}\n")
        File.write(f"Failed tests: {len(Stats.get('failed', []))}\n")
        File.write(f"Skipped tests: {len(Stats.get('skipped', []))}\n")
        
        # Calculate session duration - end time minus start time
        import time
        SessionDuration = time.time() - terminalreporter._sessionstarttime
        File.write(f"Execution time: {SessionDuration:.2f} seconds\n\n")
        
        # Write test details
        File.write("Test Details:\n")
        File.write("-" * 40 + "\n")
        
        # Process passed tests
        if Stats.get('passed'):
            File.write("\nPASSED TESTS:\n")
            for Report in Stats['passed']:
                if hasattr(Report, 'nodeid'):
                    File.write(f"✓ {Report.nodeid}\n")
        
        # Process failed tests
        if Stats.get('failed'):
            File.write("\nFAILED TESTS:\n")
            for Report in Stats['failed']:
                if hasattr(Report, 'nodeid'):
                    File.write(f"✗ {Report.nodeid}\n")
                    if hasattr(Report, 'longrepr'):
                        File.write(f"  Error: {str(Report.longrepr).split('E       ')[1].split('\\n')[0]}\n")
        
        # Process skipped tests
        if Stats.get('skipped'):
            File.write("\nSKIPPED TESTS:\n")
            for Report in Stats['skipped']:
                if hasattr(Report, 'nodeid'):
                    File.write(f"- {Report.nodeid}\n")
    
    print(f"\nTest report saved to: {TextReportPath}")


@pytest.fixture(scope="function")
def test_timestamp():
    """Generate a timestamp for test identification."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


@pytest.fixture(scope="session")
def project_root():
    """Get project root directory for consistent path resolution."""
    # First try environment variable
    ProjectRoot = os.environ.get("PROJECT_ROOT")
    
    if ProjectRoot:
        return Path(ProjectRoot)
    
    # Otherwise resolve from this file location
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def report_dir(project_root):
    """Get report directory path and ensure it exists."""
    ReportDir = project_root / "TestReports"
    ReportDir.mkdir(exist_ok=True)
    return ReportDir
