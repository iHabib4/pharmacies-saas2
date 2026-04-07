#!/bin/bash
# dev.sh — Development workflow for pharmacies_saas2

set -e  # Exit immediately if any command fails

# -----------------------------
# 1. Activate Poetry environment
# -----------------------------
echo "Activating Poetry environment..."
# Using poetry run for commands in the virtual environment

# -----------------------------
# 2. Locate manage.py
# -----------------------------
# Try to find manage.py in current or subfolder
if [ -f "./manage.py" ]; then
    BASE_DIR="."
elif [ -f "./backend/manage.py" ]; then
    BASE_DIR="./backend"
else
    echo "Error: manage.py not found in current folder or ./backend"
    exit 1
fi

cd "$BASE_DIR"
echo "Using $(pwd) as base folder for Django."

# -----------------------------
# 3. Format code with Black
# -----------------------------
echo "Formatting code with Black..."
poetry run black .

# -----------------------------
# 4. Sort imports with isort
# -----------------------------
echo "Sorting imports with isort..."
poetry run isort .

# -----------------------------
# 5. Lint code with flake8 (ignoring venv)
# -----------------------------
echo "Running flake8 lint..."
# Uses the .flake8 file in the project root, excludes venv automatically
poetry run flake8 --config ../.flake8 .

# -----------------------------
# 6. Run tests with pytest
# -----------------------------
echo "Running pytest..."
poetry run pytest

# -----------------------------
# 7. Start Django development server
# -----------------------------
echo "Starting Django development server..."
poetry run python manage.py runserver 0.0.0.0:8000

# -----------------------------
# Done
# -----------------------------
echo "Development environment setup complete!"
