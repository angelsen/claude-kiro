# Steering Files (CLAUDE.md) in Claude Code

## Overview

Steering files are markdown files that provide Claude Code with persistent instructions, context, and preferences across sessions. They use the filename `CLAUDE.md` and are automatically loaded when Claude Code starts.

**Key Concept:** Think of CLAUDE.md files as "memory" - instructions that Claude remembers every time it starts in a project or workspace.

## CLAUDE.md File Locations

Claude Code supports a hierarchical memory system with four levels:

### 1. Enterprise Policy (Organization-Wide)

**Purpose:** Company-wide standards managed by IT/DevOps

**Locations:**
- macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`
- Linux/WSL: `/etc/claude-code/CLAUDE.md`
- Windows: `C:\ProgramData\ClaudeCode\CLAUDE.md`

**Use Cases:**
- Company coding standards
- Security policies
- Compliance requirements
- Mandatory workflows

**Shared With:** All users in organization

### 2. User Memory (Personal Global)

**Location:** `~/.claude/CLAUDE.md`

**Purpose:** Personal preferences that apply to all projects

**Use Cases:**
- Code styling preferences
- Personal tooling shortcuts
- Favorite commands
- Global workflow preferences

**Shared With:** Just you (across all projects)

### 3. Project Memory (Team-Shared)

**Locations:**
- `./CLAUDE.md` (project root)
- `./.claude/CLAUDE.md` (recommended for organization)

**Purpose:** Team-shared instructions for the specific project

**Use Cases:**
- Project architecture
- Coding standards for this project
- Common workflows
- Team conventions
- Build/test/deploy commands

**Shared With:** Team members via source control

### 4. Project Memory Local (Personal, Deprecated)

**Location:** `./CLAUDE.local.md`

**Status:** Deprecated - use imports instead (see below)

**Previous Use:** Personal project-specific preferences not checked into git

## Memory Hierarchy and Precedence

**Loading Order (highest to lowest precedence):**
1. Enterprise policy
2. Project memory (with recursive discovery)
3. User memory
4. Project memory (local)

**Important Behaviors:**
- Files are loaded in order, with earlier ones taking precedence
- Claude recurses from current directory up to root looking for CLAUDE.md files
- Nested CLAUDE.md files in subdirectories are only loaded when Claude reads files in those subtrees
- All memory files are combined to form Claude's context

## CLAUDE.md Import System

### Import Syntax

Use `@path/to/file` to import other files into CLAUDE.md:

```markdown
See @README.md for project overview.
See @package.json for available npm commands.

# Git Workflow
Follow the instructions in @docs/git-workflow.md

# Testing Guidelines
@docs/testing.md
```

### Import Rules

**Supported Paths:**
- Relative paths: `@docs/guidelines.md`
- Absolute paths: `@/home/user/shared/standards.md`
- Home directory: `@~/.claude/my-project-instructions.md`

**Important Behaviors:**
- Both relative and absolute paths allowed
- Imports NOT evaluated inside code spans: `` `@package` ``
- Imports NOT evaluated inside code blocks
- Recursive imports supported (max depth: 5 hops)
- Use `/memory` command to see what files are loaded

### Import for Individual Preferences

Replace deprecated CLAUDE.local.md with imports:

**In CLAUDE.md (checked into git):**
```markdown
# Project Standards
Follow our coding guidelines in @docs/standards.md

# Individual Preferences
@~/.claude/myproject-preferences.md
```

**In ~/.claude/myproject-preferences.md (not in git):**
```markdown
# My Personal Preferences for This Project

- Use my sandbox environment at https://myproject-dev.example.com
- When testing, use my test account: test-user-123
- Prefer detailed explanations in code reviews
```

**Benefits:**
- Works across multiple git worktrees
- Personal settings not in version control
- Team members can have their own preference files
- More flexible than CLAUDE.local.md

## CLAUDE.md Structure and Format

### Basic Format

```markdown
# Project: My Application

## Architecture
This is a React + Node.js application with:
- Frontend: React 18 with TypeScript
- Backend: Express.js API
- Database: PostgreSQL
- Authentication: JWT tokens

## Code Style
- Use 2-space indentation
- Prefer functional components
- Use TypeScript strict mode
- Write JSDoc comments for public APIs

## Common Commands
Build: `npm run build`
Test: `npm test`
Lint: `npm run lint`
Dev server: `npm run dev`

## Git Workflow
- Main branch: `main`
- Feature branches: `feature/TICKET-description`
- Always run tests before pushing
- Squash commits when merging

## Testing
- Write unit tests for all business logic
- Use React Testing Library for component tests
- Aim for >80% code coverage
```

### Best Practices for Structure

**1. Use Markdown Headings for Organization**
```markdown
# High-Level Context

## Architecture

## Coding Standards

## Common Commands

## Workflows

## Testing

## Deployment
```

**2. Use Bullet Points for Individual Memories**
```markdown
## Coding Standards
- Use 2-space indentation
- Prefer `const` over `let`
- Use TypeScript strict mode
- Write meaningful variable names
- Add JSDoc comments to public functions
```

**3. Be Specific, Not General**

**Good:**
```markdown
- Use 2-space indentation for JavaScript files
- Function names should use camelCase
- Component files should use PascalCase
```

**Bad:**
```markdown
- Format code properly
- Use good naming conventions
```

### Importing Common Files

```markdown
# Project Context

## Overview
See @README.md for full project documentation.

## Package Information
Available commands: @package.json

## API Documentation
@docs/api-spec.yaml

## Database Schema
@docs/database-schema.sql

## Environment Setup
@.env.example
```

## Setting Up Project CLAUDE.md

### Bootstrap with /init Command

```bash
# Start Claude in your project
claude

# Initialize CLAUDE.md
> /init
```

This creates a starter CLAUDE.md with project-specific context.

### Manual Creation

**Option 1: Project Root**
```bash
# Create in project root
touch CLAUDE.md
```

**Option 2: .claude Directory (Recommended)**
```bash
# Create organized directory
mkdir -p .claude
touch .claude/CLAUDE.md
```

### Add to Version Control

```bash
# Add project memory to git
git add CLAUDE.md  # or .claude/CLAUDE.md
git commit -m "Add Claude Code memory file"

# Ensure .claude/settings.local.json is ignored
# (Claude Code auto-configures this)
```

## Quick Memory Management

### Add Memories with # Shortcut

**In Claude Code session:**
```
# Always use descriptive variable names
```

Claude prompts you to select which memory file to store this in.

### Edit Memories with /memory Command

```
> /memory
```

Opens memory files in your system editor for direct editing.

### View Loaded Memories

```
> /memory
```

Shows all currently loaded memory files and their sources.

## Import Examples

### Example 1: Team Shared + Individual Preferences

**CLAUDE.md (in git):**
```markdown
# Project Memory

## Team Standards
@docs/coding-standards.md
@docs/git-workflow.md

## Individual Developer Preferences
@~/.claude/this-project-prefs.md
```

**~/.claude/this-project-prefs.md (not in git):**
```markdown
# My Preferences for This Project

- When running tests, use my local database
- Prefer verbose error messages
- Show performance metrics in dev mode
```

### Example 2: Multi-Environment Setup

**CLAUDE.md:**
```markdown
# Application Context

## Overview
@README.md

## Development
@docs/dev-setup.md
@.env.example

## API Contracts
@docs/api/
@openapi.yaml

## Database
@docs/schema.sql
@docs/migrations/
```

### Example 3: Monorepo Structure

**Root CLAUDE.md:**
```markdown
# Monorepo Overview

Overall architecture: @docs/architecture.md

## Shared Standards
@docs/coding-standards.md
@docs/git-workflow.md

## Individual Package Docs
- Frontend: @packages/frontend/README.md
- Backend: @packages/backend/README.md
- Shared: @packages/shared/README.md
```

**packages/frontend/CLAUDE.md:**
```markdown
# Frontend Package

## Specific Guidelines
- Use React hooks, no class components
- State management: Zustand
- Styling: Tailwind CSS

## Commands
@package.json
```

## Context Loading Mechanisms

### Automatic Loading

**When Claude Code Starts:**
1. Loads enterprise CLAUDE.md (if exists)
2. Recurses from cwd up to root, loading CLAUDE.md files
3. Loads user CLAUDE.md from home directory
4. Processes all imports recursively (max depth: 5)

**When Reading Files:**
- If Claude reads a file in a subdirectory
- Checks for CLAUDE.md in that subdirectory
- Loads it for additional context

### Manual Context Loading

**@ References in Prompts:**
```
> Explain the authentication logic in @src/auth/login.js
```

This:
1. Includes the file content
2. Loads CLAUDE.md files from `src/auth/` if they exist
3. Adds parent CLAUDE.md files for context

**Directory References:**
```
> What's the structure of @src/components?
```

Shows directory listing with file information.

**MCP Resources:**
```
> Show me @github:repos/owner/repo/issues
```

Fetches from MCP servers using `@server:resource` format.

## Best Practices for Steering Files

### 1. Start Specific, Then Generalize

**Good First Memory:**
```markdown
# Build Commands
Build production: `npm run build`
Run tests: `npm test`
Start dev server: `npm run dev`
Lint code: `npm run lint`
```

**Expand Over Time:**
```markdown
# Build Commands
Build production: `npm run build`
Build staging: `npm run build:staging`
Run all tests: `npm test`
Run unit tests only: `npm run test:unit`
Run integration tests: `npm run test:integration`
Start dev server: `npm run dev` (runs on port 3000)
Start dev with hot reload: `npm run dev:hot`
Lint code: `npm run lint`
Lint and fix: `npm run lint:fix`
```

### 2. Document What's Non-Obvious

**Include:**
- Unusual patterns or conventions
- Project-specific terminology
- Non-standard directory structures
- Special build requirements
- Team-specific workflows

**Example:**
```markdown
## Project-Specific Terms
- "Widget" = A reusable UI component in our library
- "Pipeline" = Our data processing workflow (not CI/CD)
- "Core" directory = Shared business logic (not framework code)

## Unusual Conventions
- We use `.spec.tsx` for component tests (not `.test.tsx`)
- API routes are in `/pages/api/v2/` (v1 is deprecated)
- Environment variables MUST use `NEXT_PUBLIC_` prefix for client-side
```

### 3. Keep It Updated

**Review Triggers:**
- Major refactoring
- New team members joining
- Technology stack changes
- Workflow changes

**Regular Review:**
```markdown
# Last Updated
Updated: 2025-09-15 - Added new testing guidelines
Updated: 2025-08-01 - Migrated to pnpm from npm
```

### 4. Use Hierarchical Organization

**Enterprise Level (Rarely Changes):**
```markdown
# Company Standards
- All code must pass security scan
- Use approved open source licenses only
- Follow WCAG 2.1 AA accessibility standards
```

**Project Level (Changes Occasionally):**
```markdown
# Project Architecture
- Microservices pattern
- Event-driven communication
- PostgreSQL for primary database
```

**User Level (Personal Preferences):**
```markdown
# My Preferences
- Prefer detailed explanations
- Always show type annotations
- Include usage examples in code
```

### 5. Avoid Code in CLAUDE.md

**Don't Do This:**
```markdown
## Login Function
function login(user, pass) {
  // ... 100 lines of code
}
```

**Do This Instead:**
```markdown
## Authentication
Login logic is in @src/auth/login.ts
Uses JWT tokens with 24-hour expiration
Refresh tokens stored in httpOnly cookies
```

## Integration with Settings Files

**CLAUDE.md vs. settings.json:**

**CLAUDE.md (Instructions/Context):**
- What to do
- How to do it
- Project context
- Team conventions

**settings.json (Configuration):**
- Permissions
- Environment variables
- Tool settings
- Technical configuration

**Example Separation:**

**CLAUDE.md:**
```markdown
# Testing
- Always run tests before committing
- Write tests for all business logic
- Use React Testing Library for components
```

**settings.json:**
```json
{
  "permissions": {
    "allow": [
      "Bash(npm test)",
      "Bash(npm run lint)"
    ]
  },
  "env": {
    "NODE_ENV": "test"
  }
}
```

## Advanced Patterns

### Pattern 1: Progressive Disclosure

**CLAUDE.md:**
```markdown
# Quick Start
Common commands: @docs/quick-start.md

# Detailed Documentation
- Architecture: @docs/architecture.md
- API Reference: @docs/api/
- Database: @docs/database/
```

### Pattern 2: Role-Based Context

**CLAUDE.md:**
```markdown
# General Context
@README.md

# For Backend Developers
@docs/backend/

# For Frontend Developers
@docs/frontend/

# For DevOps
@docs/infrastructure/
```

### Pattern 3: Multi-Worktree Support

**CLAUDE.md (shared):**
```markdown
# Shared Project Context
@README.md

# Personal Settings (per-developer)
@~/.claude/my-prefs.md
```

**Benefit:** Works across multiple git worktrees for parallel development.

## Common Use Cases

### 1. Onboarding New Team Members

**CLAUDE.md:**
```markdown
# New Developer Onboarding

## Setup
1. @docs/setup-guide.md
2. Run `npm install`
3. Copy `.env.example` to `.env.local`
4. Run `npm run db:migrate`

## Key Concepts
@docs/architecture-overview.md

## First Tasks
- Review @docs/coding-standards.md
- Read @docs/git-workflow.md
- Try fixing a "good first issue" ticket
```

### 2. Maintaining Coding Standards

**CLAUDE.md:**
```markdown
# Coding Standards

## TypeScript
- Always use strict mode
- Prefer interfaces over types
- Use explicit return types for functions
- No `any` types (use `unknown` if needed)

## React
- Functional components only
- Use hooks, no class components
- Props types in separate file: `*.types.ts`
- One component per file

## Testing
- Unit test coverage: minimum 80%
- Integration tests for all API endpoints
- E2E tests for critical user flows
```

### 3. Project-Specific Workflows

**CLAUDE.md:**
```markdown
# Workflows

## Feature Development
1. Create feature branch: `feature/TICKET-description`
2. Implement feature
3. Write tests (min 80% coverage)
4. Run `npm run lint && npm test`
5. Push and create PR
6. Wait for CI to pass
7. Request review from 2 team members
8. Squash and merge after approval

## Bug Fixes
1. Create branch: `fix/TICKET-description`
2. Add failing test first
3. Fix the bug
4. Verify test passes
5. Check for regression
6. Follow feature PR process

## Hotfixes
1. Create from main: `hotfix/description`
2. Fix critical issue
3. Fast-track review (1 approver)
4. Deploy to staging first
5. Deploy to production after smoke test
```

## Troubleshooting

### Memory Not Loading

**Check:**
1. File named exactly `CLAUDE.md` (case-sensitive)
2. File in correct location
3. Valid markdown format
4. No syntax errors in imports
5. Run `/memory` to see what's loaded

### Imports Not Working

**Verify:**
1. Path is correct (relative or absolute)
2. File exists at specified path
3. Not inside code block or code span
4. Max depth not exceeded (5 hops)
5. Check for circular imports

### Conflicting Instructions

**Resolution Order:**
1. Enterprise policy (highest precedence)
2. Project memory
3. User memory
4. Project memory local

**Fix:** Check which file contains conflicting instruction using `/memory`.

## Resources

- **Memory Documentation**: `/docs/claude-code/memory`
- **Settings Documentation**: `/docs/claude-code/settings`
- **Common Workflows**: `/docs/claude-code/common-workflows`
- **IAM and Permissions**: `/docs/claude-code/iam`
