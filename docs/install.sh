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

# Create project-specific .claude directory
echo -e "${YELLOW}Creating project configuration directories...${NC}"
mkdir -p .claude/{output-styles,commands/spec}

# Base URL for raw GitHub content
BASE_URL="https://raw.githubusercontent.com/angelsen/claude-kiro/master/.claude"

# Download output style
echo -e "${YELLOW}Installing Spec-Driven Developer output style...${NC}"
curl -sSL "$BASE_URL/output-styles/spec-driven.md" \
     -o .claude/output-styles/spec-driven.md

# Download slash commands
echo -e "${YELLOW}Installing slash commands...${NC}"
curl -sSL "$BASE_URL/commands/spec/create.md" \
     -o .claude/commands/spec/create.md
curl -sSL "$BASE_URL/commands/spec/implement.md" \
     -o .claude/commands/spec/implement.md
curl -sSL "$BASE_URL/commands/spec/review.md" \
     -o .claude/commands/spec/review.md

echo -e "${GREEN}Files installed in current project's .claude directory${NC}"

# Success message
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ Installation Complete!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Next steps:"
echo "1. Open this project in Claude Code"
echo "2. The spec-driven output style and slash commands are now available for this project"
echo "3. Try creating your first spec with: /spec:create [feature-description]"
echo ""
echo "Note: These settings are project-specific and won't affect other projects"
echo ""
echo "Documentation: https://github.com/angelsen/claude-kiro"
echo ""