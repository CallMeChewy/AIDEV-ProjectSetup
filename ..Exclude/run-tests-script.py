# File: run_tests.py
# Path: AIDEV-ProjectSetup/run_tests.py
# Standard: AIDEV-PascalCase-1.6
# Created: 2025-03-23
# Last Modified: 2025-03-23  4:10PM
# Description: Script to run all tests for AIDEV-ProjectSetup

"""
Test runner for AIDEV-ProjectSetup.

This script runs all unit and integration tests for the AIDEV-ProjectSetup application
and generates a report of the results.
"""

import os
import sys
import time
import unittest
import datetime
from pathlib import Path

def RunTests():
    """Run all tests and return results."""
    # Start timing
    StartTime = time.time()
    
    # Get test directory
    TestDir = Path(__file__).parent / 'Tests'
    
    # Discover and run tests
    Loader = unittest.TestLoader()
    Suite = Loader.discover(str(TestDir), pattern='test_*.py')
    
    # Create test result
    Result = unittest.TextTestRunner(verbosity=2).run(Suite)
    
    # End timing
    EndTime = time.time()
    
    return {
        'total': Result.testsRun,
        'failures': len(Result.failures),
        'errors': len(Result.errors),
        'skipped': len(Result.skipped),
        'time': EndTime - StartTime,
        'success_rate': (Result.testsRun - len(Result.failures) - len(Result.errors)) / Result.testsRun * 100 if Result.testsRun > 0 else 0,
        'result': Result
    }

def GenerateReport(Results):
    """Generate a report from test results."""
    # Create report directory if it doesn't exist
    ReportDir = Path(__file__).parent / 'TestReports'
    ReportDir.mkdir(exist_ok=True)
    
    # Create report filename with timestamp
    Timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    ReportPath = ReportDir / f'test_report_{Timestamp}.txt'
    
    # Generate report content
    Content = [
        "AIDEV-ProjectSetup Test Report",
        f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "-" * 50,
        f"Total Tests: {Results['total']}",
        f"Passed: {Results['total'] - Results['failures'] - Results['errors']}",
        f"Failed: {Results['failures']}",
        f"Errors: {Results['errors']}",
        f"Skipped: {Results['skipped']}",
        f"Success Rate: {Results['success_rate']:.2f}%",
        f"Total Time: {Results['time']:.2f} seconds",
        "-" * 50,
    ]
    
    # Add failure details
    if Results['failures']:
        Content.append("\nTest Failures:")
        for i, (Test, Trace) in enumerate(Results['result'].failures, 1):
            Content.append(f"\n{i}. {Test}")
            Content.append(f"   {Trace.split('Traceback')[0].strip()}")
    
    # Add error details
    if Results['errors']:
        Content.append("\nTest Errors:")
        for i, (Test, Trace) in enumerate(Results['result'].errors, 1):
            Content.append(f"\n{i}. {Test}")
            Content.append(f"   {Trace.split('Traceback')[0].strip()}")
    
    # Add summary
    if Results['failures'] == 0 and Results['errors'] == 0:
        Content.append("\nALL TESTS PASSED!")
    else:
        Content.append("\nSOME TESTS FAILED. See details above.")
    
    # Write report to file
    with open(ReportPath, 'w') as File:
        File.write('\n'.join(Content))
    
    print(f"Test report generated: {ReportPath}")
    return ReportPath

def Main():
    """Main entry point for the test runner."""
    print("Running AIDEV-ProjectSetup tests...")
    
    # Run tests
    Results = RunTests()
    
    # Display summary
    print("\nTest Summary:")
    print(f"Total Tests: {Results['total']}")
    print(f"Passed: {Results['total'] - Results['failures'] - Results['errors']}")
    print(f"Failed: {Results['failures']}")
    print(f"Errors: {Results['errors']}")
    print(f"Success Rate: {Results['success_rate']:.2f}%")
    print(f"Total Time: {Results['time']:.2f} seconds")
    
    # Generate report
    ReportPath = GenerateReport(Results)
    
    # Return exit code
    return 0 if Results['failures'] == 0 and Results['errors'] == 0 else 1

if __name__ == '__main__':
    sys.exit(Main())
