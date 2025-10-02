# Spec-Driven Development for Claude Code

**Vision:** Bring structured, production-ready development workflow to Claude Code using Kiro's proven spec-driven methodology.

## The Problem

Current AI coding flow:
1. User prompts iteratively
2. Code gets generated
3. **Assumptions are implicit**
4. **Requirements are undocumented**
5. **Hard to track progress**
6. **Difficult to maintain**

Getting to production requires structure.

## The Solution

Spec-driven development: **Prompt → Requirements → Design → Tasks → Implementation**

Built entirely with Claude Code's existing features—no external tools needed.

## User Experience

### Creating a Spec

```bash
> /spec "Add user authentication with email/password and OAuth"

[Thinking mode activates - deep planning]

✓ Generated requirements.md (EARS notation)
✓ Generated design.md (architecture, data models)
✓ Created 12 tasks

Tasks:
 [ ] 1. Create User model with email/password fields
 [ ] 2. Implement password hashing (bcrypt)
 [ ] 3. Create authentication middleware
 ...
```

**Behind the scenes:**
- **Output style** enforces structure
- **Thinking mode** ensures thorough planning
- **TodoWrite** tracks all tasks
- **Custom slash command** triggers workflow
- Files saved to `.claude/specs/auth/`

### Implementing Tasks

```bash
> /spec-task 1

[Loads task context from spec]
[Implements with full context]
[Updates TodoWrite automatically]

✓ Task 1 complete: User model created
  Files: src/models/user.ts, tests/user.test.ts
```

**Behind the scenes:**
- **Slash command** reads spec files
- **Steering files** provide project patterns
- **Hooks** update task status on file changes
- **TodoWrite** marks task complete

### Keeping Specs Synced

```bash
# You make manual code changes
> git commit -m "refactor auth flow"

[Hook detects code changes in auth module]
[Automatically updates design.md]

ℹ Spec updated: design.md now reflects new auth flow
```

**Behind the scenes:**
- **PostToolUse hook** detects relevant changes
- **Custom agent** analyzes code vs spec
- Auto-updates spec files

### Team Collaboration

```bash
> /spec-export auth

✓ Exported to specs/auth.md
  - Requirements (EARS notation)
  - Design decisions
  - Implementation tasks
  - Current status: 8/12 tasks complete

Share with your team for review!
```

## Feature Mapping

| Kiro Feature | Claude Code Implementation | UX Benefit |
|--------------|---------------------------|------------|
| **Specs** | Output Style + Slash Commands | Structured responses automatically |
| **Task List** | TodoWrite (built-in) | Native progress tracking |
| **Hooks** | Hooks (UserPromptSubmit, PostToolUse) | Auto-sync code ↔ specs |
| **Planning** | Thinking Mode | Deep reasoning for requirements |
| **Context** | Steering Files + CLAUDE.md | Project-specific patterns |
| **Automation** | Custom Agents | Specialized spec-only planning |

## Implementation Stack

**Phase 1: Core Workflow**
1. Output style: `.claude/output-styles/spec-driven.md`
2. Slash commands: `.claude/commands/spec/*.md`
3. Leverage TodoWrite for task tracking

**Phase 2: Automation**
4. Hooks: Auto-update specs when code changes
5. Custom agent: `@spec-creator` for planning

**Phase 3: Polish**
6. Steering files: EARS templates, patterns
7. MCP server: Cross-project spec management (future)

## Success Criteria

**For Developers:**
- ✓ Requirements are explicit and documented
- ✓ Design decisions are captured
- ✓ Tasks are sequenced and trackable
- ✓ Specs stay synced with code
- ✓ No context switching (stays in Claude Code)

**For Teams:**
- ✓ Shareable, reviewable specs
- ✓ Clear implementation plans
- ✓ Onboarding documentation built-in
- ✓ Architecture decisions preserved

## Why This Works

**Kiro proved:** Developers want structure + AI coding
**Claude Code has:** All the primitives to build it
**We provide:** The methodology + configuration

No new tools. No integrations. Just better workflow.

---

## Current Status

✅ **Research Complete** - All Claude Code and Kiro features documented
✅ **Synthesis Complete** - Feature mapping and Phase 1 plan ready
⏳ **Phase 1 Implementation** - 5 config files to create (4-6 hours)

See `synthesis/phase1-implementation.md` for next steps.
