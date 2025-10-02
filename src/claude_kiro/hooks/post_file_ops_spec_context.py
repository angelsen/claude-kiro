"""PostToolUse Hook: Spec Context Provider with Session Tracking.

Provides spec context when editing files, showing messages only once per file per session.
"""

import os

from claude_kiro.hooks._shared.cache_manager import CacheManager
from claude_kiro.hooks._shared.session_tracker import SessionTracker
from claude_kiro.hooks._shared.spec_parser import SpecParser


def generate_spec_context_message(
    spec_name: str, task_num: str, task_title: str
) -> str:
    """Generate context message for a file in a spec.

    Args:
        spec_name: Name of the spec.
        task_num: Task number.
        task_title: Task title.

    Returns:
        Formatted context message.
    """
    return f"""
📋 **Spec Task Context: {spec_name}**

You are working on Task {task_num}: {task_title}

Before proceeding:
1. Read `.claude/specs/{spec_name}/requirements.md` - verify acceptance criteria
2. Read `.claude/specs/{spec_name}/design.md` - follow architectural decisions
3. Check `.claude/specs/{spec_name}/tasks.md` - review full task acceptance checklist

Your responsibilities:
- As you complete acceptance criteria, update the checkboxes in tasks.md to [x]
- When a task is fully complete, mark it with ✅ COMPLETE
- Keep the spec documentation current, just like you maintain TodoWrite
- Update the overall spec status when all tasks are done

Ensure your changes align with the spec requirements and design.
"""


def generate_no_spec_message(file_path: str) -> str:
    """Generate message for a file not in any spec.

    Args:
        file_path: Path to the file.

    Returns:
        Formatted suggestion message.
    """
    # Extract just the filename for cleaner display
    file_name = os.path.basename(file_path)

    return f"""
⚠️ **File Not in Specification**

The file `{file_name}` is not part of any existing specification.

WHEN we work on new feature code, you should suggest to me creating a specification first.

Your task:
1. Infer what feature this file relates to based on file path and context
2. Suggest to me: "You can run `/spec-create [inferred-feature-description]`"

Example: "You can run `/spec-create Add user authentication system`"

If this is a quick fix or non-feature work, acknowledge and proceed without requiring a spec.
"""


def hook(input_data: dict) -> dict | None:
    """Process post-file-ops hook.

    Args:
        input_data: Hook input from Claude Code

    Returns:
        Hook output dict or None if no output needed
    """

    # Extract relevant fields
    tool_name = input_data.get("tool_name", "")
    session_id = input_data.get("session_id", "unknown")

    # Only process file modification tools
    if tool_name not in ["Edit", "Write", "MultiEdit"]:
        return None

    # Get file path from tool input
    tool_input = input_data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")

    if not file_path:
        return None

    # IGNORE operations on spec files themselves
    if "/.claude/specs/" in file_path:
        return None

    # Get project directory
    cwd = input_data.get("cwd", os.getcwd())

    # Initialize components
    cache_manager = CacheManager()
    session_tracker = SessionTracker(session_id, cache_manager)
    spec_parser = SpecParser(cwd)

    # Clean up old sessions on first file of a new session
    if session_tracker.get_notification_count() == 0:
        session_tracker.cleanup_old_sessions(session_id)

    # Check if we've already notified about this file in this session
    if session_tracker.has_notified(file_path):
        # Already notified, return None
        return None

    # Find if this file is mentioned in any spec
    task_match = spec_parser.find_matching_task(file_path)

    if task_match:
        # File IS in spec → generate task context message
        context = generate_spec_context_message(
            task_match.spec_name, task_match.task_num, task_match.task_title
        )

        # Mark file as notified (in spec)
        session_tracker.mark_notified(
            file_path,
            in_spec=True,
            spec_name=task_match.spec_name,
            task_num=task_match.task_num,
        )

    else:
        # File NOT in any spec → suggest creating one
        context = generate_no_spec_message(file_path)

        # Mark file as notified (not in spec)
        session_tracker.mark_notified(file_path, in_spec=False)

    # Return the context for Claude Code
    return {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": context,
        }
    }
