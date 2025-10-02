# TodoWrite Tool in Claude Code

> Comprehensive guide to the TodoWrite tool for task tracking and progress management in Claude Code.

## Overview

The TodoWrite tool provides a structured way to manage tasks and display progress to users. The Claude Agent SDK includes built-in todo functionality that helps organize complex workflows and keep users informed about task progression.

## Tool API

### Tool Name
`TodoWrite`

### Input Schema

```typescript
interface TodoWriteInput {
  /**
   * The updated todo list
   */
  todos: Array<{
    /**
     * The task description (imperative form)
     * Example: "Run tests", "Build the project"
     */
    content: string;

    /**
     * The task status
     */
    status: 'pending' | 'in_progress' | 'completed';

    /**
     * Active form of the task description (present continuous)
     * Example: "Running tests", "Building the project"
     */
    activeForm: string;
  }>;
}
```

### Output Schema

```typescript
interface TodoWriteOutput {
  /**
   * Success message
   */
  message: string;

  /**
   * Current todo statistics
   */
  stats: {
    total: number;
    pending: number;
    in_progress: number;
    completed: number;
  };
}
```

## Task States

Todos follow a predictable lifecycle with three states:

| State | Description | Display |
|-------|-------------|---------|
| `pending` | Task not yet started | Task is waiting to begin |
| `in_progress` | Currently working on | Task is actively being worked on |
| `completed` | Task finished successfully | Task has been completed |

### State Transitions

1. **Created** as `pending` when tasks are identified
2. **Activated** to `in_progress` when work begins
3. **Completed** when the task finishes successfully
4. **Removed** when all tasks in a group are completed

## Content vs ActiveForm

The TodoWrite tool requires two forms of each task description:

### content (Imperative Form)
The static description of what needs to be done:
- "Run tests"
- "Build the project"
- "Fix authentication bug"
- "Update documentation"

### activeForm (Present Continuous Form)
The dynamic description shown during execution:
- "Running tests"
- "Building the project"
- "Fixing authentication bug"
- "Updating documentation"

**Important:** Both forms are required for each task. The `activeForm` is displayed when the task status is `in_progress`, while `content` is used for `pending` and `completed` states.

## When Todos Are Used

The SDK automatically creates todos for:

- **Complex multi-step tasks** requiring 3 or more distinct actions
- **User-provided task lists** when multiple items are mentioned
- **Non-trivial operations** that benefit from progress tracking
- **Explicit requests** when users ask for todo organization

### When NOT to Use Todos

Skip using todos when:
- There is only a single, straightforward task
- The task is trivial and tracking it provides no organizational benefit
- The task can be completed in less than 3 trivial steps
- The task is purely conversational or informational

## Task Persistence

### In Interactive Mode
Todos persist throughout the conversation session and are displayed in the UI with real-time updates.

### In SDK Mode
Todos are included in the message stream and can be tracked by monitoring `tool_use` messages with `name === "TodoWrite"`.

### Storage
Todos are:
- **Session-scoped**: They exist for the duration of the conversation
- **Not persistent**: They do not persist across sessions or restarts
- **Real-time**: Updates are immediately reflected in the UI or message stream

## Best Practices

### Task Management

1. **Update task status in real-time** as you work
2. **Mark tasks complete IMMEDIATELY** after finishing (don't batch completions)
3. **Exactly ONE task must be in_progress** at any time (not less, not more)
4. **Complete current tasks before starting new ones**
5. **Remove tasks that are no longer relevant** from the list entirely

### Task Completion Requirements

**ONLY mark a task as completed when you have FULLY accomplished it.**

Never mark a task as completed if:
- Tests are failing
- Implementation is partial
- You encountered unresolved errors
- You couldn't find necessary files or dependencies

When blocked, keep the task as `in_progress` and create a new task describing what needs to be resolved.

### Task Breakdown

1. **Create specific, actionable items**
2. **Break complex tasks into smaller, manageable steps**
3. **Use clear, descriptive task names**
4. **Always provide both forms**:
   - `content`: "Fix authentication bug"
   - `activeForm`: "Fixing authentication bug"

## Usage Examples

### Monitoring Todo Changes (TypeScript)

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Optimize my React app performance and track progress with todos",
  options: { maxTurns: 15 }
})) {
  // Todo updates are reflected in the message stream
  if (message.type === "tool_use" && message.name === "TodoWrite") {
    const todos = message.input.todos;

    console.log("Todo Status Update:");
    todos.forEach((todo, index) => {
      const status = todo.status === "completed" ? "✅" :
                    todo.status === "in_progress" ? "🔧" : "❌";
      console.log(`${index + 1}. ${status} ${todo.content}`);
    });
  }
}
```

### Monitoring Todo Changes (Python)

```python
from claude_agent_sdk import query

async for message in query(
    prompt="Optimize my React app performance and track progress with todos",
    options={"max_turns": 15}
):
    # Todo updates are reflected in the message stream
    if message.get("type") == "tool_use" and message.get("name") == "TodoWrite":
        todos = message["input"]["todos"]

        print("Todo Status Update:")
        for i, todo in enumerate(todos):
            status = "✅" if todo["status"] == "completed" else \
                    "🔧" if todo["status"] == "in_progress" else "❌"
            print(f"{i + 1}. {status} {todo['content']}")
```

### Real-time Progress Display (TypeScript)

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

class TodoTracker {
  private todos: any[] = [];

  displayProgress() {
    if (this.todos.length === 0) return;

    const completed = this.todos.filter(t => t.status === "completed").length;
    const inProgress = this.todos.filter(t => t.status === "in_progress").length;
    const total = this.todos.length;

    console.log(`\nProgress: ${completed}/${total} completed`);
    console.log(`Currently working on: ${inProgress} task(s)\n`);

    this.todos.forEach((todo, index) => {
      const icon = todo.status === "completed" ? "✅" :
                  todo.status === "in_progress" ? "🔧" : "❌";
      const text = todo.status === "in_progress" ? todo.activeForm : todo.content;
      console.log(`${index + 1}. ${icon} ${text}`);
    });
  }

  async trackQuery(prompt: string) {
    for await (const message of query({
      prompt,
      options: { maxTurns: 20 }
    })) {
      if (message.type === "tool_use" && message.name === "TodoWrite") {
        this.todos = message.input.todos;
        this.displayProgress();
      }
    }
  }
}

// Usage
const tracker = new TodoTracker();
await tracker.trackQuery("Build a complete authentication system with todos");
```

### Real-time Progress Display (Python)

```python
from claude_agent_sdk import query
from typing import List, Dict

class TodoTracker:
    def __init__(self):
        self.todos: List[Dict] = []

    def display_progress(self):
        if not self.todos:
            return

        completed = len([t for t in self.todos if t["status"] == "completed"])
        in_progress = len([t for t in self.todos if t["status"] == "in_progress"])
        total = len(self.todos)

        print(f"\nProgress: {completed}/{total} completed")
        print(f"Currently working on: {in_progress} task(s)\n")

        for i, todo in enumerate(self.todos):
            icon = "✅" if todo["status"] == "completed" else \
                  "🔧" if todo["status"] == "in_progress" else "❌"
            text = todo["activeForm"] if todo["status"] == "in_progress" else todo["content"]
            print(f"{i + 1}. {icon} {text}")

    async def track_query(self, prompt: str):
        async for message in query(
            prompt=prompt,
            options={"max_turns": 20}
        ):
            if message.get("type") == "tool_use" and message.get("name") == "TodoWrite":
                self.todos = message["input"]["todos"]
                self.display_progress()

# Usage
tracker = TodoTracker()
await tracker.track_query("Build a complete authentication system with todos")
```

## Practical Usage Patterns

### Pattern 1: Multi-Step Implementation

```typescript
// When user requests a complex feature
const todos = [
  {
    content: "Create database schema",
    activeForm: "Creating database schema",
    status: "in_progress"
  },
  {
    content: "Implement API endpoints",
    activeForm: "Implementing API endpoints",
    status: "pending"
  },
  {
    content: "Add authentication middleware",
    activeForm: "Adding authentication middleware",
    status: "pending"
  },
  {
    content: "Write integration tests",
    activeForm: "Writing integration tests",
    status: "pending"
  },
  {
    content: "Update documentation",
    activeForm: "Updating documentation",
    status: "pending"
  }
];
```

### Pattern 2: Bug Investigation

```typescript
const todos = [
  {
    content: "Reproduce the bug",
    activeForm: "Reproducing the bug",
    status: "in_progress"
  },
  {
    content: "Analyze error logs",
    activeForm: "Analyzing error logs",
    status: "pending"
  },
  {
    content: "Identify root cause",
    activeForm: "Identifying root cause",
    status: "pending"
  },
  {
    content: "Implement fix",
    activeForm: "Implementing fix",
    status: "pending"
  },
  {
    content: "Verify fix with tests",
    activeForm: "Verifying fix with tests",
    status: "pending"
  }
];
```

### Pattern 3: Code Review Workflow

```typescript
const todos = [
  {
    content: "Review code changes",
    activeForm: "Reviewing code changes",
    status: "in_progress"
  },
  {
    content: "Check for security issues",
    activeForm: "Checking for security issues",
    status: "pending"
  },
  {
    content: "Verify test coverage",
    activeForm: "Verifying test coverage",
    status: "pending"
  },
  {
    content: "Run linter and formatter",
    activeForm: "Running linter and formatter",
    status: "pending"
  },
  {
    content: "Document findings",
    activeForm: "Documenting findings",
    status: "pending"
  }
];
```

## Integration with Claude Code

### In Interactive Mode

When using Claude Code interactively, todos are automatically displayed in the terminal UI with visual indicators:

- ❌ Pending tasks
- 🔧 Tasks in progress
- ✅ Completed tasks

### In Headless Mode

When using Claude Code with the `-p` flag (print mode), todos are included in the output stream and can be parsed from the tool use messages.

### Permission Requirements

The TodoWrite tool does **not** require user permission, as it only manages display state and doesn't modify files or execute commands.

## Common Patterns

### Starting a Todo List

```typescript
// First call to TodoWrite
{
  todos: [
    {
      content: "Task 1",
      activeForm: "Doing Task 1",
      status: "in_progress"
    },
    {
      content: "Task 2",
      activeForm: "Doing Task 2",
      status: "pending"
    }
  ]
}
```

### Progressing Through Tasks

```typescript
// Task 1 completed, Task 2 now in progress
{
  todos: [
    {
      content: "Task 1",
      activeForm: "Doing Task 1",
      status: "completed"
    },
    {
      content: "Task 2",
      activeForm: "Doing Task 2",
      status: "in_progress"
    }
  ]
}
```

### Adding New Tasks Mid-Workflow

```typescript
// Discovered additional work needed
{
  todos: [
    {
      content: "Task 1",
      activeForm: "Doing Task 1",
      status: "completed"
    },
    {
      content: "Task 2",
      activeForm: "Doing Task 2",
      status: "completed"
    },
    {
      content: "Fix discovered issue",
      activeForm: "Fixing discovered issue",
      status: "in_progress"
    },
    {
      content: "Task 3",
      activeForm: "Doing Task 3",
      status: "pending"
    }
  ]
}
```

## Error Handling

### When Tasks Fail

If a task encounters an error:

1. Keep the task as `in_progress`
2. Create a new task describing the blocker
3. Do not mark as completed

```typescript
{
  todos: [
    {
      content: "Run integration tests",
      activeForm: "Running integration tests",
      status: "in_progress"  // Tests failed, not completed!
    },
    {
      content: "Fix failing test cases",
      activeForm: "Fixing failing test cases",
      status: "pending"  // New task to address the failure
    }
  ]
}
```

### Removing Obsolete Tasks

If a task becomes irrelevant, simply remove it from the array rather than marking it completed:

```typescript
// Before: Task 2 is no longer needed
{
  todos: [
    { content: "Task 1", activeForm: "...", status: "completed" },
    { content: "Task 2", activeForm: "...", status: "pending" },
    { content: "Task 3", activeForm: "...", status: "in_progress" }
  ]
}

// After: Task 2 removed entirely
{
  todos: [
    { content: "Task 1", activeForm: "...", status: "completed" },
    { content: "Task 3", activeForm: "...", status: "in_progress" }
  ]
}
```

## System Prompt Guidelines

The TodoWrite tool is governed by specific instructions in Claude Code's system prompt:

### When to Use

Use the TodoWrite tool proactively in these scenarios:

1. **Complex multi-step tasks** - When a task requires 3 or more distinct steps or actions
2. **Non-trivial and complex tasks** - Tasks that require careful planning or multiple operations
3. **User explicitly requests todo list** - When the user directly asks to use the todo list
4. **User provides multiple tasks** - When users provide a list of things to be done (numbered or comma-separated)

### State Management

- **Exactly ONE task** must be `in_progress` at any time
- Mark tasks `completed` immediately after finishing
- Complete current tasks before starting new ones
- Remove tasks that are no longer relevant from the list entirely

### Task Descriptions

Always provide both forms:
- `content`: Imperative form ("Run tests")
- `activeForm`: Present continuous form ("Running tests")

## Related Documentation

- [TypeScript SDK Reference](/en/api/agent-sdk/typescript)
- [Python SDK Reference](/en/api/agent-sdk/python)
- [Streaming vs Single Mode](/en/api/agent-sdk/streaming-vs-single-mode)
- [Custom Tools](/en/api/agent-sdk/custom-tools)
- [Settings](/en/docs/claude-code/settings)
