# Claude Kiro: Spec-Driven Development for Claude Code

A unified CLI tool and methodology that brings spec-driven development workflow to Claude Code.

**📖 [Documentation](https://angelsen.github.io/claude-kiro/)** | **🚀 [Getting Started](https://angelsen.github.io/claude-kiro/getting-started.html)** | **⚙️ [CLI Reference](https://angelsen.github.io/claude-kiro/cli.html)**

## What This Is

Claude Kiro `ck` provides:
- **Automated project setup** for spec-driven development
- **Smart hooks** that provide spec context while coding
- **Slash commands** for structured workflows
- **Output styles** that enforce disciplined responses

**Prompt → Requirements → Design → Tasks → Implementation**

## Repository Structure

```
├── VISION.md                    # Project vision and goals
├── synthesis/                   # Implementation guides
│   ├── kiro-to-claude-mapping.md
│   └── phase1-implementation.md
├── research/                    # Feature research from docs
│   ├── claude-code/             # Claude Code capabilities
│   └── kiro/                    # Kiro methodology
└── resources/                   # Scraped documentation
    └── scraped/
        ├── docs.claude.com/     # 255 pages
        └── kiro.dev/            # 89 pages
```

## Quick Start

```bash
# Install Claude Kiro globally
uv tool install claude-kiro

# Initialize your project
cd your-project
ck init

# Verify setup
ck doctor
```

That's it! Your project is now configured for spec-driven development.

## Installation

### Install Claude Kiro (Global Tool)

```bash
# Install from PyPI
uv tool install claude-kiro

# Or install from source in editable mode
git clone https://github.com/angelsen/claude-kiro.git
cd claude-kiro
uv tool install . --editable
```

This installs the `ck` command globally, which provides:
- `ck init` - Set up a project for spec-driven development
- `ck doctor` - Verify your setup is working
- `ck hook` - Manage Claude Code hook integration
- `ck --hook` - Hook runner for Claude Code (hidden command)

### Initialize Your Project

```bash
cd your-project
ck init
```

This creates:
- `.claude/output-styles/spec-driven.md` - Enforces structured responses
- `.claude/commands/spec/` - Slash commands for specs
- `.claude/settings.local.json` - Hook configuration
- `.claude/CLAUDE.md` - Project context template

### What the Hooks Do

The hooks provide intelligent spec context:
- **When editing spec files:** Shows which task you're implementing
- **When editing new files:** Suggests creating a spec first
- **Smart caching:** Shows messages only once per file per session (no spam!)

## How It Works

1. **Initialize:** `ck init` sets up your project with all necessary files
2. **Create specs:** `/spec:create "feature"` - Generate requirements, design, and tasks
3. **Implement:** `/spec:implement task` - Execute tasks with full context
4. **Track progress:** TodoWrite tracks implementation automatically
5. **Stay aligned:** Hooks provide context and maintain spec-driven discipline

## CLI Commands Reference

### Main Commands
- `ck init [--force]` - Initialize a project with spec-driven setup
- `ck doctor` - Check your Claude Kiro setup health
- `ck hook list` - Show available hooks
- `ck hook status` - Display configured hooks
- `ck hook test <name>` - Test a hook with sample data
- `ck hook config` - Generate settings.json configuration

### Claude Code Slash Commands (Created by `ck init`)
- `/spec:create <feature>` - Create a new specification
- `/spec:implement <task>` - Implement a spec task
- `/spec:review <spec>` - Review an existing spec

## Key Features

- **EARS notation** for testable requirements: `WHEN [condition] THE SYSTEM SHALL [behavior]`
- **3-phase workflow** with approval gates between phases
- **TodoWrite integration** for native task tracking
- **Smart hook context** that tracks what you're working on
- **Zero configuration** after running `ck init`

## Documentation Sources

All research extracted from local scraped docs:
- Claude Code: 255 pages (docs.claude.com)
- Kiro: 89 pages (kiro.dev)
- Combined: 10 research docs, 2 synthesis guides

## Development

### Code Formatting

```bash
make format-docs  # Format HTML/CSS/JS with prettier
```

## Implementation Status

- ✅ CLI tool (`ck`) - Complete with all commands
- ✅ Hook system - Smart context injection working
- ✅ Slash commands - `/spec:create`, `/spec:implement`, `/spec:review`
- ✅ Output styles - Spec-driven responses enforced
- ✅ Project setup automation - `ck init` configures everything

## Why This Exists

**Problem:** AI coding is fast but chaotic - implicit assumptions, undocumented requirements, hard to maintain.

**Solution:** Structured specs before code. Proven by Kiro, implemented in Claude Code.

**Result:** Production-ready development with AI assistance.

---

Built for developers who want structure without sacrificing speed.
