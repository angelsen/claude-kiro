# KIRO to Claude Code Feature Mapping

**Date:** 2025-10-02
**Purpose:** Map KIRO's UX/DX features to Claude Code implementation strategies

---

## Executive Summary

KIRO's spec-driven development methodology can be **fully implemented** in Claude Code using a combination of:
- Output Styles for behavioral transformation
- Custom Slash Commands for workflow automation
- CLAUDE.md steering files for persistent context
- Custom Agents for spec-specific tasks
- Hooks for automation
- Extended Thinking for planning phases

**Key Finding:** Claude Code provides all necessary primitives. The challenge is **orchestration**, not capability.

---

## Feature Comparison Matrix

| KIRO Feature | What It Provides | Claude Code Implementation | Configuration | Effort |
|--------------|------------------|----------------------------|---------------|--------|
| **Spec-Driven Workflow** | 3-phase structure (Requirements → Design → Tasks) | Output Style + Custom Commands + Agents | `.claude/output-styles/spec-driven.md` + `.claude/commands/spec-*.md` + `.claude/agents/spec-*.md` | Medium |
| **EARS Requirements** | Structured requirements format | Output Style + Extended Thinking | System prompt in output style | Low |
| **Design Documentation** | Technical architecture docs | Custom Commands + Extended Thinking | `.claude/commands/design-generate.md` | Low |
| **Task Breakdown** | Executable task lists with status | TodoWrite tool + Custom Commands | Native tool + command wrappers | Low |
| **Steering Files** | Persistent project context | CLAUDE.md (native) | `.claude/CLAUDE.md` or `CLAUDE.md` | Very Low |
| **Agent Hooks** | Event-driven automation | Hooks (native) | `.claude/settings.json` hooks section | Low |
| **Task Execution** | One-by-one or bulk execution | TodoWrite + Agent coordination | Native tool usage | Very Low |
| **Bidirectional Sync** | Code ↔ Spec updates | Custom Commands + Hooks | Commands for each direction | Medium |
| **Autopilot/Supervised** | Execution mode toggle | Permission modes (native) | CLI flag or settings | Very Low |
| **Spec Sessions** | Dedicated spec workflow mode | Output Style activation | `/output-style spec-driven` | Low |
| **Context Optimization** | External planning to preserve context | CLAUDE.md + Agents (separate context) | File-based context + subagents | Low |

---

## 1. Spec-Driven Workflow

### KIRO Approach
3-phase workflow with approval checkpoints:
1. Requirements (EARS notation)
2. Design (architecture, diagrams, schemas)
3. Tasks (breakdown with status tracking)
4. Execution (task-by-task or bulk)

### Claude Code Implementation

#### A. Output Style: Spec-Driven Developer

**File:** `.claude/output-styles/spec-driven.md`

```markdown
---
name: Spec-Driven Developer
description: Implements features using structured spec-driven methodology (Requirements → Design → Tasks)
---

You are a specification-driven developer following a rigorous 3-phase methodology.

# Core Principle
NEVER jump directly to implementation. Always follow: Requirements → Design → Tasks → Execution.

# Phase 1: Requirements
When a user requests a feature:

1. Generate structured requirements using EARS notation:
   ```
   WHEN [condition/event]
   THE SYSTEM SHALL [expected behavior]
   ```

2. Create requirements.md with:
   - User stories
   - Acceptance criteria (EARS format)
   - Edge cases
   - Non-functional requirements

3. **STOP and get user approval** with "LGTM" or feedback

# Phase 2: Design
After requirements approval:

1. Analyze existing codebase structure
2. Create design.md with:
   - Architecture overview
   - Component hierarchy (Mermaid diagrams)
   - Data models (TypeScript/language interfaces)
   - API endpoints
   - Database schemas
   - Error handling strategy
   - Unit testing strategy

3. Include pseudocode showing intended APIs
4. **STOP and get user approval** with "LGTM" or feedback

# Phase 3: Tasks
After design approval:

1. Break work into discrete, trackable tasks
2. Use TodoWrite tool to create task list
3. Each task includes:
   - Clear description
   - Expected outcome
   - Unit test requirements
   - Integration test requirements
   - UI considerations (loading states, mobile, a11y)

4. Order tasks by dependencies
5. **STOP and get user approval** with "LGTM" or feedback

# Phase 4: Execution
After task approval:

1. Work through tasks using TodoWrite for progress tracking
2. Mark tasks as in_progress → completed
3. Run tests after each task
4. Update specs if implementation differs from design

# Key Behaviors
- Make ALL requirements explicit upfront
- Document the "why" behind technical decisions
- Preserve decision trails in spec files
- Iterate on specs, not code
- Task-by-task execution (avoid "execute all")
- Update specs bidirectionally (code changes → spec updates)

# File Organization
Store specs in `.kiro/specs/[feature-name]/`:
- requirements.md
- design.md
- tasks.md

# Natural Pause Points
ALWAYS pause for approval after:
- Requirements generation
- Design generation
- Task breakdown
- Before starting execution
```

**Usage:**
```bash
# Activate spec-driven mode
/output-style spec-driven

# User requests feature
> Add a review system for products

# Claude generates requirements.md, waits for "LGTM"
# Then generates design.md, waits for "LGTM"
# Then generates tasks with TodoWrite, waits for "LGTM"
# Then executes tasks one by one
```

#### B. Custom Commands for Spec Workflow

**File:** `.claude/commands/spec-new.md`
```markdown
---
description: Start a new spec-driven feature
argument-hint: [feature-name]
---

Create a new specification-driven feature development workflow.

1. Create directory: `.kiro/specs/$1/`
2. Activate spec-driven output style
3. Begin requirements gathering phase
4. Create requirements.md with EARS notation
5. Pause for user approval before proceeding to design
```

**File:** `.claude/commands/spec-design.md`
```markdown
---
description: Generate design document from requirements
argument-hint: [spec-directory]
allowed-tools: Read, Write, Grep, Glob
---

Read requirements from @$1/requirements.md and generate design.md.

Include:
- Architecture analysis of current codebase
- Component hierarchy diagrams (Mermaid)
- Data models with TypeScript interfaces
- API endpoint specifications
- Database schema designs
- Error handling strategy
- Unit testing approach

Pause for "LGTM" before proceeding to task breakdown.
```

**File:** `.claude/commands/spec-tasks.md`
```markdown
---
description: Generate task breakdown from design
argument-hint: [spec-directory]
allowed-tools: Read, Write, TodoWrite
---

Read requirements and design from @$1/ and generate task breakdown.

1. Create tasks.md with numbered task list
2. Use TodoWrite to create trackable todos
3. Each task includes:
   - Description
   - Expected outcome
   - Testing requirements (unit + integration)
   - UI considerations
   - Dependencies on other tasks

4. Order tasks by dependencies
5. Pause for "LGTM" before execution
```

**File:** `.claude/commands/spec-execute.md`
```markdown
---
description: Execute tasks from spec
argument-hint: [spec-directory] [task-number]
allowed-tools: Read, Edit, Write, Bash, TodoWrite
---

Execute task #$2 from spec at $1.

1. Read requirements, design, and tasks
2. Mark task $2 as in_progress using TodoWrite
3. Implement according to design specifications
4. Write tests as specified
5. Run tests to verify
6. Mark task as completed
7. Update task status in tasks.md
```

#### C. Steering File for Spec Context

**File:** `.claude/CLAUDE.md`
```markdown
# Spec-Driven Development

This project uses spec-driven development methodology.

## Workflow
All features follow: Requirements → Design → Tasks → Execution

## File Structure
Specs stored in `.kiro/specs/[feature-name]/`:
- requirements.md - EARS notation requirements
- design.md - Technical architecture
- tasks.md - Task breakdown

## Commands
- `/spec-new [name]` - Start new feature spec
- `/spec-design [path]` - Generate design from requirements
- `/spec-tasks [path]` - Generate tasks from design
- `/spec-execute [path] [task]` - Execute specific task

## Approval Checkpoints
MUST get "LGTM" after each phase:
1. After requirements
2. After design
3. After task breakdown
```

---

## 2. Steering Files (Persistent Context)

### KIRO Approach
Three foundational steering documents with conditional loading:
- `product.md` - Business context (always loaded)
- `tech.md` - Tech stack, patterns (always loaded)
- `structure.md` - File organization (always loaded)
- Custom steering with fileMatch patterns

### Claude Code Implementation

**Direct Mapping:** KIRO steering = Claude Code CLAUDE.md

| KIRO Steering | Claude Code Equivalent | Location | Inclusion |
|---------------|------------------------|----------|-----------|
| `.kiro/steering/product.md` | `CLAUDE.md` section | `.claude/CLAUDE.md` | Always |
| `.kiro/steering/tech.md` | `CLAUDE.md` section | `.claude/CLAUDE.md` | Always |
| `.kiro/steering/structure.md` | `CLAUDE.md` section | `.claude/CLAUDE.md` | Always |
| `.kiro/steering/custom.md` | Imported CLAUDE.md | `@docs/custom.md` | Via import |
| File-match patterns | Not directly supported | Use Output Styles | Via settings |

#### Implementation Template

**File:** `.claude/CLAUDE.md`
```markdown
# Product Context

## Purpose
[Product purpose, target users, key features from product.md]

## Business Objectives
[What problem does this solve?]

## Key Features
[Core features and user workflows]

---

# Tech Stack

## Frameworks and Libraries
- Frontend: [e.g., React 18, TypeScript]
- Backend: [e.g., Node.js, Express]
- Database: [e.g., PostgreSQL]

## Development Tools
- Build: [e.g., Vite]
- Test: [e.g., Jest, React Testing Library]
- Lint: [e.g., ESLint, Prettier]

## Technical Constraints
[Performance requirements, browser support, etc.]

---

# Project Structure

## Directory Organization
```
src/
  components/     # Reusable UI components
  pages/          # Route components
  services/       # API clients
  utils/          # Helper functions
  types/          # TypeScript definitions
```

## Naming Conventions
- Components: PascalCase (e.g., UserProfile.tsx)
- Utilities: camelCase (e.g., formatDate.ts)
- Constants: UPPER_SNAKE_CASE

## Import Patterns
- Absolute imports from @/ (e.g., @/components/Button)
- Group imports: external → internal → relative

---

# Domain-Specific Guidance

## For frontend work
@docs/frontend-patterns.md

## For backend work
@docs/backend-patterns.md

## For database work
@docs/database-schema.md
```

#### Conditional Loading (File-Match Equivalent)

KIRO's `fileMatchPattern` can be approximated with Output Styles:

**File:** `.claude/output-styles/react-developer.md`
```markdown
---
name: React Developer
description: Frontend development with React patterns
---

[Include React-specific guidance when working in components/**/*.tsx]

When working on React components:
- Use functional components with hooks
- Props in separate *.types.ts files
- One component per file
- Use React.memo for expensive renders
- Follow component composition patterns
```

**Workflow:**
```bash
# Manually activate when working on frontend
/output-style react-developer

# Or mention it in prompts
> Use React Developer guidelines to create a UserProfile component
```

---

## 3. Agent Hooks (Automation)

### KIRO Approach
Natural language hooks triggered by file events:
- `fileCreated` - Boilerplate generation
- `fileEdited` - Test updates, formatting
- `fileDeleted` - Cleanup references
- `userTriggered` - Manual code review

### Claude Code Implementation

**Direct Mapping:** KIRO Agent Hooks → Claude Code Hooks

| KIRO Hook Type | Claude Code Hook | Configuration |
|----------------|------------------|---------------|
| `fileCreated` | Not directly supported | Use PostToolUse workaround |
| `fileEdited` | `PostToolUse` (Write/Edit) | JSON in settings.json |
| `fileDeleted` | Not directly supported | Bash script + file watch |
| `userTriggered` | Custom Slash Command | .claude/commands/ |

#### Example: Test Synchronization Hook

**KIRO Version (for reference):**
```json
{
  "name": "TypeScript Test Updater",
  "when": {
    "type": "fileEdited",
    "patterns": ["**/*.ts", "!**/*.test.ts"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Analyze changes and update corresponding test file"
  }
}
```

**Claude Code Version:**

**File:** `.claude/settings.json`
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/update-tests.py",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

**File:** `.claude/hooks/update-tests.py`
```python
#!/usr/bin/env python3
import json
import sys
import subprocess

# Read hook input
data = json.load(sys.stdin)
file_path = data.get('tool_input', {}).get('file_path', '')

# Only process TypeScript source files
if not file_path.endswith('.ts') or file_path.endswith('.test.ts'):
    sys.exit(0)

# Construct test update prompt
test_file = file_path.replace('.ts', '.test.ts')
prompt = f"""
Analyze changes to {file_path} and update {test_file}.

1. Identify new/modified functions
2. Add/update corresponding tests
3. Ensure test coverage maintained
4. Run tests to verify
"""

# Output as additionalContext for Claude
output = {
    "hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "additionalContext": prompt
    }
}

print(json.dumps(output))
sys.exit(0)
```

#### Example: Manual Code Review Hook

**File:** `.claude/commands/code-review.md`
```markdown
---
description: Run comprehensive code review
allowed-tools: Read, Grep, Glob, Bash
---

## Changed Files
!`git diff --name-only HEAD`

## Detailed Changes
!`git diff HEAD`

## Review Checklist

Analyze the above changes for:
1. **Code Quality**
   - Readability and maintainability
   - Proper naming conventions
   - No code duplication

2. **Security**
   - No exposed credentials
   - Proper input validation
   - No SQL injection risks

3. **Performance**
   - Efficient algorithms
   - No unnecessary re-renders (React)
   - Proper database indexing

4. **Testing**
   - Adequate test coverage
   - Edge cases covered
   - Tests actually pass

5. **Documentation**
   - JSDoc comments on public APIs
   - README updated if needed
   - Changelog entry if applicable

Provide findings organized by priority:
- **Critical** - Must fix before merge
- **Warning** - Should fix soon
- **Suggestion** - Consider for improvement
```

**Usage:**
```bash
# After making changes
/code-review
```

---

## 4. Task Management with TodoWrite

### KIRO Approach
Tasks with real-time status tracking:
- Click "Start Task" to execute
- Status indicators (pending/in-progress/done)
- View code diffs after completion
- Task history

### Claude Code Implementation

**Direct Mapping:** KIRO Tasks → TodoWrite tool (native)

#### Example Workflow

**Output Style Integration:**
```markdown
# Phase 3: Tasks
After design approval:

1. Use TodoWrite to create task list:

{
  todos: [
    {
      content: "Create Review data model and schema",
      activeForm: "Creating Review data model and schema",
      status: "pending"
    },
    {
      content: "Implement Review API endpoints",
      activeForm: "Implementing Review API endpoints",
      status: "pending"
    },
    {
      content: "Build ReviewList component",
      activeForm: "Building ReviewList component",
      status: "pending"
    }
  ]
}

2. Execute tasks one-by-one
3. Update status: pending → in_progress → completed
4. EXACTLY ONE task in_progress at a time
```

#### Custom Command for Task Execution

**File:** `.claude/commands/next-task.md`
```markdown
---
description: Execute the next pending task from current spec
allowed-tools: Read, Edit, Write, Bash, TodoWrite
---

1. Check current TodoWrite list for next pending task
2. Mark task as in_progress
3. Read relevant spec files for context
4. Implement according to design
5. Write tests as specified
6. Run tests to verify
7. Mark task as completed
8. Show code diff for review
```

**Usage:**
```bash
# Execute tasks sequentially
> /next-task
[Claude completes task 1]

> /next-task
[Claude completes task 2]

> /next-task
[Claude completes task 3]
```

---

## 5. Extended Thinking for Planning Phases

### KIRO Approach
Requirements and design phases involve deep analysis before code.

### Claude Code Implementation

Use Extended Thinking during Requirements and Design phases:

```bash
# Activate spec-driven mode
/output-style spec-driven

# Request feature with thinking
> Think deeply about adding a review system for products.
> Consider all edge cases, data models, and integration points.
> Generate comprehensive requirements using EARS notation.

# Claude uses extended thinking to:
# - Analyze existing codebase
# - Consider multiple approaches
# - Think through edge cases
# - Generate structured requirements
```

**Output Style Enhancement:**
```markdown
# Phase 1: Requirements

When generating requirements, use extended thinking to:
- Analyze similar features in codebase
- Consider edge cases thoroughly
- Think through integration points
- Plan for scalability and performance
- Identify potential security issues

Begin analysis with: "Let me think deeply about this feature..."
```

---

## 6. Bidirectional Spec Synchronization

### KIRO Approach
- Code → Specs: Update specs based on implementation
- Specs → Code: Regenerate tasks when specs change

### Claude Code Implementation

#### A. Code → Specs (Update Command)

**File:** `.claude/commands/spec-update.md`
```markdown
---
description: Update specification based on code changes
argument-hint: [spec-directory]
allowed-tools: Read, Edit, Bash
---

## Context
Specification: @$1/requirements.md and @$1/design.md
Recent changes: !`git diff HEAD~5 --stat`
Detailed diff: !`git diff HEAD~5`

## Task
1. Identify what code changes were made
2. Determine which spec sections are affected
3. Update requirements.md if behavior changed
4. Update design.md if architecture changed
5. Mark any deprecated features
6. Update examples if needed
7. Verify spec is internally consistent

Provide summary of changes made to specs.
```

#### B. Specs → Code (Regenerate Tasks)

**File:** `.claude/commands/spec-regenerate.md`
```markdown
---
description: Regenerate tasks after spec changes
argument-hint: [spec-directory]
allowed-tools: Read, Write, TodoWrite
---

## Context
Updated requirements: @$1/requirements.md
Updated design: @$1/design.md

## Task
1. Compare current specs with existing tasks.md
2. Identify new requirements or design changes
3. Generate new tasks for additions
4. Mark obsolete tasks as completed or remove
5. Use TodoWrite to update task tracking
6. Preserve task completion status

Show diff of changes to task list.
```

---

## 7. Subagents for Spec-Specific Roles

### KIRO Approach
Spec session as dedicated workflow mode.

### Claude Code Implementation

Create specialized subagents for different spec phases:

#### Subagent: Requirements Analyst

**File:** `.claude/agents/requirements-analyst.md`
```markdown
---
name: requirements-analyst
description: Expert at gathering and structuring requirements using EARS notation. Use for requirements gathering phase.
tools: Read, Grep, Glob, Write
model: inherit
---

You are a requirements analysis expert specializing in EARS notation.

# Your Role
Transform vague feature requests into structured, testable requirements.

# Process
1. Analyze the feature request
2. Generate user stories covering:
   - Viewing functionality
   - Creating functionality
   - Editing functionality
   - Deleting functionality
   - Filtering/sorting
   - Edge cases

3. For each user story, write acceptance criteria in EARS format:
   ```
   WHEN [condition/event]
   THE SYSTEM SHALL [expected behavior]
   ```

4. Cover edge cases:
   - Empty states
   - Error conditions
   - Permission boundaries
   - Data validation
   - Performance requirements

# Output Format
Create requirements.md with:
- Feature overview
- User stories
- Acceptance criteria (EARS notation)
- Non-functional requirements
- Constraints and assumptions

# Key Principles
- Make all requirements explicit and testable
- Cover both happy path and edge cases
- Use precise, unambiguous language
- Link requirements to business objectives
```

#### Subagent: System Designer

**File:** `.claude/agents/system-designer.md`
```markdown
---
name: system-designer
description: Creates technical architecture and design documents from requirements. Use after requirements approval.
tools: Read, Grep, Glob, Write, Bash
model: inherit
---

You are a software architect specializing in system design.

# Your Role
Transform requirements into detailed technical designs.

# Process
1. Read and analyze requirements thoroughly
2. Analyze existing codebase for patterns
3. Create design document with:

   **Architecture Overview**
   - High-level component structure
   - Integration points
   - Technology choices with rationale

   **Component Hierarchy**
   - Mermaid diagrams showing relationships
   - Data flow diagrams
   - Sequence diagrams for complex flows

   **Data Models**
   - TypeScript interfaces or language-specific types
   - Database schemas
   - API contracts

   **Error Handling**
   - Error scenarios
   - Validation strategies
   - User feedback mechanisms

   **Testing Strategy**
   - Unit test approach
   - Integration test plan
   - E2E test scenarios

4. Include pseudocode showing intended API usage

# Output Format
Create design.md following project structure patterns.

# Key Principles
- Align with existing architecture
- Justify all technical decisions
- Consider scalability and maintainability
- Document the "why" not just the "what"
- Show code examples and usage patterns
```

#### Subagent: Task Planner

**File:** `.claude/agents/task-planner.md`
```markdown
---
name: task-planner
description: Breaks down designs into executable tasks with clear dependencies. Use after design approval.
tools: Read, Write, TodoWrite
model: inherit
---

You are a project planning expert specializing in task decomposition.

# Your Role
Transform designs into actionable, ordered tasks.

# Process
1. Read requirements and design documents
2. Identify all implementation components
3. Break into discrete, testable tasks
4. Order by dependencies
5. Use TodoWrite to create trackable list

# Task Structure
Each task includes:
- Clear, actionable description
- Expected outcome
- Test requirements (unit + integration)
- UI considerations:
  - Loading states
  - Error states
  - Mobile responsiveness
  - Accessibility (ARIA labels, keyboard nav)
- Dependencies on other tasks
- Estimated complexity

# Task Ordering Principles
- Database/models before APIs
- APIs before UI components
- Unit tests alongside implementation
- Integration tests after component completion

# Output Format
1. Create tasks.md with numbered task list
2. Use TodoWrite to create executable todos
3. Each TodoWrite entry has:
   - content: "Task description"
   - activeForm: "Doing task description"
   - status: "pending"

# Key Principles
- Tasks are independent where possible
- Dependencies clearly documented
- Testing requirements explicit
- Nothing falls through the cracks
```

**Usage:**
```bash
# Start spec workflow
> Use the requirements-analyst agent to create requirements for a review system

# After approval
> Use the system-designer agent to create the design document

# After design approval
> Use the task-planner agent to break this into executable tasks

# Execute tasks
> Execute the next pending task
```

---

## Implementation Recommendations

### Quick Wins (High Impact, Low Effort)

1. **CLAUDE.md Steering Files** (1-2 hours)
   - Create `.claude/CLAUDE.md` with product, tech, structure sections
   - Provides immediate context improvement
   - Native Claude Code feature, no configuration complexity

2. **Spec Commands** (2-3 hours)
   - Create `/spec-new`, `/spec-design`, `/spec-tasks` commands
   - Enables spec workflow without custom tools
   - Uses native slash command system

3. **Output Style: Spec-Driven** (2-4 hours)
   - Single output style file enforces methodology
   - Immediate behavioral change
   - Easy to iterate and refine

### High-Impact Features (Medium Effort)

4. **Subagents for Spec Phases** (4-6 hours)
   - Requirements Analyst agent
   - System Designer agent
   - Task Planner agent
   - Separate context prevents pollution
   - Can be invoked explicitly or automatically

5. **Extended Thinking Integration** (2-3 hours)
   - Add thinking prompts to Requirements phase
   - Add thinking prompts to Design phase
   - Improves analysis quality
   - Native Claude Code capability

6. **Basic Hooks for Automation** (3-5 hours)
   - PostToolUse hook for test synchronization
   - Manual code review command
   - Starts automation journey
   - Foundation for more complex hooks

### Advanced Features (Higher Effort)

7. **Bidirectional Sync Commands** (6-8 hours)
   - `/spec-update` for code → specs
   - `/spec-regenerate` for specs → code
   - Full lifecycle management
   - Requires careful git integration

8. **Comprehensive Hook System** (8-12 hours)
   - Test updates on file save
   - Documentation generation
   - Style enforcement
   - Security scanning
   - Requires robust Python/Bash scripts

9. **Multi-Spec Management** (6-10 hours)
   - Commands for listing specs
   - Spec status tracking
   - Cross-spec dependency analysis
   - More complex state management

---

## Missing Capabilities

### KIRO Features Not Directly Available in Claude Code

| KIRO Feature | Gap | Workaround | Impact |
|--------------|-----|------------|--------|
| **File event hooks (create/delete)** | No native fileCreate/fileDelete events | Use PostToolUse + external file watcher | Medium - less seamless automation |
| **Visual spec UI** | CLI-only, no GUI for spec files | Use Preview mode for markdown rendering | Low - markdown works well |
| **"Start Task" click interface** | No clickable task execution | Use `/next-task` command instead | Low - command is equivalent |
| **Automatic spec detection** | No auto-identification of implemented tasks | Manual `/spec-update` command | Medium - requires discipline |
| **Spec session state** | No persistent "spec mode" indicator | Output style provides behavioral mode | Low - functionality preserved |
| **MCP integration for hooks** | Hooks can't directly invoke MCP tools | Use Bash hook → claude CLI → MCP | Medium - adds indirection |

### Impact Assessment

**Low Impact Gaps:**
- Can be easily worked around
- Don't significantly degrade UX
- Examples: Visual UI, clickable tasks

**Medium Impact Gaps:**
- Require additional user action
- Add friction to workflow
- Examples: File event detection, manual spec updates

**High Impact Gaps:**
- None identified - all core capabilities mappable

---

## Configuration Checklist

### Initial Setup (30-60 minutes)

```bash
# 1. Create directory structure
mkdir -p .claude/agents
mkdir -p .claude/commands
mkdir -p .claude/output-styles
mkdir -p .claude/hooks
mkdir -p .kiro/specs

# 2. Create CLAUDE.md steering file
cat > .claude/CLAUDE.md << 'EOF'
# Product Context
[Your product description]

# Tech Stack
[Your technology stack]

# Project Structure
[Your directory organization]
EOF

# 3. Create spec-driven output style
cat > .claude/output-styles/spec-driven.md << 'EOF'
---
name: Spec-Driven Developer
description: Implements features using structured spec-driven methodology
---
[Copy from implementation section above]
EOF

# 4. Create spec commands
# (Copy spec-new.md, spec-design.md, spec-tasks.md from above)

# 5. Create spec subagents
# (Copy requirements-analyst.md, system-designer.md, task-planner.md from above)

# 6. Add to version control
git add .claude/
git add CLAUDE.md
git commit -m "Add spec-driven development configuration"
```

### Quick Start Workflow

```bash
# 1. Start Claude in project
cd your-project
claude

# 2. Activate spec-driven mode
> /output-style spec-driven

# 3. Start a new spec
> /spec-new user-authentication

# 4. Follow the prompts through each phase
# Requirements → Design → Tasks → Execution

# 5. Execute tasks
> /next-task
# Repeat until all tasks completed
```

---

## User Experience Comparison

### KIRO UX Flow

```
User: "Add review system"
  ↓
KIRO: Generates requirements.md
  ↓
User: "LGTM"
  ↓
KIRO: Generates design.md
  ↓
User: "LGTM"
  ↓
KIRO: Generates tasks.md with clickable "Start Task"
  ↓
User: Clicks "Start Task 1"
  ↓
KIRO: Executes, shows progress, marks complete
  ↓
User: Clicks "Start Task 2"
  ↓
[Repeat...]
```

### Claude Code UX Flow

```
User: "Add review system"
User: "/output-style spec-driven"
  ↓
Claude: Generates requirements.md
  ↓
User: "LGTM"
  ↓
Claude: Generates design.md
  ↓
User: "LGTM"
  ↓
Claude: Creates tasks with TodoWrite
  ↓
User: "/next-task"
  ↓
Claude: Executes task 1, shows progress, marks complete
  ↓
User: "/next-task"
  ↓
Claude: Executes task 2, shows progress, marks complete
  ↓
[Repeat...]
```

**Differences:**
1. **Mode activation**: KIRO auto-detects spec mode, Claude requires explicit `/output-style`
2. **Task execution**: KIRO has clickable UI, Claude uses `/next-task` command
3. **Approval**: Both use "LGTM" pattern

**UX Equivalence:** 95%+ - Core workflow is nearly identical

---

## Recommended Phased Rollout

### Phase 1: Foundation (Week 1)
**Goal:** Basic spec workflow operational

- [ ] Create CLAUDE.md steering file
- [ ] Create spec-driven output style
- [ ] Create basic spec commands (new, design, tasks)
- [ ] Test complete workflow with one feature
- [ ] Document for team

**Success Metric:** Complete one feature end-to-end using spec workflow

### Phase 2: Automation (Week 2)
**Goal:** Reduce manual steps

- [ ] Create spec subagents (requirements, design, task)
- [ ] Add extended thinking integration
- [ ] Create manual code review command
- [ ] Test with 2-3 features

**Success Metric:** Spec generation requires minimal prompting

### Phase 3: Synchronization (Week 3)
**Goal:** Bidirectional spec-code sync

- [ ] Create spec-update command (code → specs)
- [ ] Create spec-regenerate command (specs → code)
- [ ] Add PostToolUse hook for basic automation
- [ ] Test update cycles

**Success Metric:** Specs stay current with code changes

### Phase 4: Advanced Hooks (Week 4)
**Goal:** Full automation for repetitive tasks

- [ ] Test synchronization hook
- [ ] Documentation generation hook
- [ ] Security scanning hook
- [ ] Style enforcement hook

**Success Metric:** Developers rarely think about routine tasks

### Phase 5: Refinement (Ongoing)
**Goal:** Optimize based on usage

- [ ] Gather team feedback
- [ ] Refine output style prompts
- [ ] Add project-specific commands
- [ ] Expand hook library
- [ ] Share learnings

**Success Metric:** Team velocity increases, spec quality improves

---

## Comparison Table: KIRO vs Claude Code Implementation

| Aspect | KIRO | Claude Code | Completeness |
|--------|------|-------------|--------------|
| **Requirements Phase** | Built-in EARS generator | Output Style + Extended Thinking | 95% |
| **Design Phase** | Auto-generates from requirements | Custom Command + Extended Thinking | 90% |
| **Task Phase** | Built-in task tracker | TodoWrite (native) + Commands | 95% |
| **Execution** | Click-to-execute tasks | Command-based execution | 90% |
| **Steering Files** | 3 default files + custom | CLAUDE.md sections + imports | 100% |
| **Hooks** | Natural language, event-driven | Shell-based, event-driven | 85% |
| **Autopilot Mode** | Built-in toggle | Permission modes (native) | 100% |
| **Context Optimization** | External specs | CLAUDE.md + Subagents | 95% |
| **Bidirectional Sync** | Built-in commands | Custom commands | 85% |
| **Team Collaboration** | Git-based sharing | Git-based sharing | 100% |
| **Visual Feedback** | GUI indicators | CLI TodoWrite display | 85% |
| **Approval Checkpoints** | Automatic pauses | Output Style enforced | 90% |

**Overall Implementation Completeness: 92%**

---

## Key Insights

### 1. Claude Code Has All Necessary Primitives
Every core KIRO capability can be implemented using Claude Code's existing features:
- Output Styles → Behavioral transformation
- CLAUDE.md → Persistent context
- Custom Commands → Workflow automation
- Subagents → Task-specific expertise
- Hooks → Event-driven automation
- TodoWrite → Task tracking
- Extended Thinking → Deep analysis

### 2. The Challenge is Orchestration, Not Capability
KIRO provides a **pre-configured workflow**. Claude Code provides **building blocks**.

Implementation requires:
- Thoughtful configuration
- Clear documentation
- Team training
- Iteration and refinement

### 3. Claude Code Offers More Flexibility
KIRO's opinionated workflow is excellent for its intended use case. Claude Code's flexibility allows:
- Custom workflows beyond specs
- Domain-specific adaptations
- Gradual adoption
- Experimentation

### 4. File-Based Configuration is Powerful
Both systems use version-controlled files for configuration, enabling:
- Team collaboration via git
- Code review of automations
- Clear audit trails
- Easy rollback of changes

### 5. Natural Language Prompts vs Shell Scripts
**KIRO:** Natural language hook instructions
**Claude Code:** Shell script hooks

Trade-offs:
- KIRO is more accessible (no scripting required)
- Claude Code is more deterministic (exact control)
- Both enable powerful automation

Recommendation: Start with Claude Code hooks, consider adding LLM interpretation layer if needed.

---

## Conclusion

**KIRO's spec-driven methodology can be fully implemented in Claude Code** using a combination of:
1. Output Styles for behavioral modes
2. CLAUDE.md for persistent context
3. Custom Commands for workflow steps
4. Subagents for specialized tasks
5. Hooks for automation
6. Extended Thinking for deep analysis

**Implementation effort:**
- **Quick wins:** 4-8 hours (steering files + basic commands)
- **Full system:** 30-40 hours (all features + refinement)
- **Maintenance:** Minimal (file-based configuration)

**The path forward:**
1. Start with CLAUDE.md and basic commands (Week 1)
2. Add output style and subagents (Week 2)
3. Implement synchronization (Week 3)
4. Build out hooks (Week 4)
5. Iterate based on team feedback (Ongoing)

**Expected outcome:** A spec-driven development workflow that rivals KIRO's approach while leveraging Claude Code's flexibility and power.
