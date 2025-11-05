#!/bin/bash
# Quick start script for Flipzy

# Check if poetry is installed
if ! command -v poetry &> /dev/null
then
    echo "Poetry is not installed. Please install it first:"
    echo "curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

# Install dependencies if needed
if [ ! -d ".venv" ] && [ ! -f "poetry.lock" ]; then
    echo "Installing dependencies..."
    poetry install
fi

# Run the app
echo "Starting Flipzy..."
poetry run streamlit run app.py

