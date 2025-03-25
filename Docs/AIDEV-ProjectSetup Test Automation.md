# AIDEV-ProjectSetup Test Automation

This directory contains automated tests for the AIDEV-ProjectSetup application. These tests are designed to verify the functionality of all core components and their integration.

## Test Structure

The test suite is organized as follows:

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test interactions between components
- **End-to-End Tests**: Test complete workflows

## Running the Tests

To run all tests and generate a report:

```bash
python run_tests.py
```

To run specific test modules:

```bash
# Run unit tests only
python -m unittest Tests/UnitTests/test_project_setup.py

# Run integration tests only
python -m unittest Tests/IntegrationTests/test_integration.py
```

## Test Coverage

These tests cover the following core functionality:

### Unit Tests

- **DirectoryParser**: Parsing and formatting directory structures
- **ConfigManager**: Configuration loading and management
- **DatabaseIntegration**: Database initialization and schema creation
- **GitHubManager**: Repository validation and management
- **ProjectInitializer**: Project creation and setup

### Integration Tests

- **End-to-End Project Creation**: Full project setup process
- **Database Integration Flow**: Complete database setup and registration

## Test Dependencies

The tests use the following Python packages:

- unittest (standard library)
- tempfile (standard library)
- sqlite3 (standard library)
- unittest.mock (standard library)

## Adding New Tests

When adding new tests, please follow these guidelines:

1. **Naming Convention**: Test files should be named `test_*.py`
2. **Class Structure**: Each test class should inherit from `unittest.TestCase`
3. **Test Naming**: Test methods should start with `test_` and have descriptive names
4. **Setup/Teardown**: Use `setUp` and `tearDown` methods for test environment setup
5. **Mocking**: Use patches and mocks to isolate tests from external dependencies
6. **Test Documentation**: Include docstrings describing the purpose of each test

## Test Reports

Test reports are generated in the `TestReports` directory with timestamped filenames. These reports include:

- Test count and execution time
- Pass/fail statistics
- Detailed failure information
- Overall success rate

## Continuous Integration

These tests are designed to be run in a CI/CD pipeline. To integrate with GitHub Actions:

1. Create a `.github/workflows/tests.yml` file in your repository
2. Configure it to run `python run_tests.py` on push and pull requests
3. Set up failure notifications and reporting

## Troubleshooting

If tests fail, check the following:

1. **Dependencies**: Ensure all required packages are installed
2. **Environment**: Verify the test environment matches the expected configuration
3. **Mocks**: Ensure mocks are correctly configured for the expected behaviors
4. **Database**: Check database connection and schema issues
5. **File Paths**: Verify path
