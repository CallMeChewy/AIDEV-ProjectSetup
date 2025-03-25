#!/bin/bash

# Script to test the fixed components

echo "Setting up templates..."
# Run template setup script
./setup_templates.sh

echo "Running tests..."
# Run test script
python run-tests-script.py

echo "Test run complete!"
