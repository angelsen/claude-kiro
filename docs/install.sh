#!/bin/bash

# Claude Kiro Installation Script
# Installs spec-driven development configuration for Claude Code

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

# Check for Claude Code directory
if [ ! -d "$HOME/.claude" ]; then
    echo -e "${RED}Error: Claude Code directory not found at ~/.claude${NC}"
    echo "Please ensure Claude Code is installed and has been run at least once."
    exit 1
fi

# Create necessary directories
echo -e "${YELLOW}Creating configuration directories...${NC}"
mkdir -p ~/.claude/{output_styles,slash_commands,hooks,steering}

# Base URL for raw GitHub content
BASE_URL="https://raw.githubusercontent.com/angelsen/claude-kiro/main/.claude"

# Download output style
echo -e "${YELLOW}Installing Spec-Driven Developer output style...${NC}"
curl -sSL "$BASE_URL/output_styles/spec-driven-developer.md" \
     -o ~/.claude/output_styles/spec-driven-developer.md

# Download slash commands
echo -e "${YELLOW}Installing slash commands...${NC}"
curl -sSL "$BASE_URL/slash_commands/spec-create.md" \
     -o ~/.claude/slash_commands/spec-create.md
curl -sSL "$BASE_URL/slash_commands/spec-implement.md" \
     -o ~/.claude/slash_commands/spec-implement.md
curl -sSL "$BASE_URL/slash_commands/spec-review.md" \
     -o ~/.claude/slash_commands/spec-review.md

# Download hooks (Phase 2 - optional)
if [ -f "$BASE_URL/hooks/pre-commit-spec-update.sh" ]; then
    echo -e "${YELLOW}Installing hooks...${NC}"
    curl -sSL "$BASE_URL/hooks/pre-commit-spec-update.sh" \
         -o ~/.claude/hooks/pre-commit-spec-update.sh
    chmod +x ~/.claude/hooks/pre-commit-spec-update.sh
fi

# Download steering file
echo -e "${YELLOW}Installing project steering file...${NC}"
curl -sSL "$BASE_URL/steering/CLAUDE.md" \
     -o ~/.claude/steering/CLAUDE.md

# Success message
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ Installation Complete!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Next steps:"
echo "1. Restart Claude Code to load the new configuration"
echo "2. Select 'Spec-Driven Developer' as your output style in settings"
echo "3. Try creating your first spec with: /spec-create [feature-description]"
echo ""
echo "Documentation: https://github.com/angelsen/claude-kiro"
echo ""