
#!/bin/bash

# Purpose: Set up the development environment for the AI Software Factory application
# Description: This script creates a virtual environment, installs dependencies,
#              and sets up the initial database for the application.

# Exit immediately if a command exits with a non-zero status
set -e

# Define colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Setting up development environment for AI Software Factory...${NC}"

# Create virtual environment
echo -e "${GREEN}Creating virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo -e "${GREEN}Upgrading pip...${NC}"
pip install --upgrade pip

# Install dependencies
echo -e "${GREEN}Installing dependencies...${NC}"
pip install -r requirements.txt

# Set up environment variables
echo -e "${GREEN}Setting up environment variables...${NC}"
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Please update the .env file with your specific configuration."
fi

# Initialize the database
echo -e "${GREEN}Initializing the database...${NC}"
flask db init
flask db migrate
flask db upgrade

# Run database initialization script
echo -e "${GREEN}Running database initialization script...${NC}"
python scripts/db_init.py

echo -e "${YELLOW}Development environment setup complete!${NC}"
echo -e "To activate the virtual environment, run: ${GREEN}source venv/bin/activate${NC}"
echo -e "To start the application, run: ${GREEN}flask run${NC}"
