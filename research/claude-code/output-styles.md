# Claude Code Output Styles - Comprehensive Research

**Research Date:** 2025-10-02
**Source:** Local Claude Code documentation in `/home/fredrik/Projects/Python/project-autumn-25/claude-kiro/resources/scraped/docs.claude.com/`

---

## Table of Contents

1. [Overview](#overview)
2. [How Output Styles Work](#how-output-styles-work)
3. [Built-in Output Styles](#built-in-output-styles)
4. [Configuration Format](#configuration-format)
5. [Creating Custom Output Styles](#creating-custom-output-styles)
6. [Usage and Management](#usage-and-management)
7. [Output Styles vs Other Features](#output-styles-vs-other-features)
8. [Best Practices](#best-practices)
9. [Integration with SDK](#integration-with-sdk)
10. [Key Insights for Spec-Driven Development](#key-insights-for-spec-driven-development)

---

## Overview

Output styles allow you to use Claude Code as any type of agent while keeping its core capabilities, such as running local scripts, reading/writing files, and tracking TODOs. They are a powerful way to adapt Claude Code for uses beyond software engineering.

**Key Characteristics:**
- Directly modify Claude Code's system prompt
- Persistent across sessions (saved as files)
- Can be shared across projects or kept user-specific
- Completely replace software engineering-specific instructions

**Source:** `/home/fredrik/Projects/Python/project-autumn-25/claude-kiro/resources/scraped/docs.claude.com/docs/claude-code/output-styles.md`

---

## How Output Styles Work

Output styles directly modify Claude Code's system prompt with the following mechanics:

### System Prompt Modification

1. **Default Behavior**: Claude Code's **Default** output style uses the existing system prompt, designed to help complete software engineering tasks efficiently.

2. **Non-default Output Styles**:
   - Exclude instructions specific to code generation and efficient output normally built into Claude Code
   - Remove instructions like responding concisely and verifying code with tests
   - Add their own custom instructions to the system prompt instead

### Application Scope

- Changes apply at the **local project level**
- Saved in `.claude/settings.local.json`
- Can also be configured at user level in `~/.claude/output-styles`

**Source:** `/home/fredrik/Projects/Python/project-autumn-25/claude-kiro/resources/scraped/docs.claude.com/docs/claude-code/output-styles.md` (lines 26-47)

---

## Built-in Output Styles

### 1. Default

The existing system prompt designed for software engineering tasks.

**Purpose:** Efficient completion of coding tasks

### 2. Explanatory

**Purpose:** Educational mode that provides "Insights" while helping with software engineering tasks

**Behavior:**
- Provides insights between helping complete tasks
- Helps understand implementation choices
- Explains codebase patterns
- Maintains software engineering capabilities

**Use Case:** Learning codebases and understanding Claude's decision-making

### 3. Learning

**Purpose:** Collaborative, learn-by-doing mode

**Behavior:**
- Shares "Insights" while coding
- Asks you to contribute small, strategic pieces of code
- Adds `TODO(human)` markers for you to implement
- Interactive teaching approach

**Use Case:** Hands-on learning and skill development

**Source:** `/home/fredrik/Projects/Python/project-autumn-25/claude-kiro/resources/scraped/docs.claude.com/docs/claude-code/output-styles.md` (lines 9-24)

---

## Configuration Format

### Markdown File Structure

Output styles are stored as markdown files with YAML frontmatter:

```markdown
---
name: My Custom Style
description: A brief description of what this style does, to be displayed to the user
---

# Custom Style Instructions

You are an interactive CLI tool that helps users with software engineering
tasks. [Your custom instructions here...]

## Specific Behaviors

[Define how the assistant should behave in this style...]
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Display name for the output style |
| `description` | Yes | Brief description shown to users when selecting styles |

### Content Section

The markdown content after the frontmatter contains:
- Role definition
- Behavioral instructions
- Specific guidelines
- Output format preferences
- Any domain-specific knowledge

**Source:** `/home/fredrik/Projects/Python/project-autumn-25/claude-kiro/resources/scraped/docs.claude.com/docs/claude-code/output-styles.md` (lines 58-73)

---

## Creating Custom Output Styles

### Method 1: Interactive Creation with Claude

```bash
/output-style:new I want an output style that ...
```

**Process:**
1. Describe what you want the output style to do
2. Claude helps create the style configuration
3. Automatically saved to `~/.claude/output-styles/`
4. Available across all projects

### Method 2: Manual File Creation

#### User-Level (Available Across Projects)

Location: `~/.claude/output-styles/`

```bash
mkdir -p ~/.claude/output-styles
cat > ~/.claude/output-styles/code-reviewer.md << 'EOF'
---
name: Code Reviewer
description: Thorough code review assistant
---

You are an expert code reviewer.

For every code submission:
1. Check for bugs and security issues
2. Evaluate performance
3. Suggest improvements
4. Rate code quality (1-10)
EOF
```

#### Project-Level (Project-Specific)

Location: `.claude/output-styles/`

```bash
mkdir -p .claude/output-styles
# Create style file in project directory
```

### SDK Example (TypeScript)

```typescript
import { writeFile, mkdir } from "fs/promises";
import { join } from "path";
import { homedir } from "os";

async function createOutputStyle(
  name: string,
  description: string,
  prompt: string
) {
  // User-level: ~/.claude/output-styles
  // Project-level: .claude/output-styles
  const outputStylesDir = join(homedir(), ".claude", "output-styles");

  await mkdir(outputStylesDir, { recursive: true });

  const content = `---
name: ${name}
description: ${description}
---

${prompt}`;

  const filePath = join(
    outputStylesDir,
    `${name.toLowerCase().replace(/\s+/g, "-")}.md`
  );
  await writeFile(filePath, content, "utf-8");
}

// Example: Create a code review specialist
await createOutputStyle(
  "Code Reviewer",
  "Thorough code review assistant",
  `You are an expert code reviewer.

For every code submission:
1. Check for bugs and security issues
2. Evaluate performance
3. Suggest improvements
4. Rate code quality (1-10)`
);
```

**Sources:**
- `/home/fredrik/Projects/Python/project-autumn-25/claude-kiro/resources/scraped/docs.claude.com/docs/claude-code/output-styles.md` (lines 49-77)
- `/home/fredrik/Projects/Python/project-autumn-25/claude-kiro/resources/scraped/docs.claude.com/api/agent-sdk/modifying-system-prompts.md` (lines 148-191)

---

## Usage and Management

### Activating Output Styles

#### Via CLI Commands

1. **Access menu:**
   ```bash
   /output-style
   ```
   Opens interactive menu to select output style

2. **Direct selection:**
   ```bash
   /output-style explanatory
   ```
   Directly switch to named style

3. **Via config menu:**
   ```bash
   /config
   ```
   Access output style settings from main config

#### Via Settings File

Edit `.claude/settings.local.json`:

```json
{
  "outputStyle": "Explanatory"
}
```

#### Via SDK

When using the Agent SDK, output styles are loaded when you include `settingSources`:

```typescript
// TypeScript
for await (const message of query({
  prompt: "Help me with this task",
  options: {
    systemPrompt: {
      type: "preset",
      preset: "claude_code",
    },
    settingSources: ["user", "project"], // Loads output styles
  },
})) {
  // Process messages
}
```

**Sources:**
- `/home/fredrik/Projects/Python/project-autumn-25/claude-kiro/resources/scraped/docs.claude.com/docs/claude-code/output-styles.md` (lines 36-47)
- `/home/fredrik/Projects/Python/project-autumn-25/claude-kiro/resources/scraped/docs.claude.com/docs/claude-code/settings.md` (line 61)

---

## Output Styles vs Other Features

### Output Styles vs CLAUDE.md

| Feature | Output Styles | CLAUDE.md |
|---------|--------------|-----------|
| **System Prompt** | Completely replaces default | Adds as user message after system prompt |
| **Software Engineering Instructions** | Turned off | Preserved |
| **Scope** | Behavioral transformation | Additional context/instructions |
| **When to Use** | Changing Claude's role/behavior | Adding project context, conventions |

**Key Difference:** Output styles "turn off" parts of Claude Code's default system prompt specific to software engineering. CLAUDE.md adds content without editing the default prompt.

### Output Styles vs --append-system-prompt

| Feature | Output Styles | --append-system-prompt |
|---------|--------------|------------------------|
| **System Prompt** | Replaces default | Appends to system prompt |
| **Persistence** | Saved as files | Session-only (CLI flag) |
| **Software Engineering Instructions** | Turned off | Preserved |
| **Management** | File-based, reusable | Code/CLI based |

### Output Styles vs Agents (Sub-agents)

| Feature | Output Styles | Agents |
|---------|--------------|--------|
| **Scope** | Main agent loop | Specific delegated tasks |
| **Modifications** | System prompt only | System prompt + tools + model + context |
| **Context** | Same conversation | Separate context window |
| **Invocation** | Active for entire session | Invoked for specific tasks |

**Key Difference:** Output styles affect the main conversation behavior. Agents are specialized assistants invoked for specific tasks with their own context.

### Output Styles vs Custom Slash Commands

**Conceptual Difference:**
- **Output Styles**: "Stored system prompts"
- **Custom Slash Commands**: "Stored prompts"

| Feature | Output Styles | Slash Commands |
|---------|--------------|----------------|
| **Purpose** | Change how Claude behaves | Store frequently-used prompts |
| **Persistence** | Active for session | Execute on demand |
| **Scope** | Entire conversation | Single invocation |

**Sources:**
- `/home/fredrik/Projects/Python/project-autumn-25/claude-kiro/resources/scraped/docs.claude.com/docs/claude-code/output-styles.md` (lines 79-99)
- `/home/fredrik/Projects/Python/project-autumn-25/claude-kiro/resources/scraped/docs.claude.com/api/agent-sdk/modifying-system-prompts.md` (lines 344-358)

---

## Best Practices

### When to Use Output Styles

**Best for:**
- Persistent behavior changes across sessions
- Team-shared configurations
- Specialized assistants (code reviewer, data scientist, DevOps expert)
- Complex prompt modifications that need versioning
- Non-software engineering use cases

**Examples:**
- Creating a dedicated SQL optimization assistant
- Building a security-focused code reviewer
- Developing a teaching assistant with specific pedagogy
- Data analysis workflows
- Documentation generation

### Design Guidelines

1. **Be Specific About Behavior**
   - Define clear role and expertise area
   - Include specific instructions and examples
   - Document expected output formats

2. **Document the Purpose**
   - Write clear `description` field
   - Explain when this style should be used
   - Include use case examples in the prompt

3. **Structure the Prompt**
   - Use markdown headings for organization
   - Include checklists or step-by-step processes
   - Define specific behaviors and constraints

4. **Version Control**
   - Save project-level styles in `.claude/output-styles/`
   - Commit to source control for team sharing
   - Document changes when updating styles

### Example: Code Reviewer Style

```markdown
---
name: Code Reviewer
description: Thorough code review assistant focusing on quality, security, and performance
---

You are an expert code reviewer ensuring high standards.

## Review Process

When reviewing code:
1. Analyze for bugs and edge cases
2. Check security vulnerabilities
3. Evaluate performance implications
4. Assess code readability and maintainability
5. Verify test coverage

## Output Format

Provide feedback organized by priority:
- **Critical**: Must fix before merging
- **Warnings**: Should fix soon
- **Suggestions**: Consider for improvement

Include specific examples and recommendations for each issue.
```

**Source:** `/home/fredrik/Projects/Python/project-autumn-25/claude-kiro/resources/scraped/docs.claude.com/api/agent-sdk/modifying-system-prompts.md` (lines 380-394)

---

## Integration with SDK

### Using Output Styles with Agent SDK

The Agent SDK supports multiple approaches to system prompt customization:

#### Approach 1: Load Output Styles via Setting Sources

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

const messages = [];

for await (const message of query({
  prompt: "Review this code",
  options: {
    systemPrompt: {
      type: "preset",
      preset: "claude_code",
    },
    settingSources: ["project", "user"], // Loads output styles from files
  },
})) {
  messages.push(message);
}
```

#### Approach 2: Append to Claude Code Preset

```typescript
const messages = [];

for await (const message of query({
  prompt: "Help me write a Python function",
  options: {
    systemPrompt: {
      type: "preset",
      preset: "claude_code",
      append: "Always include detailed docstrings and type hints in Python code.",
    },
  },
})) {
  messages.push(message);
}
```

#### Approach 3: Custom System Prompt

```typescript
const customPrompt = `You are a Python coding specialist.
Follow these guidelines:
- Write clean, well-documented code
- Use type hints for all functions
- Include comprehensive docstrings
- Prefer functional programming patterns when appropriate
- Always explain your code choices`;

for await (const message of query({
  prompt: "Create a data processing pipeline",
  options: {
    systemPrompt: customPrompt,
  },
})) {
  messages.push(message);
}
```

### Comparison of SDK Approaches

| Feature | Output Styles (via settingSources) | systemPrompt with append | Custom systemPrompt |
|---------|-----------------------------------|-------------------------|---------------------|
| **Persistence** | Per-project file | Session only | Session only |
| **Reusability** | Across projects | Code duplication | Code duplication |
| **Management** | CLI + files | In code | In code |
| **Default tools** | Preserved | Preserved | Lost (unless included) |
| **Built-in safety** | Maintained | Maintained | Must be added |
| **Environment context** | Automatic | Automatic | Must be provided |
| **Customization level** | Replace default | Additions only | Complete control |
| **Version control** | With project | With code | With code |

**Important Note:** The `claude_code` system prompt preset does NOT automatically load CLAUDE.md or output styles without explicitly setting `settingSources`.

**Source:** `/home/fredrik/Projects/Python/project-autumn-25/claude-kiro/resources/scraped/docs.claude.com/api/agent-sdk/modifying-system-prompts.md` (lines 142-359)

---

## Key Insights for Spec-Driven Development

### 1. Behavioral Transformation Architecture

Output styles enable complete behavioral transformation while preserving tool capabilities. This is crucial for:

- **Multi-Agent Systems**: Different agents can have fundamentally different behaviors using the same toolset
- **Workflow Specialization**: Create specialized workflows (review, debug, optimize) as output styles
- **Domain Adaptation**: Transform Claude Code for non-programming domains (data analysis, documentation, research)

### 2. Hierarchical Configuration System

Understanding the configuration hierarchy is essential:

```
Enterprise Managed Policies (highest priority)
    ↓
Command Line Arguments
    ↓
Local Project Settings (.claude/settings.local.json)
    ↓
Shared Project Settings (.claude/settings.json)
    ↓
User Settings (~/.claude/settings.json)
```

Output styles interact with this hierarchy through:
- User-level: `~/.claude/output-styles/`
- Project-level: `.claude/output-styles/`
- Settings reference: `"outputStyle": "StyleName"` in settings files

### 3. System Prompt Engineering Principles

From Claude 4 best practices and output styles documentation:

**Be Explicit:**
- Output styles should include explicit instructions for desired behaviors
- Explain WHY behaviors are important, not just WHAT to do
- Provide context and motivation behind instructions

**Example from documentation:**
```text
# Less effective:
NEVER use ellipses

# More effective:
Your response will be read aloud by a text-to-speech engine,
so never use ellipses since the text-to-speech engine will
not know how to pronounce them.
```

**Structured Guidelines:**
- Use markdown headings for organization
- Include checklists and step-by-step processes
- Provide examples of desired behaviors
- Define output formats explicitly

### 4. Integration Patterns

#### Pattern 1: Layered Customization

Combine multiple customization mechanisms:

```
Output Style (base behavior)
    + CLAUDE.md (project context)
    + systemPrompt append (session-specific additions)
    = Complete customization
```

#### Pattern 2: Specialized Agents

Create output styles for different roles:
- Code Reviewer (quality focus)
- Debugger (problem-solving focus)
- Data Scientist (analysis focus)
- Technical Writer (documentation focus)

Each maintains tool access while changing behavioral patterns.

#### Pattern 3: Context Preservation

Output styles work with context management:
- Separate from conversation context
- Compatible with context compaction
- Can reference memory files (CLAUDE.md)
- Preserved across sessions via settings

### 5. File-Based Configuration Benefits

Output styles use file-based configuration, enabling:

**Version Control:**
```bash
.claude/
  output-styles/
    code-reviewer.md
    debugger.md
    optimizer.md
```

**Team Collaboration:**
- Share styles via git
- Review and iterate on behavioral patterns
- Establish team standards

**Programmatic Generation:**
- Generate styles based on project analysis
- Template-based style creation
- Dynamic style composition

### 6. Limitations and Considerations

**What Output Styles Cannot Do:**
- Cannot modify available tools (use agents for that)
- Cannot change model selection (use settings for that)
- Cannot affect permission rules
- Cannot add new capabilities to Claude Code

**What Output Styles Excel At:**
- Changing response style and tone
- Defining specialized workflows
- Teaching domain-specific approaches
- Establishing output formats
- Modifying decision-making patterns

### 7. Spec-Driven Development Applications

**For Autonomous Agents:**
```markdown
---
name: Spec-Driven Developer
description: Implements features based on formal specifications
---

You are a specification-driven developer. For every task:

1. Request or locate the formal specification
2. Parse specification into testable requirements
3. Create test suite from specifications
4. Implement to satisfy tests
5. Verify against original specification

Always work from specs, never from assumptions.
```

**For Test-First Development:**
```markdown
---
name: Test-First Developer
description: Always writes tests before implementation
---

You are a test-first developer. Your workflow:

1. Understand the requirement
2. Write comprehensive tests FIRST
3. Run tests (they should fail)
4. Implement minimal code to pass tests
5. Refactor while maintaining green tests
6. Document test coverage

NEVER write implementation before tests exist.
```

**For Code Quality Enforcement:**
```markdown
---
name: Quality Enforcer
description: Proactively maintains code quality standards
---

You are a code quality enforcer. After any code changes:

1. Run linters and formatters
2. Check test coverage (minimum 80%)
3. Verify documentation completeness
4. Scan for security issues
5. Evaluate performance implications
6. Provide actionable feedback

Do not accept code that fails quality checks.
```

### 8. Best Practices Summary

From all documentation sources:

1. **Start Simple**: Use built-in styles (Explanatory, Learning) to understand patterns
2. **Generate with Claude**: Use `/output-style:new` for initial creation, then customize
3. **Be Explicit**: Include detailed instructions with examples and rationale
4. **Organize Content**: Use markdown structure for clarity
5. **Version Control**: Save project styles in `.claude/output-styles/`
6. **Document Purpose**: Clear `description` field helps team understanding
7. **Iterate Based on Usage**: Refine styles based on actual usage patterns
8. **Combine Approaches**: Layer output styles with CLAUDE.md and agents

### 9. Technical Implementation Notes

**File Naming Convention:**
- Lowercase with hyphens: `code-reviewer.md`
- Descriptive names that indicate purpose
- Avoid special characters except hyphens

**Settings Integration:**
```json
{
  "outputStyle": "Explanatory",
  "model": "claude-sonnet-4-5-20250929",
  "permissions": {
    "allow": ["Read", "Write", "Edit", "Bash"]
  }
}
```

**SDK Integration Points:**
- `settingSources`: Loads output styles from files
- `systemPrompt.preset`: Uses Claude Code's base prompt
- `systemPrompt.append`: Adds session-specific instructions
- Custom `systemPrompt`: Full control (loses default behaviors)

### 10. Future Considerations

Based on documentation patterns:

- **Composable Styles**: Potential for combining multiple styles
- **Conditional Activation**: Styles that activate based on context
- **Dynamic Generation**: Programmatically creating styles based on project analysis
- **Style Libraries**: Sharing style collections across organizations
- **Style Testing**: Frameworks for validating style effectiveness

---

## Source Files Reference

All information extracted from local documentation:

1. **Primary Source:**
   - `/home/fredrik/Projects/Python/project-autumn-25/claude-kiro/resources/scraped/docs.claude.com/docs/claude-code/output-styles.md`

2. **SDK Integration:**
   - `/home/fredrik/Projects/Python/project-autumn-25/claude-kiro/resources/scraped/docs.claude.com/api/agent-sdk/modifying-system-prompts.md`

3. **Settings Context:**
   - `/home/fredrik/Projects/Python/project-autumn-25/claude-kiro/resources/scraped/docs.claude.com/docs/claude-code/settings.md`

4. **Related Features:**
   - `/home/fredrik/Projects/Python/project-autumn-25/claude-kiro/resources/scraped/docs.claude.com/docs/claude-code/sub-agents.md`
   - `/home/fredrik/Projects/Python/project-autumn-25/claude-kiro/resources/scraped/docs.claude.com/docs/claude-code/slash-commands.md`
   - `/home/fredrik/Projects/Python/project-autumn-25/claude-kiro/resources/scraped/docs.claude.com/docs/claude-code/memory.md`

5. **Best Practices:**
   - `/home/fredrik/Projects/Python/project-autumn-25/claude-kiro/resources/scraped/docs.claude.com/docs/build-with-claude/prompt-engineering/claude-4-best-practices.md`

---

## Conclusion

Output styles are a powerful mechanism for transforming Claude Code's behavior while preserving its core tool capabilities. They enable:

- **Behavioral Specialization**: Create role-specific configurations
- **Team Standardization**: Share behavioral patterns via version control
- **Domain Adaptation**: Extend Claude Code beyond software engineering
- **Workflow Optimization**: Define and enforce specific workflows
- **Educational Modes**: Teaching and learning-focused interactions

The file-based configuration system integrates cleanly with existing tools (CLAUDE.md, agents, slash commands) while providing a clear separation of concerns: output styles define HOW Claude behaves, while other mechanisms define WHAT Claude knows and can do.

For spec-driven development, output styles provide a foundation for creating rigorous, test-first, specification-driven workflows that can be consistently applied across projects and teams.
