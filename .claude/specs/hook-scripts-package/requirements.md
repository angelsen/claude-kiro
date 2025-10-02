# Feature: Hook Scripts as Installable Python Package

## Overview
Transform the current project-specific hook scripts (like spec-file-matcher.py) into a proper Python package structure with installable command-line scripts. This enables users to install Claude Kiro hooks globally via `uv tool install claude-kiro` and reference them by name in their Claude Code settings, eliminating path dependencies and enabling code reuse across multiple hook scripts.

## User Stories

### Story 1: Install and Use Hooks Globally
**As a** Claude Code user
**I want** to install Claude Kiro hooks as a global tool
**So that** I can use them in any project without copying files or managing paths

**Acceptance Criteria (EARS notation):**
- WHEN a user runs `uv tool install claude-kiro`, THE SYSTEM SHALL install all hook scripts as globally available commands
- WHEN a user configures `.claude/settings.local.json` with hook command names (e.g., `ckh-post-file-ops`), THE SYSTEM SHALL execute the installed scripts without requiring file paths
- WHEN a user updates Claude Kiro via `uv tool install --upgrade claude-kiro`, THE SYSTEM SHALL update all hook scripts to the latest version
- WHEN a hook script is not found in PATH, THE SYSTEM SHALL provide a clear error message suggesting installation

### Story 2: Prevent Duplicate Hook Messages
**As a** developer working with Claude Code
**I want** hook messages to appear only once per file per session
**So that** my workflow isn't interrupted by repetitive notifications

**Acceptance Criteria (EARS notation):**
- WHEN a file is edited for the first time in a session, THE SYSTEM SHALL display the appropriate spec context message
- WHEN the same file is edited again in the same session, THE SYSTEM SHALL suppress the duplicate message
- WHEN a new Claude Code session starts, THE SYSTEM SHALL reset the notification tracking for all files
- WHEN session cache files are older than 24 hours, THE SYSTEM SHALL automatically clean them up

### Story 3: Share Code Between Hook Scripts
**As a** Claude Kiro maintainer
**I want** shared utility modules for common functionality
**So that** code is DRY and bugs are fixed in one place

**Acceptance Criteria (EARS notation):**
- WHEN multiple hook scripts need session tracking, THE SYSTEM SHALL provide a shared SessionTracker module
- WHEN multiple hooks need to parse spec files, THE SYSTEM SHALL provide a shared SpecParser module
- WHEN a bug is fixed in a shared module, THE SYSTEM SHALL apply the fix to all hooks using that module
- WHEN a new hook is created, THE SYSTEM SHALL enable reuse of existing shared utilities

### Story 4: Maintain Backward Compatibility
**As a** existing Claude Kiro user
**I want** my current hooks to continue working during migration
**So that** I can upgrade at my own pace

**Acceptance Criteria (EARS notation):**
- WHEN a user has existing file-based hooks configured, THE SYSTEM SHALL continue to support them
- WHEN documentation is provided, THE SYSTEM SHALL include migration instructions from file-based to package-based hooks
- WHEN both old and new hooks exist, THE SYSTEM SHALL not conflict or duplicate functionality

## Non-Functional Requirements
- **Performance:** Hook execution time must remain under 100ms for session cache operations
- **Storage:** Session cache files should use minimal disk space (< 1MB per session)
- **Security:** Session cache must be stored in user-specific temp directories with appropriate permissions
- **Compatibility:** Must work on Python 3.11+ on Windows, macOS, and Linux
- **Installation:** Single command installation via `uv tool install` with no additional dependencies
- **Naming:** Hook command names follow `ckh-{event}-{action}` pattern for clarity

## Constraints
- Technical constraints:
  - Must use only Python standard library (no external dependencies)
  - Must read input from stdin as JSON (Claude Code hook protocol)
  - Must exit with appropriate codes (0 for success, 2 for blocking)
  - Must work with existing Claude Code hook infrastructure
- Business constraints:
  - Must maintain the existing hook behavior and message format
  - Must be installable via uv/pip tooling
- Timeline constraints:
  - Initial implementation focuses on post-file-ops hook only
  - Additional hooks can be migrated incrementally

## Out of Scope
- This feature does NOT include:
  - A CLI tool for managing hooks (just the hook scripts themselves)
  - Automatic configuration of `.claude/settings.local.json`
  - Migration of all possible future hooks (only post-file-ops initially)
  - GUI or interactive configuration tools
  - Hook testing framework (though hooks should be testable)
  - Custom hook development tools or templates