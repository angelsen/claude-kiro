# Spec-Driven Development for Claude Code

Configuration files and methodology to bring Kiro's structured development workflow to Claude Code.

## What This Is

A set of Claude Code configurations (output styles, slash commands, hooks) that implement spec-driven development:

**Prompt → Requirements → Design → Tasks → Implementation**

No external tools. Pure Claude Code primitives.

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

See `synthesis/phase1-implementation.md` for complete setup (5 config files, 4-6 hours).

**Core files to create:**
- `.claude/commands/spec/create.md` - Requirements → Design → Tasks workflow
- `.claude/commands/spec/implement.md` - Task-by-task implementation
- `.claude/output-styles/spec-driven.md` - Enforces structured responses
- `.claude/CLAUDE.md` - Project context (optional)

## How It Works

1. **`/spec-create "feature"`** - Generate requirements (EARS notation), design, and tasks
2. **TodoWrite** - Tracks implementation progress automatically
3. **`/spec-implement 1`** - Execute tasks with full context
4. **Hooks** (Phase 2) - Keep specs synced with code changes

## Key Insights

- **92% feature parity** with Kiro using Claude Code primitives
- **EARS notation** for testable requirements: `WHEN [condition] THE SYSTEM SHALL [behavior]`
- **3-phase workflow** with approval gates between phases
- **TodoWrite integration** for native task tracking
- **No custom code** - pure configuration

## Documentation Sources

All research extracted from local scraped docs:
- Claude Code: 255 pages (docs.claude.com)
- Kiro: 89 pages (kiro.dev)
- Combined: 10 research docs, 2 synthesis guides

## Implementation Status

- ✅ Research complete (10 docs)
- ✅ Synthesis complete (feature mapping + Phase 1 plan)
- ⏳ Phase 1 implementation (pending)
- ⏳ Phase 2 automation (pending)

## Why This Exists

**Problem:** AI coding is fast but chaotic - implicit assumptions, undocumented requirements, hard to maintain.

**Solution:** Structured specs before code. Proven by Kiro, implemented in Claude Code.

**Result:** Production-ready development with AI assistance.

---

Built for developers who want structure without sacrificing speed.
