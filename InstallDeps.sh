#!/bin/bash

VENV_NAME=venv
REQUIREMENTS_FILE=requirements.txt

# Install necessary packages for creating virtual environments
if ! command -v python3 &>/dev/null; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

if ! command -v pip &>/dev/null; then
    echo "Pip is not installed. Installing pip..."
    sudo apt update
    sudo apt install -y python3-pip
fi

# Install python3-venv package if not installed
if ! dpkg -s python3-venv &>/dev/null; then
    echo "python3-venv package is not installed. Installing python3-venv..."
    sudo apt update
    sudo apt install -y python3-venv
fi

# Check for .gitignore and update or create as necessary
if [ -f .gitignore ]; then
    if ! grep -q "$VENV_NAME/" .gitignore; then
        echo "$VENV_NAME/" >> .gitignore
        echo "Added $VENV_NAME to .gitignore."
    else
        echo "$VENV_NAME is already in .gitignore."
    fi
else
    echo "$VENV_NAME/" > .gitignore
    echo "Created .gitignore and added $VENV_NAME."
fi

# Check for virtual environment, create if not exists
if [ ! -d "$VENV_NAME" ]; then
    python3 -m venv "$VENV_NAME"
    echo "Virtual environment created."
fi

# Activate virtual environment and install requirements
source "$VENV_NAME/bin/activate" && pip install -r "$REQUIREMENTS_FILE"

echo
echo "To activate the virtual env use: \"source venv/bin/activate\""
echo "To deactivate the virtual env use: \"deactivate\""
