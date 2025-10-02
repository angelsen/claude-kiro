# Claude Code Hooks - Research Documentation

## Overview

Claude Code hooks are user-defined shell commands that execute at various points in Claude Code's lifecycle. They provide deterministic control over Claude Code's behavior, ensuring certain actions always happen rather than relying on the LLM to choose to run them.

## Hook Events

Claude Code provides 9 different hook events that trigger at specific points in the workflow:

### 1. PreToolUse

**When it triggers:** After Claude creates tool parameters and before processing the tool call.

**Use cases:**
- Validate bash commands before execution
- Block modifications to protected files
- Auto-approve certain tool calls
- Add guardrails for tool usage

**Input data:**
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/working/directory",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  }
}
```

**Common matchers:**
- `Task` - Subagent tasks
- `Bash` - Shell commands
- `Glob` - File pattern matching
- `Grep` - Content search
- `Read` - File reading
- `Edit`, `MultiEdit` - File editing
- `Write` - File writing
- `WebFetch`, `WebSearch` - Web operations
- `mcp__<server>__<tool>` - MCP tools

**Exit code 2 behavior:** Blocks the tool call, shows stderr to Claude

### 2. PostToolUse

**When it triggers:** Immediately after a tool completes successfully.

**Use cases:**
- Run code formatters after file edits
- Validate output files
- Update related files
- Run tests after code changes
- Track command history

**Input data:**
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/working/directory",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  },
  "tool_response": {
    "filePath": "/path/to/file.txt",
    "success": true
  }
}
```

**Exit code 2 behavior:** Shows stderr to Claude (tool already ran)

### 3. UserPromptSubmit

**When it triggers:** When the user submits a prompt, before Claude processes it.

**Use cases:**
- Add additional context (e.g., current time, project status)
- Validate prompts for sensitive patterns
- Block certain types of prompts
- Inject project-specific information

**Input data:**
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/working/directory",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "Write a function to calculate the factorial of a number"
}
```

**Special behavior:** With exit code 0, stdout is added as context for Claude (unlike other hooks).

**Exit code 2 behavior:** Blocks prompt processing, erases prompt, shows stderr to user only

### 4. Notification

**When it triggers:** When Claude Code sends notifications.

**Notification types:**
1. Claude needs your permission to use a tool
2. The prompt input has been idle for at least 60 seconds

**Use cases:**
- Send desktop notifications
- Custom notification systems
- Integration with external alerting tools

**Input data:**
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/working/directory",
  "hook_event_name": "Notification",
  "message": "Task completed successfully"
}
```

**Exit code 2 behavior:** N/A, shows stderr to user only

### 5. Stop

**When it triggers:** When the main Claude Code agent has finished responding (not if stopped by user interrupt).

**Use cases:**
- Enforce completion of certain tasks
- Add follow-up prompts
- Validate completion state
- Log session statistics

**Input data:**
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "hook_event_name": "Stop",
  "stop_hook_active": true
}
```

**Special field:** `stop_hook_active` - true when Claude Code is already continuing as a result of a stop hook (prevents infinite loops)

**Exit code 2 behavior:** Blocks stoppage, shows stderr to Claude

### 6. SubagentStop

**When it triggers:** When a Claude Code subagent (Task tool call) has finished responding.

**Use cases:**
- Similar to Stop but for subagent tasks
- Validate subagent results
- Chain subagent tasks

**Input data:**
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "hook_event_name": "SubagentStop",
  "stop_hook_active": true
}
```

**Exit code 2 behavior:** Blocks stoppage, shows stderr to Claude subagent

### 7. PreCompact

**When it triggers:** Before Claude Code runs a compact operation.

**Use cases:**
- Customize compact instructions
- Save pre-compact state
- Add context before compaction

**Matchers:**
- `manual` - Invoked from `/compact`
- `auto` - Invoked from auto-compact (due to full context window)

**Input data:**
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "hook_event_name": "PreCompact",
  "trigger": "manual",
  "custom_instructions": ""
}
```

**Exit code 2 behavior:** N/A, shows stderr to user only

### 8. SessionStart

**When it triggers:** When Claude Code starts a new session or resumes an existing session.

**Use cases:**
- Load development context
- Add issue tracker information
- Inject recent codebase changes
- Initialize session state

**Matchers:**
- `startup` - Invoked from startup
- `resume` - Invoked from `--resume`, `--continue`, or `/resume`
- `clear` - Invoked from `/clear`
- `compact` - Invoked from auto or manual compact

**Input data:**
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "hook_event_name": "SessionStart",
  "source": "startup"
}
```

**Special behavior:** stdout is added as context for Claude (like UserPromptSubmit)

**Exit code 2 behavior:** N/A, shows stderr to user only

### 9. SessionEnd

**When it triggers:** When a Claude Code session ends.

**Use cases:**
- Cleanup tasks
- Log session statistics
- Save session state
- Archival operations

**Reason values:**
- `clear` - Session cleared with /clear command
- `logout` - User logged out
- `prompt_input_exit` - User exited while prompt input was visible
- `other` - Other exit reasons

**Input data:**
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/working/directory",
  "hook_event_name": "SessionEnd",
  "reason": "exit"
}
```

**Exit code 2 behavior:** N/A, shows stderr to user only

## Hook Configuration

### Configuration Files

Hooks are configured in settings files with this precedence:
1. `~/.claude/settings.json` - User settings
2. `.claude/settings.json` - Project settings
3. `.claude/settings.local.json` - Local project settings (not committed)
4. Enterprise managed policy settings

### Basic Structure

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

### Matcher Patterns

- **Simple strings:** Match exactly (`Write` matches only the Write tool)
- **Regex:** Use patterns like `Edit|Write` or `Notebook.*`
- **Wildcard:** Use `*` to match all tools
- **Empty:** Empty string (`""`) or omit matcher for events without tools
- **Case-sensitive:** Matchers are case-sensitive

### Events Without Matchers

For `UserPromptSubmit`, `Notification`, `Stop`, and `SubagentStop`, omit the matcher field:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/script.py"
          }
        ]
      }
    ]
  }
}
```

### Project-Specific Scripts

Use `$CLAUDE_PROJECT_DIR` environment variable to reference project scripts:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/check-style.sh"
          }
        ]
      }
    ]
  }
}
```

## Hook Input/Output

### Input Format

Hooks receive JSON via stdin containing:
- Common fields: `session_id`, `transcript_path`, `cwd`, `hook_event_name`
- Event-specific fields vary by event type

### Output Methods

#### Method 1: Exit Codes (Simple)

- **Exit 0:** Success
  - `stdout` shown to user in transcript mode (CTRL-R)
  - Exception: For `UserPromptSubmit` and `SessionStart`, stdout is added as context for Claude
- **Exit 2:** Blocking error
  - `stderr` is fed back to Claude to process automatically
  - Behavior varies by hook event (see table in reference)
- **Other exit codes:** Non-blocking error
  - `stderr` shown to user, execution continues

#### Method 2: JSON Output (Advanced)

##### Common JSON Fields

All hook types support these optional fields:

```json
{
  "continue": true,
  "stopReason": "string",
  "suppressOutput": true,
  "systemMessage": "string"
}
```

- `continue`: Whether Claude should continue after hook execution (default: true)
- `stopReason`: Message shown when continue is false
- `suppressOutput`: Hide stdout from transcript mode (default: false)
- `systemMessage`: Optional warning message shown to the user

##### PreToolUse Decision Control

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow" | "deny" | "ask",
    "permissionDecisionReason": "My reason here"
  }
}
```

- `"allow"`: Bypasses permission system, reason shown to user but not Claude
- `"deny"`: Prevents tool call, reason shown to Claude
- `"ask"`: Asks user to confirm, reason shown to user but not Claude

##### PostToolUse Decision Control

```json
{
  "decision": "block" | undefined,
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Additional information for Claude"
  }
}
```

- `"block"`: Automatically prompts Claude with reason
- `undefined`: Does nothing, reason is ignored
- `additionalContext`: Adds context for Claude to consider

##### UserPromptSubmit Decision Control

```json
{
  "decision": "block" | undefined,
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "My additional context here"
  }
}
```

- `"block"`: Prevents prompt processing, erases submitted prompt from context
- `undefined`: Allows prompt to proceed normally
- `additionalContext`: Added to context if not blocked

##### Stop/SubagentStop Decision Control

```json
{
  "decision": "block" | undefined,
  "reason": "Must be provided when Claude is blocked from stopping"
}
```

- `"block"`: Prevents Claude from stopping, must provide reason
- `undefined`: Allows Claude to stop

##### SessionStart Decision Control

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "My additional context here"
  }
}
```

Multiple hooks' `additionalContext` values are concatenated.

## MCP Integration

### MCP Tool Naming Pattern

MCP tools follow: `mcp__<server>__<tool>`

Examples:
- `mcp__memory__create_entities`
- `mcp__filesystem__read_file`
- `mcp__github__search_repositories`

### Configuring Hooks for MCP Tools

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__memory__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Memory operation initiated' >> ~/mcp-operations.log"
          }
        ]
      },
      {
        "matcher": "mcp__.*__write.*",
        "hooks": [
          {
            "type": "command",
            "command": "/home/user/scripts/validate-mcp-write.py"
          }
        ]
      }
    ]
  }
}
```

## Hook Execution Details

- **Timeout:** 60-second default, configurable per command
- **Parallelization:** All matching hooks run in parallel
- **Deduplication:** Identical hook commands are deduplicated automatically
- **Environment:** Runs in current directory with Claude Code's environment
  - `CLAUDE_PROJECT_DIR` environment variable available
- **Input:** JSON via stdin
- **Output visibility:**
  - PreToolUse/PostToolUse/Stop/SubagentStop: Progress shown in transcript (Ctrl-R)
  - Notification/SessionEnd: Logged to debug only (`--debug`)
  - UserPromptSubmit/SessionStart: stdout added as context for Claude

## Configuration Safety

Direct edits to hooks in settings files don't take effect immediately:

1. Hooks are captured at startup as a snapshot
2. Snapshot is used throughout the session
3. Warning shown if hooks are modified externally
4. Changes require review in `/hooks` menu to apply

This prevents malicious hook modifications from affecting the current session.

## Examples

### Example 1: Bash Command Validation (Exit Code)

```python
#!/usr/bin/env python3
import json
import re
import sys

VALIDATION_RULES = [
    (
        r"\bgrep\b(?!.*\|)",
        "Use 'rg' (ripgrep) instead of 'grep' for better performance",
    ),
    (
        r"\bfind\s+\S+\s+-name\b",
        "Use 'rg --files | rg pattern' instead of 'find -name'",
    ),
]

def validate_command(command: str) -> list[str]:
    issues = []
    for pattern, message in VALIDATION_RULES:
        if re.search(pattern, command):
            issues.append(message)
    return issues

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})
command = tool_input.get("command", "")

if tool_name != "Bash" or not command:
    sys.exit(1)

issues = validate_command(command)

if issues:
    for message in issues:
        print(f"• {message}", file=sys.stderr)
    # Exit code 2 blocks tool call and shows stderr to Claude
    sys.exit(2)
```

### Example 2: UserPromptSubmit with Context Injection (JSON)

```python
#!/usr/bin/env python3
import json
import sys
import re
import datetime

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

prompt = input_data.get("prompt", "")

# Check for sensitive patterns
sensitive_patterns = [
    (r"(?i)\b(password|secret|key|token)\s*[:=]", "Prompt contains potential secrets"),
]

for pattern, message in sensitive_patterns:
    if re.search(pattern, prompt):
        # Use JSON output to block with a specific reason
        output = {
            "decision": "block",
            "reason": f"Security policy violation: {message}"
        }
        print(json.dumps(output))
        sys.exit(0)

# Add current time to context
context = f"Current time: {datetime.datetime.now()}"
print(context)

# Allow the prompt to proceed with the additional context
sys.exit(0)
```

### Example 3: Auto-Approve Documentation Files (JSON)

```python
#!/usr/bin/env python3
import json
import sys

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})

if tool_name == "Read":
    file_path = tool_input.get("file_path", "")
    if file_path.endswith((".md", ".mdx", ".txt", ".json")):
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "permissionDecisionReason": "Documentation file auto-approved"
            },
            "suppressOutput": True
        }
        print(json.dumps(output))
        sys.exit(0)

sys.exit(0)
```

### Example 4: TypeScript Formatting Hook

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | { read file_path; if echo \"$file_path\" | grep -q '\\.ts$'; then npx prettier --write \"$file_path\"; fi; }"
          }
        ]
      }
    ]
  }
}
```

### Example 5: Bash Command Logging

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '\"\\(.tool_input.command) - \\(.tool_input.description // \"No description\")\"' >> ~/.claude/bash-command-log.txt"
          }
        ]
      }
    ]
  }
}
```

### Example 6: Desktop Notifications

```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' 'Awaiting your input'"
          }
        ]
      }
    ]
  }
}
```

### Example 7: File Protection

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 -c \"import json, sys; data=json.load(sys.stdin); path=data.get('tool_input',{}).get('file_path',''); sys.exit(2 if any(p in path for p in ['.env', 'package-lock.json', '.git/']) else 0)\""
          }
        ]
      }
    ]
  }
}
```

## Best Practices

### Security

1. **Validate and sanitize inputs** - Never trust input data blindly
2. **Always quote shell variables** - Use `"$VAR"` not `$VAR`
3. **Block path traversal** - Check for `..` in file paths
4. **Use absolute paths** - Specify full paths for scripts (use `$CLAUDE_PROJECT_DIR`)
5. **Skip sensitive files** - Avoid `.env`, `.git/`, keys, etc.

### Hook Design

1. **Start simple** - Begin with basic hooks and build up
2. **Test thoroughly** - Run hook commands manually first
3. **Use descriptive names** - Clear naming helps debugging
4. **Monitor performance** - Check hook execution time
5. **Handle errors gracefully** - Provide helpful error messages

### Debugging

1. **Check configuration** - Run `/hooks` to see registered hooks
2. **Verify syntax** - Ensure JSON settings are valid
3. **Test commands manually** - Run commands outside of hooks first
4. **Check permissions** - Make sure scripts are executable
5. **Review logs** - Use `claude --debug` for detailed execution info

Common issues:
- **Quotes not escaped** - Use `\"` inside JSON strings
- **Wrong matcher** - Tool names are case-sensitive
- **Command not found** - Use full paths for scripts

## Security Warning

**USE AT YOUR OWN RISK**: Claude Code hooks execute arbitrary shell commands on your system automatically. By using hooks, you acknowledge that:

- You are solely responsible for the commands you configure
- Hooks can modify, delete, or access any files your user account can access
- Malicious or poorly written hooks can cause data loss or system damage
- Anthropic provides no warranty and assumes no liability
- You should thoroughly test hooks in a safe environment before production use

Always review and understand any hook commands before adding them to your configuration.

## Debugging Output

Use `claude --debug` to see hook execution details:

```
[DEBUG] Executing hooks for PostToolUse:Write
[DEBUG] Getting matching hook commands for PostToolUse with query: Write
[DEBUG] Found 1 hook matchers in settings
[DEBUG] Matched 1 hooks for query "Write"
[DEBUG] Found 1 hook commands to execute
[DEBUG] Executing hook command: <Your command> with timeout 60000ms
[DEBUG] Hook command completed with status 0: <Your stdout>
```

Progress messages appear in transcript mode (Ctrl-R) showing:
- Which hook is running
- Command being executed
- Success/failure status
- Output or error messages
