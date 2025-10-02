# Custom Slash Commands in Claude Code

> Research from local Claude Code documentation

## Overview

Custom slash commands allow you to define frequently-used prompts as Markdown files that Claude Code can execute. They provide a powerful way to standardize workflows, create reusable templates, and share best practices across teams.

## File Structure and Locations

### Project Commands (`.claude/commands/`)

Commands stored in your repository and shared with your team.

**Location**: `.claude/commands/`

**Characteristics**:
- Available only in the current project
- Shared with all team members via version control
- Show "(project)" suffix in `/help` listing
- Perfect for project-specific workflows

**Example**:
```bash
mkdir -p .claude/commands
echo "Analyze this code for performance issues and suggest optimizations:" > .claude/commands/optimize.md
```

### Personal Commands (`~/.claude/commands/`)

Commands available across all your projects.

**Location**: `~/.claude/commands/`

**Characteristics**:
- Available in all your projects
- Not shared with team members
- Show "(user)" suffix in `/help` listing
- Perfect for personal workflows

**Example**:
```bash
mkdir -p ~/.claude/commands
echo "Review this code for security vulnerabilities:" > ~/.claude/commands/security-review.md
```

### Namespacing with Subdirectories

Organize commands in subdirectories for better structure:

```bash
.claude/commands/
├── frontend/
│   ├── component.md      # Creates /component (project:frontend)
│   └── style-check.md     # Creates /style-check (project:frontend)
├── backend/
│   ├── api-test.md        # Creates /api-test (project:backend)
│   └── db-migrate.md      # Creates /db-migrate (project:backend)
└── review.md              # Creates /review (project)
```

**Important**:
- The subdirectory name appears in the command description but NOT in the command name
- Example: `.claude/commands/frontend/component.md` creates `/component` (not `/frontend/component`)
- Description shows: "(project:frontend)"
- Conflicts between user and project level commands are NOT supported
- Multiple commands with the same base filename can coexist if they're in different scopes (user vs project) or subdirectories

## File Format

Each custom command is a Markdown file where:
- **Filename** (without `.md` extension) becomes the command name
- **File content** defines what the command does
- **Optional YAML frontmatter** provides configuration

### Basic Example

Create `.claude/commands/refactor.md`:

```markdown
Refactor the selected code to improve readability and maintainability.
Focus on clean code principles and best practices.
```

Usage: `/refactor`

### Example with Frontmatter

Create `.claude/commands/security-check.md`:

```markdown
---
allowed-tools: Read, Grep, Glob
description: Run security vulnerability scan
model: claude-3-5-sonnet-20241022
---

Analyze the codebase for security vulnerabilities including:
- SQL injection risks
- XSS vulnerabilities
- Exposed credentials
- Insecure configurations
```

Usage: `/security-check`

## Frontmatter Options

| Field                      | Purpose                                                                 | Default                             |
|:---------------------------|:------------------------------------------------------------------------|:------------------------------------|
| `allowed-tools`            | List of tools the command can use                                       | Inherits from the conversation      |
| `argument-hint`            | Arguments expected for the slash command (shown in autocomplete)        | None                                |
| `description`              | Brief description of the command                                        | Uses the first line from the prompt |
| `model`                    | Specific model string (e.g., `claude-3-5-haiku-20241022`)              | Inherits from the conversation      |
| `disable-model-invocation` | Whether to prevent `SlashCommand` tool from calling this command        | false                               |

### Example with All Options

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
argument-hint: [message]
description: Create a git commit
model: claude-3-5-haiku-20241022
disable-model-invocation: false
---

Create a git commit with message: $ARGUMENTS
```

## Arguments and Placeholders

Commands support dynamic values through argument placeholders.

### Using `$ARGUMENTS` (All Arguments)

The `$ARGUMENTS` placeholder captures ALL arguments passed to the command as a single string.

**Command definition** (`.claude/commands/fix-issue.md`):
```markdown
Fix issue #$ARGUMENTS following our coding standards
```

**Usage**:
```
/fix-issue 123 high-priority
```

**Result**: `$ARGUMENTS` becomes `"123 high-priority"`

### Using Positional Parameters (`$1`, `$2`, `$3`, etc.)

Access specific arguments individually using positional parameters (like shell scripts).

**Command definition** (`.claude/commands/review-pr.md`):
```markdown
---
argument-hint: [pr-number] [priority] [assignee]
description: Review pull request
---

Review PR #$1 with priority $2 and assign to $3.
Focus on security, performance, and code style.
```

**Usage**:
```
/review-pr 456 high alice
```

**Result**:
- `$1` becomes `"456"`
- `$2` becomes `"high"`
- `$3` becomes `"alice"`

**When to use positional arguments**:
- Access arguments individually in different parts of your command
- Provide defaults for missing arguments
- Build more structured commands with specific parameter roles

### Advanced Example with Arguments

Create `.claude/commands/fix-issue.md`:
```markdown
---
argument-hint: [issue-number] [priority]
description: Fix a GitHub issue
---

Fix issue #$1 with priority $2.

Steps:
1. Check the issue description
2. Locate relevant code in our codebase
3. Implement the necessary changes
4. Add appropriate tests
5. Prepare a concise PR description
```

Usage: `/fix-issue 123 high`

## Bash Command Execution

Execute bash commands before the slash command runs using the `!` prefix. The output is included in the command context.

**Requirements**:
- MUST include `allowed-tools` with the `Bash` tool
- Can specify specific bash commands to allow using the format: `Bash(command:*)`

### Example: Git Commit Command

Create `.claude/commands/git-commit.md`:

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your task

Based on the above changes, create a single git commit.
```

### Example: Code Review with Git Info

Create `.claude/commands/code-review.md`:

```markdown
---
allowed-tools: Read, Grep, Glob, Bash(git diff:*)
description: Comprehensive code review
---

## Changed Files
!`git diff --name-only HEAD~1`

## Detailed Changes
!`git diff HEAD~1`

## Review Checklist

Review the above changes for:
1. Code quality and readability
2. Security vulnerabilities
3. Performance implications
4. Test coverage
5. Documentation completeness

Provide specific, actionable feedback organized by priority.
```

## File References with @

Include file contents in commands using the `@` prefix to reference files.

### Single File Reference

```markdown
# Reference a specific file
Review the implementation in @src/utils/helpers.js
```

### Multiple File References

```markdown
# Reference multiple files
Compare @src/old-version.js with @src/new-version.js
```

### Directory References

```markdown
# Reference a directory
What's the structure of @src/components?
```

### MCP Resource References

```markdown
# Reference MCP resources
Show me the data from @github:repos/owner/repo/issues
```

**Important**:
- File paths can be relative or absolute
- `@` file references add CLAUDE.md from the file's directory and parent directories to context
- Directory references show file listings, not contents
- You can reference multiple files in a single message

### Complete Example with File References

Create `.claude/commands/review-config.md`:

```markdown
---
description: Review configuration files
---

Review the following configuration files for issues:
- Package config: @package.json
- TypeScript config: @tsconfig.json
- Environment config: @.env.example

Check for:
1. Security issues
2. Outdated dependencies
3. Misconfigurations
4. Missing required settings
```

## Extended Thinking Mode

Slash commands can trigger extended thinking by including extended thinking keywords.

### Example with Thinking

```markdown
---
description: Architectural planning with deep analysis
---

Think deeply about the best approach for implementing OAuth2 authentication in our API.

Consider:
- Security implications
- Performance impact
- Scalability requirements
- Migration strategy from current auth system
```

**Trigger phrases**:
- "think" - triggers basic extended thinking
- "think hard", "think more", "think longer" - triggers deeper thinking

## The SlashCommand Tool

The `SlashCommand` tool allows Claude to execute custom slash commands programmatically during a conversation.

### How It Works

1. Claude has access to all available custom slash commands
2. Each command's metadata is included in context (up to character budget limit)
3. Claude can invoke commands automatically when appropriate
4. Commands must reference the slash name in instructions to be triggered

### Requirements for Automatic Invocation

**Your custom command MUST have**:
- The `description` frontmatter field populated (used in context)
- Be user-defined (built-in commands like `/compact` are NOT supported)

**Example to encourage Claude to use your command**:

```markdown
> Run /write-unit-test when you are about to start writing tests.
```

### Supported Commands

- User-defined custom commands (from `.claude/commands/` or `~/.claude/commands/`)
- Commands with `description` frontmatter populated
- Commands without `disable-model-invocation: true`

### NOT Supported

- Built-in commands like `/compact`, `/init`, `/help`
- Commands without `description` field
- Commands with `disable-model-invocation: true`

### Disabling SlashCommand Tool Entirely

```bash
/permissions
# Add to deny rules: SlashCommand
```

This will:
- Remove the SlashCommand tool from Claude's available tools
- Remove all slash command descriptions from context
- Prevent Claude from invoking any custom commands automatically

### Disabling Specific Commands

To prevent a specific slash command from automatic invocation:

```markdown
---
disable-model-invocation: true
description: Manual-only security scan
---

This command must be invoked manually by the user.
```

This will:
- Remove the command's metadata from context
- Prevent Claude from invoking it via the SlashCommand tool
- Still allow manual invocation by the user

### Permission Rules

The permission system supports:

**Exact match**:
```
SlashCommand:/commit
```
Allows only `/commit` with no arguments.

**Prefix match**:
```
SlashCommand:/review-pr:*
```
Allows `/review-pr` with any arguments.

### Character Budget Limit

The `SlashCommand` tool includes a character budget to limit the size of command descriptions shown to Claude.

**Default limit**: 15,000 characters

**Custom limit**: Set via `SLASH_COMMAND_TOOL_CHAR_BUDGET` environment variable

**What's included in the budget**:
- Each custom slash command's name
- Arguments hint
- Description

**When budget is exceeded**:
- Claude sees only a subset of available commands
- A warning shows in `/context` with "M of N commands"

### Debugging

For Claude Code versions >= 1.0.124, see which commands are available to the SlashCommand tool:

```bash
claude --debug
# Then trigger a query to see the command list
```

## Practical Examples for Spec-Related Commands

### 1. Spec Review Command

Create `.claude/commands/spec-review.md`:

```markdown
---
allowed-tools: Read, Grep, Glob
description: Review specification document for completeness
argument-hint: [spec-file-path]
---

Review the specification at @$1 for:

1. **Completeness**
   - Are all requirements clearly defined?
   - Are acceptance criteria specified?
   - Are edge cases covered?

2. **Clarity**
   - Is the language clear and unambiguous?
   - Are technical terms defined?
   - Are examples provided where needed?

3. **Feasibility**
   - Are the requirements technically feasible?
   - Are dependencies identified?
   - Are potential risks noted?

4. **Consistency**
   - Does it align with existing specs?
   - Are naming conventions consistent?
   - Are patterns followed consistently?

Provide specific, actionable feedback with line numbers.
```

Usage: `/spec-review docs/specs/feature-x.md`

### 2. Spec Implementation Plan

Create `.claude/commands/spec-implement.md`:

```markdown
---
allowed-tools: Read, Grep, Glob, Write
description: Create implementation plan from specification
argument-hint: [spec-file-path]
---

Read the specification at @$1 and create a detailed implementation plan.

## Your task

1. **Analysis**
   - Break down the spec into implementable components
   - Identify dependencies between components
   - List affected areas of the codebase

2. **Implementation Steps**
   - Create a numbered list of implementation steps
   - Include file paths that need changes
   - Specify test requirements for each step

3. **Risk Assessment**
   - Identify potential risks
   - Suggest mitigation strategies
   - Note breaking changes

4. **Estimation**
   - Estimate complexity for each step
   - Identify parallel vs. sequential work

Output the plan in a clear, structured format.
```

Usage: `/spec-implement docs/specs/new-feature.md`

### 3. Spec Compliance Check

Create `.claude/commands/spec-check.md`:

```markdown
---
allowed-tools: Read, Grep, Glob, Bash(git diff:*)
description: Check if implementation matches specification
argument-hint: [spec-file-path] [implementation-path]
---

## Context

Specification: @$1
Implementation: @$2

## Your task

Compare the implementation against the specification and verify:

1. **Requirements Coverage**
   - Are all specified requirements implemented?
   - List any missing features
   - List any extra features not in spec

2. **Behavioral Correctness**
   - Does behavior match specification?
   - Are edge cases handled as specified?
   - Are error cases handled correctly?

3. **API Contract**
   - Do function signatures match?
   - Are return values as specified?
   - Are exceptions as documented?

4. **Documentation**
   - Is code documented as required?
   - Are examples provided?
   - Is usage clear?

Provide a compliance report with:
- ✓ Compliant items
- ✗ Non-compliant items (with details)
- ? Ambiguous items (needing clarification)
```

Usage: `/spec-check docs/specs/auth.md src/auth/`

### 4. Spec Generator from Code

Create `.claude/commands/spec-generate.md`:

```markdown
---
allowed-tools: Read, Grep, Glob, Write
description: Generate specification document from existing code
argument-hint: [code-path] [output-spec-path]
---

## Your task

Analyze the code at @$1 and generate a specification document.

## Document Structure

1. **Overview**
   - Purpose and scope
   - High-level description
   - Key concepts

2. **Requirements**
   - Functional requirements
   - Non-functional requirements
   - Constraints

3. **API Specification**
   - Public interfaces
   - Function signatures
   - Parameters and return values
   - Error conditions

4. **Behavior Specification**
   - Normal flow
   - Edge cases
   - Error handling
   - State transitions

5. **Examples**
   - Usage examples
   - Code snippets
   - Common patterns

6. **Dependencies**
   - External dependencies
   - Internal dependencies
   - Environment requirements

Write the specification to $2 in clear, structured markdown.
```

Usage: `/spec-generate src/payment/ docs/specs/payment-system.md`

### 5. Spec Update from Changes

Create `.claude/commands/spec-update.md`:

```markdown
---
allowed-tools: Read, Edit, Bash(git diff:*)
description: Update specification to reflect code changes
argument-hint: [spec-file-path]
---

## Context

Current specification: @$1
Recent changes: !`git diff HEAD~5 --stat`
Detailed diff: !`git diff HEAD~5`

## Your task

1. **Identify Changes**
   - What code changes were made?
   - Which parts of the spec are affected?
   - Are there new features or behaviors?

2. **Update Specification**
   - Update affected sections
   - Add documentation for new features
   - Mark deprecated features
   - Update examples if needed

3. **Verify Consistency**
   - Ensure spec is internally consistent
   - Check all cross-references
   - Verify examples still work

4. **Summary**
   - List changes made to spec
   - Note any items needing manual review

Update the specification file and provide a summary of changes.
```

Usage: `/spec-update docs/specs/api.md`

### 6. Test Plan from Spec

Create `.claude/commands/spec-test-plan.md`:

```markdown
---
allowed-tools: Read, Write
description: Generate test plan from specification
argument-hint: [spec-file-path]
---

Read the specification at @$1 and create a comprehensive test plan.

## Test Plan Structure

1. **Test Strategy**
   - Testing approach
   - Test levels (unit, integration, e2e)
   - Coverage goals

2. **Test Cases**
   For each requirement:
   - Test case ID
   - Description
   - Preconditions
   - Test steps
   - Expected results
   - Priority

3. **Edge Cases**
   - Boundary conditions
   - Error conditions
   - Unexpected inputs

4. **Performance Tests**
   - Load tests
   - Stress tests
   - Benchmarks

5. **Test Data**
   - Required test data
   - Data generation approach
   - Cleanup procedures

Output a structured test plan document.
```

Usage: `/spec-test-plan docs/specs/checkout.md`

## Best Practices

### 1. Command Naming

- Use descriptive, action-oriented names
- Use hyphens for multi-word commands (e.g., `review-pr`, not `review_pr`)
- Keep names concise but clear
- Follow consistent naming patterns within your project

### 2. Description Writing

- Write clear, concise descriptions (shown in `/help`)
- Focus on what the command does, not how
- Include key use cases
- Keep under 100 characters when possible

### 3. Arguments Design

- Use `argument-hint` to document expected arguments
- Prefer positional parameters (`$1`, `$2`) for structured commands
- Use `$ARGUMENTS` for flexible, free-form input
- Provide examples in the description or frontmatter

### 4. Tool Permissions

- Only request tools the command actually needs
- Be specific with `Bash(command:*)` restrictions
- Consider security implications of tool access
- Document why tools are needed

### 5. Documentation

- Add comments explaining complex command logic
- Include usage examples in the command file
- Document any special requirements or dependencies
- Keep commands focused on a single purpose

### 6. Organization

- Use subdirectories to group related commands
- Separate user and project commands appropriately
- Keep command files in version control (for project commands)
- Document your command structure in project README

### 7. Testing

- Test commands with various argument combinations
- Verify bash command execution works correctly
- Check file references resolve properly
- Test with different permission levels

### 8. Performance

- Be mindful of character budget limits
- Keep descriptions concise to maximize available commands
- Use `disable-model-invocation: true` for manual-only commands
- Consider command execution time when using bash

### 9. Model Selection

- Use appropriate models for command complexity
- Consider cost vs. capability tradeoffs
- Test with default model before specifying
- Document why a specific model is needed

### 10. For Spec-Related Commands

- Always reference the spec file with `@` notation
- Include section headings for structured output
- Cross-reference implementation and spec
- Generate actionable, specific feedback
- Consider version control integration
- Maintain bidirectional traceability (spec ↔ code)

## Summary

Custom slash commands in Claude Code provide:

- **Standardization**: Consistent prompts across team and projects
- **Efficiency**: Quick access to complex, multi-step workflows
- **Flexibility**: Dynamic arguments and bash execution
- **Context**: File references and environment information
- **Automation**: Automatic invocation via SlashCommand tool
- **Organization**: Namespaced commands for clean structure

**Key takeaways**:
1. Commands are Markdown files in `.claude/commands/` (project) or `~/.claude/commands/` (personal)
2. Frontmatter provides configuration (tools, model, description, arguments)
3. Arguments use `$ARGUMENTS` (all) or `$1`, `$2` (positional)
4. Bash execution with `!` prefix, file references with `@` prefix
5. SlashCommand tool enables automatic invocation
6. Character budget limits prevent context overflow
7. Permissions system provides fine-grained control

## References

- [Slash Commands Documentation](/docs/claude-code/slash-commands) - Complete official reference
- [Slash Commands in SDK](/api/agent-sdk/slash-commands) - SDK integration guide
- [Common Workflows](/docs/claude-code/common-workflows) - Practical usage examples
- [IAM Guide](/docs/claude-code/iam) - Permissions and access control
- [Settings](/docs/claude-code/settings) - Configuration options
