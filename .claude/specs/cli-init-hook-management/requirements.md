# Feature: CLI with Init and Hook Management

## Overview
Provide a unified command-line interface (`ck`) for initializing Claude Kiro projects and managing hooks. This replaces the need for multiple `ckh-*` scripts with a single entry point (`ck --hook <name>`) that Claude Code calls, and provides user-facing commands for setup and management. The CLI bundles all configuration files (output styles, slash commands, templates) within the package for offline, versioned deployment.

## User Stories

### Story 1: Simple Project Initialization
**As a** new Claude Kiro user
**I want** to initialize my project with a single command
**So that** I can start using spec-driven development immediately without manual file copying

**Acceptance Criteria (EARS notation):**
- WHEN a user runs `ck init` in a project directory, THE SYSTEM SHALL create `.claude/output-styles/spec-driven.md`
- WHEN a user runs `ck init` in a project directory, THE SYSTEM SHALL create `.claude/commands/spec/{create,implement,review}.md`
- WHEN a user runs `ck init` in a project directory, THE SYSTEM SHALL create `.claude/CLAUDE.md` template
- WHEN a user runs `ck init` in a project directory, THE SYSTEM SHALL configure hooks in `.claude/settings.local.json`
- WHEN a user runs `ck init` and files already exist, THE SYSTEM SHALL skip existing files and report what was skipped
- WHEN a user runs `ck init --force`, THE SYSTEM SHALL overwrite existing files
- WHEN `ck init` completes successfully, THE SYSTEM SHALL display next steps and usage instructions

### Story 2: Unified Hook Execution
**As a** Claude Code user
**I want** hooks to be called via a single command
**So that** I don't have multiple `ckh-*` commands polluting my global namespace

**Acceptance Criteria (EARS notation):**
- WHEN Claude Code calls `ck --hook post-file-ops` with JSON on stdin, THE SYSTEM SHALL execute the post-file-ops hook module
- WHEN a hook reads JSON from stdin, THE SYSTEM SHALL pass it to the appropriate hook module
- WHEN a hook completes successfully, THE SYSTEM SHALL output JSON to stdout for Claude Code
- WHEN a hook name is invalid, THE SYSTEM SHALL exit with code 1 and display an error message
- WHEN hook execution fails, THE SYSTEM SHALL exit with appropriate error code and log to stderr

### Story 3: Hook Management and Testing
**As a** developer
**I want** to list, test, and manage hooks easily
**So that** I can understand what hooks are available and verify they work correctly

**Acceptance Criteria (EARS notation):**
- WHEN a user runs `ck hook list`, THE SYSTEM SHALL display all available hook modules
- WHEN a user runs `ck hook status`, THE SYSTEM SHALL show which hooks are configured in settings.local.json
- WHEN a user runs `ck hook test <name>` with sample JSON file, THE SYSTEM SHALL execute the hook and display output
- WHEN a user runs `ck hook config`, THE SYSTEM SHALL generate a settings.json snippet for copy/paste
- WHEN a hook test fails, THE SYSTEM SHALL display the error and suggest fixes

### Story 4: Setup Health Checking
**As a** user
**I want** to verify my Claude Kiro setup is correct
**So that** I can troubleshoot configuration issues quickly

**Acceptance Criteria (EARS notation):**
- WHEN a user runs `ck doctor`, THE SYSTEM SHALL check if `ck` command is installed
- WHEN a user runs `ck doctor`, THE SYSTEM SHALL verify `.claude` directory structure exists
- WHEN a user runs `ck doctor`, THE SYSTEM SHALL validate required files are present
- WHEN a user runs `ck doctor`, THE SYSTEM SHALL check hooks are configured in settings.json
- WHEN a user runs `ck doctor`, THE SYSTEM SHALL report the count of existing specs
- WHEN all checks pass, THE SYSTEM SHALL display "✓ Everything looks good!"
- WHEN any check fails, THE SYSTEM SHALL display specific actionable error messages

## Non-Functional Requirements

- **Performance:** `ck init` must complete in < 2 seconds on typical hardware
- **Dependencies:** CLI must use only Python standard library plus Click (already a dependency)
- **Compatibility:** Must work on Python 3.11+ on Windows, macOS, and Linux
- **Installation:** Single command via `uv tool install claude-kiro` installs all functionality
- **User Experience:** Error messages must be clear, actionable, and friendly
- **Offline Operation:** All bundled resources available without network access
- **Idempotency:** `ck init` must be safe to run multiple times without data loss

## Constraints

- **Technical constraints:**
  - Must maintain backward compatibility with existing hook modules
  - Resources (.md files) must be bundled in the package using `importlib.resources`
  - Hook execution must use stdin/stdout JSON protocol (Claude Code requirement)
  - CLI must not interfere with existing `.claude` directory structures

- **Business constraints:**
  - Must eliminate need for multiple `ckh-*` scripts (namespace pollution)
  - Installation experience must be simpler than current approach
  - Must work with existing settings.json format

- **Timeline constraints:**
  - Initial implementation focuses on `init`, `doctor`, and `hook` subcommands only
  - Future commands (spec management, config, etc.) are deferred

## Out of Scope

This feature does NOT include:
- Spec management commands (`ck spec list`, `ck spec status`) - future enhancement
- Config management commands (`ck config show/set`) - future enhancement
- Template management (`ck template create`) - future enhancement
- Automatic migration from file-based hooks - manual migration documented
- Interactive wizards or prompts (except `--force` confirmation)
- Remote spec file downloads (all resources bundled)
- Custom hook development tools or scaffolding
- Integration with other package managers besides `uv`