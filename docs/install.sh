#!/bin/bash

# Claude Kiro Quick Setup Script
# Sets up spec-driven development for Claude Code

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}     Claude Kiro - Spec-Driven Development for Claude Code      ${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check if ck is installed
echo -e "${YELLOW}Checking for Claude Kiro CLI...${NC}"
if ! command -v ck &> /dev/null; then
    echo -e "${RED}⚠ Claude Kiro CLI (ck) is not installed.${NC}"
    echo ""
    echo "Would you like to install it now?"
    echo ""
    read -p "Install Claude Kiro? [Y/n]: " -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
        echo -e "${YELLOW}Installing Claude Kiro...${NC}"
        if command -v uv &> /dev/null; then
            uv tool install claude-kiro
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}✓ Claude Kiro installed successfully!${NC}"
            else
                echo -e "${RED}Failed to install. Try manually:${NC}"
                echo "  uv tool install claude-kiro"
                exit 1
            fi
        else
            echo -e "${RED}uv is not installed. Please install uv first:${NC}"
            echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
            echo ""
            echo "Then run: uv tool install claude-kiro"
            exit 1
        fi
    else
        echo -e "${RED}Claude Kiro is required. Install it with:${NC}"
        echo "  uv tool install claude-kiro"
        exit 1
    fi
    echo ""
else
    echo -e "${GREEN}✓ Claude Kiro CLI is installed${NC}"
fi

# Initialize the project
echo -e "${YELLOW}Initializing project for spec-driven development...${NC}"
ck init

# Run doctor to verify
echo ""
echo -e "${YELLOW}Verifying setup...${NC}"
ck doctor

# Success message
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Next steps:"
echo "1. Open this project in Claude Code"
echo "2. Try creating your first spec: /spec:create [feature-description]"
echo "3. Use 'ck doctor' anytime to check your setup"
echo ""
echo "Documentation: https://angelsen.github.io/claude-kiro/"
echo ""