#!/bin/bash

# Exit on error
set -e

echo "Setting up Project Tasker development environment..."

# Function to check Python version
check_python_version() {
    if command -v python3 >/dev/null 2>&1; then
        python_version=$(python3 -c "import sys; print(f{sys.version_info.major}.{sys.version_info.minor})")
        if [ "$(echo "$python_version >= 3.10" | bc)" -eq 1 ]; then
            echo "Python version $python_version detected"
            return 0
        fi
    fi
    echo "Error: Python 3.10 or higher is required"
    return 1
}

# Function to create and activate virtual environment
setup_venv() {
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    echo "Activating virtual environment..."
    source venv/bin/activate
}

# Function to install and configure poetry
setup_poetry() {
    if ! command -v poetry >/dev/null 2>&1; then
        echo "Installing poetry..."
        curl -sSL https://install.python-poetry.org | python3 -
    else
        echo "Poetry already installed"
    fi

    echo "Configuring poetry..."
    poetry config virtualenvs.in-project true
}

# Function to install project dependencies
install_dependencies() {
    echo "Installing project dependencies..."
    poetry install
    
    echo "Installing spaCy language model..."
    python3 -m spacy download en_core_web_sm
}

# Function to setup git hooks
setup_git_hooks() {
    if [ -f ".git/hooks" ]; then
        echo "Setting up git hooks..."
        poetry run pre-commit install
    fi
}

# Function to setup environment configuration
setup_env() {
    if [ ! -f ".env" ]; then
        echo "Creating .env file from template..."
        if [ -f ".env.example" ]; then
            cp .env.example .env
            echo "Please update .env with your configuration values"
        else
            echo "Error: .env.example not found"
            return 1
        fi
    else
        echo ".env file already exists"
    fi
}

# Function to run database migrations
run_migrations() {
    echo "Running database migrations..."
    poetry run alembic upgrade head
}

# Main setup process
main() {
    echo "Starting setup process..."
    
    # Check requirements
    check_python_version || exit 1
    
    # Setup virtual environment
    setup_venv
    
    # Setup poetry
    setup_poetry
    
    # Install dependencies
    install_dependencies
    
    # Setup git hooks
    setup_git_hooks
    
    # Setup environment configuration
    setup_env
    
    # Run migrations
    run_migrations
    
    echo "Setup complete!"
    echo
    echo "To start the development server, run:"
    echo "poetry run uvicorn project_tasker.main:app --reload"
    echo
    echo "To run tests:"
    echo "poetry run pytest"
}

# Run main setup
main
