#!/bin/bash

# Script to run the fixed tests

# First ensure the setup_templates.sh is executable
chmod +x setup_templates.sh

# Run the setup templates script
echo "Setting up templates..."
./setup_templates.sh

# Run the tests
echo "Running tests..."
python run-tests-script.py

echo "Test run complete!"
