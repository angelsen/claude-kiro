# Claude Code CLI and Agent SDK - Complete Guide

> Comprehensive documentation on CLI usage patterns, Agent SDK for TypeScript and Python, and automation workflows for building tools on top of Claude Code.

**Source:** Local documentation from `/home/fredrik/Projects/Python/project-autumn-25/claude-kiro/resources/scraped/docs.claude.com/`

---

## Table of Contents

1. [CLI Usage Patterns](#cli-usage-patterns)
2. [Headless Mode & Automation](#headless-mode--automation)
3. [Agent SDK Overview](#agent-sdk-overview)
4. [TypeScript SDK](#typescript-sdk)
5. [Python SDK](#python-sdk)
6. [Custom Tools & MCP Integration](#custom-tools--mcp-integration)
7. [CI/CD Integration](#cicd-integration)
8. [Session Management](#session-management)
9. [Building Tools on Claude Code](#building-tools-on-claude-code)
10. [Best Practices](#best-practices)

---

## CLI Usage Patterns

### Basic CLI Commands

| Command | Description | Example |
|---------|-------------|---------|
| `claude` | Start interactive REPL | `claude` |
| `claude "query"` | Start REPL with initial prompt | `claude "explain this project"` |
| `claude -p "query"` | Query via SDK, then exit (print mode) | `claude -p "explain this function"` |
| `cat file \| claude -p "query"` | Process piped content | `cat logs.txt \| claude -p "explain"` |
| `claude -c` | Continue most recent conversation | `claude -c` |
| `claude -c -p "query"` | Continue via SDK | `claude -c -p "Check for type errors"` |
| `claude -r "<session-id>" "query"` | Resume session by ID | `claude -r "abc123" "Finish this PR"` |
| `claude update` | Update to latest version | `claude update` |

### Essential CLI Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--print`, `-p` | Print response without interactive mode | `claude -p "query"` |
| `--output-format` | Specify output format: `text`, `json`, `stream-json` | `claude -p "query" --output-format json` |
| `--input-format` | Specify input format: `text`, `stream-json` | `claude -p --input-format stream-json` |
| `--include-partial-messages` | Include partial streaming events | `claude -p --output-format stream-json --include-partial-messages "query"` |
| `--verbose` | Enable verbose logging | `claude --verbose` |
| `--max-turns` | Limit agentic turns in non-interactive mode | `claude -p --max-turns 3 "query"` |
| `--model` | Set model (alias or full name) | `claude --model claude-sonnet-4-5-20250929` |
| `--permission-mode` | Begin in specified permission mode | `claude --permission-mode plan` |
| `--resume`, `-r` | Resume a specific session by ID | `claude --resume abc123 "query"` |
| `--continue`, `-c` | Load most recent conversation | `claude --continue` |
| `--add-dir` | Add additional working directories | `claude --add-dir ../apps ../lib` |
| `--allowedTools` | List of tools allowed without prompting | `claude --allowedTools "Bash(git log:*)" "Read"` |
| `--disallowedTools` | List of tools to disallow | `claude --disallowedTools "Bash(rm:*)" "Edit"` |
| `--append-system-prompt` | Append to system prompt (only with `--print`) | `claude -p "query" --append-system-prompt "Custom instruction"` |
| `--agents` | Define custom subagents dynamically via JSON | `claude --agents '{"reviewer":{"description":"Reviews code","prompt":"You are a code reviewer"}}'` |

### Agents Flag Format

Define custom subagents with JSON:

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "debugger": {
    "description": "Debugging specialist for errors and test failures.",
    "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
  }
}'
```

---

## Headless Mode & Automation

Headless mode allows running Claude Code programmatically without interactive UI, perfect for scripts and automation.

### Basic Headless Usage

```bash
# Run non-interactive query
claude -p "Stage my changes and write a set of commits for them" \
  --allowedTools "Bash,Read" \
  --permission-mode acceptEdits
```

### Output Formats

#### Text Output (Default)

```bash
claude -p "Explain file src/components/Header.tsx"
# Output: Plain text response
```

#### JSON Output

Returns structured data with metadata:

```bash
claude -p "How does the data layer work?" --output-format json
```

Response format:
```json
{
  "type": "result",
  "subtype": "success",
  "total_cost_usd": 0.003,
  "is_error": false,
  "duration_ms": 1234,
  "duration_api_ms": 800,
  "num_turns": 6,
  "result": "The response text here...",
  "session_id": "abc123"
}
```

#### Streaming JSON Output

Streams each message as it's received:

```bash
claude -p "Build an application" --output-format stream-json
```

Each message is emitted as a separate JSON object (JSONL format).

### Multi-turn Conversations

```bash
# Continue most recent conversation
claude --continue "Now refactor this for better performance"

# Resume specific conversation
claude --resume 550e8400-e29b-41d4-a716-446655440000 "Update the tests"

# Resume in non-interactive mode
claude --resume 550e8400-e29b-41d4-a716-446655440000 "Fix all linting issues" --print
```

### Automation Examples

#### SRE Incident Response Bot

```bash
#!/bin/bash

investigate_incident() {
    local incident_description="$1"
    local severity="${2:-medium}"

    claude -p "Incident: $incident_description (Severity: $severity)" \
      --append-system-prompt "You are an SRE expert. Diagnose the issue, assess impact, and provide immediate action items." \
      --output-format json \
      --allowedTools "Bash,Read,WebSearch,mcp__datadog" \
      --mcp-config monitoring-tools.json
}

investigate_incident "Payment API returning 500 errors" "high"
```

#### Automated Security Review

```bash
# Security audit for pull requests
audit_pr() {
    local pr_number="$1"

    gh pr diff "$pr_number" | claude -p \
      --append-system-prompt "You are a security engineer. Review this PR for vulnerabilities, insecure patterns, and compliance issues." \
      --output-format json \
      --allowedTools "Read,Grep,WebSearch"
}

audit_pr 123 > security-report.json
```

#### Multi-turn Legal Assistant

```bash
# Legal document review with session persistence
session_id=$(claude -p "Start legal review session" --output-format json | jq -r '.session_id')

# Review contract in multiple steps
claude -p --resume "$session_id" "Review contract.pdf for liability clauses"
claude -p --resume "$session_id" "Check compliance with GDPR requirements"
claude -p --resume "$session_id" "Generate executive summary of risks"
```

### Best Practices for Headless Mode

1. **Use JSON output format** for programmatic parsing:
   ```bash
   result=$(claude -p "Generate code" --output-format json)
   code=$(echo "$result" | jq -r '.result')
   cost=$(echo "$result" | jq -r '.cost_usd')
   ```

2. **Handle errors gracefully**:
   ```bash
   if ! claude -p "$prompt" 2>error.log; then
       echo "Error occurred:" >&2
       cat error.log >&2
       exit 1
   fi
   ```

3. **Use session management** for multi-turn conversations

4. **Consider timeouts** for long-running operations:
   ```bash
   timeout 300 claude -p "$complex_prompt" || echo "Timed out after 5 minutes"
   ```

5. **Respect rate limits** by adding delays between calls

---

## Agent SDK Overview

The Claude Agent SDK enables programmatic integration of Claude Code into applications, built on the same agent harness that powers Claude Code.

### Installation

**TypeScript:**
```bash
npm install @anthropic-ai/claude-agent-sdk
```

**Python:**
```bash
pip install claude-agent-sdk
```

### Why Use the Agent SDK?

- **Context Management**: Automatic compaction and context management
- **Rich tool ecosystem**: File operations, code execution, web search, MCP extensibility
- **Advanced permissions**: Fine-grained control over agent capabilities
- **Production essentials**: Built-in error handling, session management, monitoring
- **Optimized integration**: Automatic prompt caching and performance optimizations

### Key Features

All Claude Code features available programmatically:

- **Subagents**: Launch specialized agents from `./.claude/agents/`
- **Hooks**: Execute custom commands from `./.claude/settings.json`
- **Slash Commands**: Custom commands from `./.claude/commands/`
- **Memory (CLAUDE.md)**: Project context from `CLAUDE.md` files
- **Settings Sources**: Control which filesystem settings to load

### Authentication

Set `ANTHROPIC_API_KEY` environment variable, or use:

- **Amazon Bedrock**: Set `CLAUDE_CODE_USE_BEDROCK=1` + AWS credentials
- **Google Vertex AI**: Set `CLAUDE_CODE_USE_VERTEX=1` + GCP credentials

---

## TypeScript SDK

### Basic Usage

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

// Simple query
for await (const message of query({
  prompt: "Explain this codebase",
  options: {
    cwd: "/path/to/project",
    allowedTools: ["Read", "Grep", "Glob"]
  }
})) {
  console.log(message);
}
```

### Key Types

#### `Options` Interface

```typescript
{
  // Core options
  cwd: string;                              // Working directory
  model: string;                            // Claude model to use
  systemPrompt: string | SystemPromptPreset; // System prompt config

  // Tool configuration
  allowedTools: string[];                   // Allowed tool names
  disallowedTools: string[];               // Disallowed tool names
  canUseTool: CanUseTool;                  // Custom permission function

  // Session management
  continue: boolean;                        // Continue most recent conversation
  resume: string;                          // Session ID to resume
  forkSession: boolean;                    // Fork when resuming

  // MCP configuration
  mcpServers: Record<string, McpServerConfig>;

  // Advanced options
  permissionMode: PermissionMode;          // Permission strategy
  maxTurns: number;                        // Max conversation turns
  settingSources: SettingSource[];         // Filesystem settings to load
  agents: Record<string, AgentDefinition>; // Programmatic subagents
  hooks: Record<HookEvent, HookCallbackMatcher[]>; // Event hooks
}
```

#### System Prompt Configuration

```typescript
// Custom prompt
const options = {
  systemPrompt: "You are a senior Python developer"
};

// Use Claude Code's preset prompt
const options = {
  systemPrompt: {
    type: "preset",
    preset: "claude_code"
  }
};

// Extend preset prompt
const options = {
  systemPrompt: {
    type: "preset",
    preset: "claude_code",
    append: "Focus on security best practices"
  }
};
```

#### Setting Sources

```typescript
// Load all settings (legacy behavior)
settingSources: ['user', 'project', 'local']

// Load only project settings (recommended for CI)
settingSources: ['project']

// No filesystem settings (default)
settingSources: []

// Load CLAUDE.md files (requires 'project' source)
settingSources: ['project'],
systemPrompt: { type: 'preset', preset: 'claude_code' }
```

### Permission Modes

```typescript
type PermissionMode =
  | 'default'           // Standard permission behavior
  | 'acceptEdits'       // Auto-accept file edits
  | 'bypassPermissions' // Bypass all permission checks
  | 'plan';             // Planning mode - no execution
```

### Custom Permission Handler

```typescript
import { query, CanUseTool } from "@anthropic-ai/claude-agent-sdk";

const customPermissionHandler: CanUseTool = async (toolName, input, { signal }) => {
  // Block dangerous operations
  if (toolName === "Bash" && input.command.includes("rm -rf")) {
    return {
      behavior: "deny",
      message: "Dangerous command blocked",
      interrupt: true
    };
  }

  // Redirect sensitive operations
  if (toolName === "Write" && input.file_path.includes("/etc/")) {
    return {
      behavior: "allow",
      updatedInput: {
        ...input,
        file_path: `/sandbox${input.file_path}`
      }
    };
  }

  // Allow by default
  return {
    behavior: "allow",
    updatedInput: input
  };
};

// Use in query
for await (const message of query({
  prompt: "Update system config",
  options: {
    canUseTool: customPermissionHandler
  }
})) {
  console.log(message);
}
```

### Subagents Configuration

```typescript
import { query, AgentDefinition } from "@anthropic-ai/claude-agent-sdk";

const agents: Record<string, AgentDefinition> = {
  "code-reviewer": {
    description: "Expert code reviewer. Use after code changes.",
    prompt: "You are a senior code reviewer. Focus on quality and security.",
    tools: ["Read", "Grep", "Glob", "Bash"],
    model: "sonnet"
  },
  "test-engineer": {
    description: "Test specialist. Use for testing tasks.",
    prompt: "You are a test engineer. Write comprehensive tests.",
    tools: ["Read", "Write", "Bash"],
    model: "haiku"
  }
};

for await (const message of query({
  prompt: "Review and test this code",
  options: { agents }
})) {
  console.log(message);
}
```

### Streaming Mode

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

// Create async generator for streaming input
async function* generateMessages() {
  yield {
    type: "user" as const,
    message: {
      role: "user" as const,
      content: "Analyze the auth module"
    }
  };

  // Can add more messages dynamically
  await someAsyncOperation();

  yield {
    type: "user" as const,
    message: {
      role: "user" as const,
      content: "Now check for security issues"
    }
  };
}

const queryInstance = query({
  prompt: generateMessages(),
  options: {
    allowedTools: ["Read", "Grep"]
  }
});

// Can interrupt streaming queries
setTimeout(() => {
  queryInstance.interrupt();
}, 5000);

for await (const message of queryInstance) {
  console.log(message);
}
```

---

## Python SDK

### Basic Usage - `query()` Function

Use `query()` for **one-off tasks** where you don't need conversation history:

```python
from claude_agent_sdk import query, ClaudeAgentOptions
import asyncio

async def main():
    options = ClaudeAgentOptions(
        system_prompt="You are an expert Python developer",
        permission_mode='acceptEdits',
        cwd="/home/user/project"
    )

    async for message in query(
        prompt="Create a Python web server",
        options=options
    ):
        print(message)

asyncio.run(main())
```

### Advanced Usage - `ClaudeSDKClient` Class

Use `ClaudeSDKClient` for **continuous conversations** where context matters:

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage, TextBlock
import asyncio

async def main():
    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Write", "Bash"],
        permission_mode="acceptEdits"
    )

    async with ClaudeSDKClient(options=options) as client:
        # First question
        await client.query("What's the capital of France?")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")

        # Follow-up - Claude remembers previous context!
        await client.query("What's the population of that city?")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")

asyncio.run(main())
```

### Comparison: `query()` vs `ClaudeSDKClient`

| Feature | `query()` | `ClaudeSDKClient` |
|---------|-----------|-------------------|
| **Session** | Creates new each time | Reuses same session |
| **Conversation** | Single exchange | Multiple exchanges in context |
| **Interrupts** | Not supported | Supported |
| **Hooks** | Not supported | Supported |
| **Custom Tools** | Not supported | Supported |
| **Continue Chat** | New session each time | Maintains conversation |
| **Use Case** | One-off tasks | Continuous conversations |

### Key Options - `ClaudeAgentOptions`

```python
from claude_agent_sdk import ClaudeAgentOptions

options = ClaudeAgentOptions(
    # Core settings
    cwd="/path/to/project",
    model="claude-sonnet-4-5-20250929",
    system_prompt="You are an expert developer",

    # Tool configuration
    allowed_tools=["Read", "Write", "Bash"],
    disallowed_tools=["WebSearch"],

    # Permission control
    permission_mode="acceptEdits",  # or "default", "plan", "bypassPermissions"
    can_use_tool=custom_permission_handler,

    # Session management
    continue_conversation=False,
    resume="session-id",
    fork_session=False,

    # MCP servers
    mcp_servers={"server_name": server_config},

    # Advanced
    max_turns=10,
    agents={"agent_name": agent_definition},
    hooks={"PreToolUse": [hook_matchers]},
    setting_sources=["project"],  # None by default
    include_partial_messages=False
)
```

### System Prompt Configuration

```python
from claude_agent_sdk import ClaudeAgentOptions

# Custom prompt
options = ClaudeAgentOptions(
    system_prompt="You are a senior Python developer"
)

# Use Claude Code's preset
options = ClaudeAgentOptions(
    system_prompt={
        "type": "preset",
        "preset": "claude_code"
    }
)

# Extend preset
options = ClaudeAgentOptions(
    system_prompt={
        "type": "preset",
        "preset": "claude_code",
        "append": "Focus on security"
    }
)
```

### Custom Permission Handler

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
import asyncio

async def custom_permission_handler(
    tool_name: str,
    input_data: dict,
    context: dict
):
    # Block dangerous operations
    if tool_name == "Bash" and "rm -rf" in input_data.get("command", ""):
        return {
            "behavior": "deny",
            "message": "Dangerous command blocked",
            "interrupt": True
        }

    # Redirect sensitive file operations
    if tool_name in ["Write", "Edit"] and "config" in input_data.get("file_path", ""):
        safe_path = f"./sandbox/{input_data['file_path']}"
        return {
            "behavior": "allow",
            "updatedInput": {**input_data, "file_path": safe_path}
        }

    # Allow by default
    return {
        "behavior": "allow",
        "updatedInput": input_data
    }

async def main():
    options = ClaudeAgentOptions(
        can_use_tool=custom_permission_handler,
        allowed_tools=["Read", "Write", "Edit"]
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query("Update the system config file")
        async for message in client.receive_response():
            print(message)

asyncio.run(main())
```

### Hooks for Behavior Modification

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, HookMatcher, HookContext
from typing import Any
import asyncio

async def pre_tool_logger(
    input_data: dict[str, Any],
    tool_use_id: str | None,
    context: HookContext
) -> dict[str, Any]:
    """Log and validate tool usage before execution."""
    tool_name = input_data.get('tool_name', 'unknown')
    print(f"[PRE-TOOL] About to use: {tool_name}")

    # Block dangerous commands
    if tool_name == "Bash" and "rm -rf" in str(input_data.get('tool_input', {})):
        return {
            'hookSpecificOutput': {
                'hookEventName': 'PreToolUse',
                'permissionDecision': 'deny',
                'permissionDecisionReason': 'Dangerous command blocked'
            }
        }
    return {}

async def post_tool_logger(
    input_data: dict[str, Any],
    tool_use_id: str | None,
    context: HookContext
) -> dict[str, Any]:
    """Log results after tool execution."""
    tool_name = input_data.get('tool_name', 'unknown')
    print(f"[POST-TOOL] Completed: {tool_name}")
    return {}

async def main():
    options = ClaudeAgentOptions(
        hooks={
            'PreToolUse': [
                HookMatcher(matcher='Bash', hooks=[pre_tool_logger]),
                HookMatcher(hooks=[pre_tool_logger])  # All tools
            ],
            'PostToolUse': [
                HookMatcher(hooks=[post_tool_logger])
            ]
        },
        allowed_tools=["Read", "Write", "Bash"]
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query("List files in current directory")
        async for message in client.receive_response():
            pass

asyncio.run(main())
```

### Interrupts with `ClaudeSDKClient`

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
import asyncio

async def interruptible_task():
    options = ClaudeAgentOptions(
        allowed_tools=["Bash"],
        permission_mode="acceptEdits"
    )

    async with ClaudeSDKClient(options=options) as client:
        # Start a long-running task
        await client.query("Count from 1 to 100 slowly")

        # Let it run for a bit
        await asyncio.sleep(2)

        # Interrupt the task
        await client.interrupt()
        print("Task interrupted!")

        # Send a new command
        await client.query("Just say hello instead")

        async for message in client.receive_response():
            pass

asyncio.run(interruptible_task())
```

### Error Handling

```python
from claude_agent_sdk import (
    query,
    CLINotFoundError,
    ProcessError,
    CLIJSONDecodeError
)
import asyncio

async def main():
    try:
        async for message in query(prompt="Hello"):
            print(message)
    except CLINotFoundError:
        print("Please install: npm install -g @anthropic-ai/claude-code")
    except ProcessError as e:
        print(f"Process failed with exit code: {e.exit_code}")
    except CLIJSONDecodeError as e:
        print(f"Failed to parse response: {e}")

asyncio.run(main())
```

---

## Custom Tools & MCP Integration

Custom tools extend Claude's capabilities through in-process MCP servers.

### TypeScript - Creating Custom Tools

```typescript
import { query, tool, createSdkMcpServer } from "@anthropic-ai/claude-agent-sdk";
import { z } from "zod";

// Define a custom tool
const weatherTool = tool(
  "get_weather",
  "Get current weather for a location",
  {
    location: z.string().describe("City name or coordinates"),
    units: z.enum(["celsius", "fahrenheit"]).default("celsius")
  },
  async (args) => {
    const response = await fetch(
      `https://api.weather.com/v1/current?q=${args.location}&units=${args.units}`
    );
    const data = await response.json();

    return {
      content: [{
        type: "text",
        text: `Temperature: ${data.temp}°\nConditions: ${data.conditions}`
      }]
    };
  }
);

// Create MCP server
const customServer = createSdkMcpServer({
  name: "weather-tools",
  version: "1.0.0",
  tools: [weatherTool]
});

// Use with streaming input (REQUIRED for custom tools)
async function* generateMessages() {
  yield {
    type: "user" as const,
    message: {
      role: "user" as const,
      content: "What's the weather in San Francisco?"
    }
  };
}

for await (const message of query({
  prompt: generateMessages(),  // Must use async generator!
  options: {
    mcpServers: {
      "weather": customServer
    },
    allowedTools: [
      "mcp__weather__get_weather"  // Format: mcp__{server}__{tool}
    ]
  }
})) {
  console.log(message);
}
```

### Python - Creating Custom Tools

```python
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    tool,
    create_sdk_mcp_server
)
from typing import Any
import aiohttp
import asyncio

# Define custom tool with @tool decorator
@tool("get_weather", "Get current weather for a location", {"location": str, "units": str})
async def get_weather(args: dict[str, Any]) -> dict[str, Any]:
    units = args.get('units', 'celsius')
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://api.weather.com/v1/current?q={args['location']}&units={units}"
        ) as response:
            data = await response.json()

    return {
        "content": [{
            "type": "text",
            "text": f"Temperature: {data['temp']}°\nConditions: {data['conditions']}"
        }]
    }

# Create SDK MCP server
custom_server = create_sdk_mcp_server(
    name="weather-tools",
    version="1.0.0",
    tools=[get_weather]
)

# Use with ClaudeSDKClient
async def main():
    options = ClaudeAgentOptions(
        mcp_servers={"weather": custom_server},
        allowed_tools=["mcp__weather__get_weather"]
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query("What's the weather in San Francisco?")
        async for msg in client.receive_response():
            print(msg)

asyncio.run(main())
```

### Multiple Tools Example

```typescript
const multiToolServer = createSdkMcpServer({
  name: "utilities",
  version: "1.0.0",
  tools: [
    tool("calculate", "Perform calculations", { expression: z.string() }, async (args) => {
      const result = eval(args.expression);
      return { content: [{ type: "text", text: `Result: ${result}` }] };
    }),
    tool("translate", "Translate text", {
      text: z.string(),
      target: z.string()
    }, async (args) => {
      // Translation logic
      return { content: [{ type: "text", text: "Translated text" }] };
    })
  ]
});

// Allow specific tools
async function* generateMessages() {
  yield {
    type: "user" as const,
    message: {
      role: "user" as const,
      content: "Calculate 5 + 3 and translate 'hello' to Spanish"
    }
  };
}

for await (const message of query({
  prompt: generateMessages(),
  options: {
    mcpServers: { utilities: multiToolServer },
    allowedTools: [
      "mcp__utilities__calculate",
      "mcp__utilities__translate"
      // Other tools not allowed
    ]
  }
})) {
  console.log(message);
}
```

### Tool Name Format

MCP tools follow this naming pattern:
- **Pattern**: `mcp__{server_name}__{tool_name}`
- **Example**: `get_weather` in server `weather-tools` becomes `mcp__weather-tools__get_weather`

### Error Handling in Tools

```typescript
tool(
  "fetch_data",
  "Fetch data from API",
  { endpoint: z.string().url() },
  async (args) => {
    try {
      const response = await fetch(args.endpoint);

      if (!response.ok) {
        return {
          content: [{
            type: "text",
            text: `API error: ${response.status} ${response.statusText}`
          }],
          isError: true
        };
      }

      const data = await response.json();
      return {
        content: [{
          type: "text",
          text: JSON.stringify(data, null, 2)
        }]
      };
    } catch (error) {
      return {
        content: [{
          type: "text",
          text: `Failed to fetch: ${error.message}`
        }],
        isError: true
      };
    }
  }
)
```

---

## CI/CD Integration

### GitHub Actions

#### Basic Workflow

```yaml
name: Claude Code
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]

jobs:
  claude:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          # Responds to @claude mentions in comments
```

#### Using Slash Commands

```yaml
name: Code Review
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "/review"
          claude_args: "--max-turns 5"
```

#### Custom Automation

```yaml
name: Daily Report
on:
  schedule:
    - cron: "0 9 * * *"

jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Generate a summary of yesterday's commits and open issues"
          claude_args: "--model claude-opus-4-1-20250805"
```

#### AWS Bedrock Integration

```yaml
name: Claude PR Action

permissions:
  contents: write
  pull-requests: write
  issues: write
  id-token: write

on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]

jobs:
  claude-pr:
    if: contains(github.event.comment.body, '@claude')
    runs-on: ubuntu-latest
    env:
      AWS_REGION: us-west-2
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Generate GitHub App token
        id: app-token
        uses: actions/create-github-app-token@v2
        with:
          app-id: ${{ secrets.APP_ID }}
          private-key: ${{ secrets.APP_PRIVATE_KEY }}

      - name: Configure AWS Credentials (OIDC)
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_TO_ASSUME }}
          aws-region: us-west-2

      - uses: anthropics/claude-code-action@v1
        with:
          github_token: ${{ steps.app-token.outputs.token }}
          use_bedrock: "true"
          claude_args: '--model us.anthropic.claude-sonnet-4-5-20250929-v1:0 --max-turns 10'
```

#### Google Vertex AI Integration

```yaml
name: Claude PR Action

permissions:
  contents: write
  pull-requests: write
  issues: write
  id-token: write

on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]

jobs:
  claude-pr:
    if: contains(github.event.comment.body, '@claude')
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Generate GitHub App token
        id: app-token
        uses: actions/create-github-app-token@v2
        with:
          app-id: ${{ secrets.APP_ID }}
          private-key: ${{ secrets.APP_PRIVATE_KEY }}

      - name: Authenticate to Google Cloud
        id: auth
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.GCP_WORKLOAD_IDENTITY_PROVIDER }}
          service_account: ${{ secrets.GCP_SERVICE_ACCOUNT }}

      - uses: anthropics/claude-code-action@v1
        with:
          github_token: ${{ steps.app-token.outputs.token }}
          trigger_phrase: "@claude"
          use_vertex: "true"
          claude_args: '--model claude-sonnet-4@20250514 --max-turns 10'
        env:
          ANTHROPIC_VERTEX_PROJECT_ID: ${{ steps.auth.outputs.project_id }}
          CLOUD_ML_REGION: us-east5
          VERTEX_REGION_CLAUDE_3_7_SONNET: us-east5
```

### GitLab CI/CD

```yaml
claude_review:
  stage: review
  image: node:18
  before_script:
    - npm install -g @anthropic-ai/claude-code
  script:
    - |
      claude -p "Review this merge request for security issues" \
        --output-format json \
        --allowedTools "Read,Grep,Glob" \
        --max-turns 5 > review.json
  artifacts:
    reports:
      codequality: review.json
  only:
    - merge_requests
```

---

## Session Management

Sessions allow continuing conversations while maintaining full context.

### Getting Session ID

**TypeScript:**
```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

let sessionId: string | undefined;

for await (const message of query({
  prompt: "Help me build a web app",
  options: { model: "claude-sonnet-4-5" }
})) {
  if (message.type === 'system' && message.subtype === 'init') {
    sessionId = message.session_id;
    console.log(`Session: ${sessionId}`);
  }
}

// Resume later
if (sessionId) {
  const resumed = query({
    prompt: "Continue where we left off",
    options: { resume: sessionId }
  });
}
```

**Python:**
```python
from claude_agent_sdk import query, ClaudeAgentOptions

session_id = None

async for message in query(
    prompt="Help me build a web app",
    options=ClaudeAgentOptions(model="claude-sonnet-4-5")
):
    if hasattr(message, 'subtype') and message.subtype == 'init':
        session_id = message.data.get('session_id')
        print(f"Session: {session_id}")

# Resume later
if session_id:
    async for message in query(
        prompt="Continue where we left off",
        options=ClaudeAgentOptions(resume=session_id)
    ):
        print(message)
```

### Forking Sessions

Create branching conversations without modifying original:

**TypeScript:**
```typescript
// Fork to try different approach
const forked = query({
  prompt: "Now let's try GraphQL instead",
  options: {
    resume: sessionId,
    forkSession: true  // Creates new session ID
  }
});

// Original session unchanged
const continued = query({
  prompt: "Add auth to REST API",
  options: {
    resume: sessionId,
    forkSession: false  // Continue original (default)
  }
});
```

**Python:**
```python
# Fork to try different approach
async for message in query(
    prompt="Now let's try GraphQL instead",
    options=ClaudeAgentOptions(
        resume=session_id,
        fork_session=True  # Creates new session ID
    )
):
    print(message)

# Original session unchanged
async for message in query(
    prompt="Add auth to REST API",
    options=ClaudeAgentOptions(
        resume=session_id,
        fork_session=False  # Continue original (default)
    )
):
    print(message)
```

### Session Forking Use Cases

- Explore different approaches from same starting point
- Create conversation branches without modifying original
- Test changes without affecting original session
- Maintain separate paths for experiments

---

## Building Tools on Claude Code

### Example: Code Review Automation Tool

**TypeScript:**
```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";
import { readFileSync } from "fs";

async function reviewPullRequest(prNumber: string) {
  // Get PR diff
  const diff = execSync(`gh pr diff ${prNumber}`).toString();

  // Create review prompt
  const prompt = `
    Review this pull request for:
    - Code quality and best practices
    - Security vulnerabilities
    - Performance issues
    - Test coverage

    ${diff}
  `;

  let review = "";

  for await (const message of query({
    prompt,
    options: {
      systemPrompt: "You are a senior code reviewer",
      allowedTools: ["Read", "Grep"],
      maxTurns: 5,
      outputFormat: "json"
    }
  })) {
    if (message.type === "result" && message.subtype === "success") {
      review = message.result;
    }
  }

  // Post review as comment
  execSync(`gh pr comment ${prNumber} --body "${review}"`);

  return review;
}

// Usage
reviewPullRequest("123");
```

**Python:**
```python
from claude_agent_sdk import query, ClaudeAgentOptions
import subprocess
import asyncio

async def review_pull_request(pr_number: str):
    # Get PR diff
    diff = subprocess.check_output(
        ["gh", "pr", "diff", pr_number]
    ).decode()

    # Create review prompt
    prompt = f"""
    Review this pull request for:
    - Code quality and best practices
    - Security vulnerabilities
    - Performance issues
    - Test coverage

    {diff}
    """

    review = ""

    options = ClaudeAgentOptions(
        system_prompt="You are a senior code reviewer",
        allowed_tools=["Read", "Grep"],
        max_turns=5
    )

    async for message in query(prompt=prompt, options=options):
        if hasattr(message, 'result'):
            review = message.result

    # Post review as comment
    subprocess.run(["gh", "pr", "comment", pr_number, "--body", review])

    return review

# Usage
asyncio.run(review_pull_request("123"))
```

### Example: Automated Documentation Generator

```typescript
import { query, tool, createSdkMcpServer } from "@anthropic-ai/claude-agent-sdk";
import { z } from "zod";
import { writeFileSync } from "fs";

// Custom tool for saving docs
const saveDocs = tool(
  "save_documentation",
  "Save generated documentation to file",
  {
    filename: z.string(),
    content: z.string()
  },
  async (args) => {
    writeFileSync(`./docs/${args.filename}`, args.content);
    return {
      content: [{
        type: "text",
        text: `Documentation saved to ./docs/${args.filename}`
      }]
    };
  }
);

const docsServer = createSdkMcpServer({
  name: "docs-tools",
  version: "1.0.0",
  tools: [saveDocs]
});

async function* generateMessages() {
  yield {
    type: "user" as const,
    message: {
      role: "user" as const,
      content: "Generate comprehensive API documentation for this codebase"
    }
  };
}

async function generateDocs() {
  for await (const message of query({
    prompt: generateMessages(),
    options: {
      systemPrompt: "You are a technical writer. Create clear, comprehensive documentation.",
      mcpServers: { docs: docsServer },
      allowedTools: ["Read", "Grep", "Glob", "mcp__docs__save_documentation"],
      maxTurns: 10
    }
  })) {
    console.log(message);
  }
}

generateDocs();
```

### Example: Interactive Development Assistant

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
import asyncio

class DevAssistant:
    def __init__(self):
        self.options = ClaudeAgentOptions(
            allowed_tools=["Read", "Write", "Edit", "Bash", "Grep"],
            permission_mode="acceptEdits"
        )

    async def start_session(self):
        async with ClaudeSDKClient(options=self.options) as client:
            print("Dev Assistant Ready! Type 'exit' to quit.")

            while True:
                user_input = input("\nYou: ")

                if user_input.lower() == 'exit':
                    break
                elif user_input.lower() == 'interrupt':
                    await client.interrupt()
                    print("Task interrupted!")
                    continue

                await client.query(user_input)

                print("Assistant: ", end="")
                async for message in client.receive_response():
                    if isinstance(message, AssistantMessage):
                        for block in message.content:
                            if isinstance(block, TextBlock):
                                print(block.text, end="")
                print()

# Usage
assistant = DevAssistant()
asyncio.run(assistant.start_session())
```

---

## Best Practices

### 1. Security

- **Never commit API keys** - use environment variables or secrets management
- **Use permission modes appropriately**:
  - `default` for interactive development
  - `plan` for read-only analysis
  - `acceptEdits` only in trusted environments
  - `bypassPermissions` with extreme caution
- **Implement custom permission handlers** for sensitive operations
- **Validate tool inputs** in custom MCP tools
- **Use allowedTools/disallowedTools** to restrict capabilities

### 2. Performance

- **Use streaming mode** for real-time feedback
- **Set appropriate max_turns** to prevent runaway iterations
- **Configure timeouts** for long-running operations
- **Use plan mode** for analysis before execution
- **Leverage prompt caching** (automatic in SDK)
- **Load only necessary settings sources**

### 3. Workflow Optimization

- **Use subagents** for specialized tasks
- **Create custom slash commands** for repetitive workflows
- **Use CLAUDE.md** for project-specific guidelines
- **Fork sessions** for experimentation
- **Resume sessions** for continuity
- **Use hooks** for auditing and validation

### 4. Error Handling

- **Always wrap SDK calls in try-catch**
- **Handle specific error types** (CLINotFoundError, ProcessError, etc.)
- **Log errors with context** for debugging
- **Provide fallbacks** for tool failures
- **Validate inputs** before passing to Claude

### 5. Cost Management

- **Monitor token usage** via result messages
- **Use haiku model** for simple tasks
- **Set max_turns** appropriately
- **Use plan mode** to preview before execution
- **Cache prompts** when possible
- **Review usage patterns** regularly

### 6. Testing

- **Test with plan mode** before production
- **Validate tool outputs** in tests
- **Mock API calls** in development
- **Use different permission modes** for testing
- **Test error scenarios** explicitly

### 7. Documentation

- **Document custom tools** clearly
- **Maintain CLAUDE.md** up-to-date
- **Comment complex workflows**
- **Share subagent definitions** with team
- **Document permission requirements**

---

## Complete Examples

### Production-Ready Code Review Bot

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";
import { exec } from "child_process";
import { promisify } from "util";

const execAsync = promisify(exec);

interface ReviewResult {
  issues: Array<{
    severity: 'low' | 'medium' | 'high';
    file: string;
    line: number;
    description: string;
  }>;
  summary: string;
  cost: number;
}

async function reviewCode(
  targetBranch: string = "main",
  options: {
    maxTurns?: number;
    verbose?: boolean;
  } = {}
): Promise<ReviewResult> {
  try {
    // Get diff
    const { stdout: diff } = await execAsync(`git diff ${targetBranch}...HEAD`);

    if (!diff) {
      return {
        issues: [],
        summary: "No changes to review",
        cost: 0
      };
    }

    const prompt = `
      Perform a comprehensive code review of these changes:

      ${diff}

      Focus on:
      1. Security vulnerabilities
      2. Performance issues
      3. Code quality and maintainability
      4. Best practices violations
      5. Test coverage gaps

      Return a JSON object with:
      {
        "issues": [
          {
            "severity": "low|medium|high",
            "file": "path/to/file",
            "line": 42,
            "description": "Issue description"
          }
        ],
        "summary": "Overall assessment"
      }
    `;

    let result: ReviewResult = {
      issues: [],
      summary: "",
      cost: 0
    };

    for await (const message of query({
      prompt,
      options: {
        systemPrompt: {
          type: "preset",
          preset: "claude_code",
          append: "You are a senior code reviewer with expertise in security and performance."
        },
        allowedTools: ["Read", "Grep", "Glob"],
        permissionMode: "default",
        maxTurns: options.maxTurns || 5,
        settingSources: ['project']
      }
    })) {
      if (options.verbose) {
        console.log(message);
      }

      if (message.type === "result" && message.subtype === "success") {
        const parsed = JSON.parse(message.result);
        result.issues = parsed.issues;
        result.summary = parsed.summary;
        result.cost = message.total_cost_usd || 0;
      }
    }

    return result;

  } catch (error) {
    console.error("Code review failed:", error);
    throw error;
  }
}

// Usage
async function main() {
  const review = await reviewCode("main", { verbose: true });

  console.log(`\n\nReview Summary: ${review.summary}`);
  console.log(`Found ${review.issues.length} issues`);
  console.log(`Cost: $${review.cost.toFixed(4)}`);

  // Filter high severity
  const highSeverity = review.issues.filter(i => i.severity === 'high');
  if (highSeverity.length > 0) {
    console.log("\n🚨 High Severity Issues:");
    highSeverity.forEach(issue => {
      console.log(`  ${issue.file}:${issue.line} - ${issue.description}`);
    });
    process.exit(1);
  }
}

main();
```

---

## Additional Resources

### Official Documentation
- [Claude Code CLI Reference](https://docs.claude.com/en/docs/claude-code/cli-reference)
- [TypeScript SDK Reference](https://docs.claude.com/en/api/agent-sdk/typescript)
- [Python SDK Reference](https://docs.claude.com/en/api/agent-sdk/python)
- [MCP Documentation](https://modelcontextprotocol.io)

### GitHub Repositories
- [Claude Code Action](https://github.com/anthropics/claude-code-action)
- [TypeScript SDK](https://github.com/anthropics/claude-agent-sdk-typescript)
- [Python SDK](https://github.com/anthropics/claude-agent-sdk-python)

### Community
- [GitHub Discussions](https://github.com/anthropics/claude-code/discussions)
- Report issues: TypeScript SDK | Python SDK

---

**Document Version:** 1.0
**Last Updated:** 2025-10-02
**Source:** Local Claude Code documentation
