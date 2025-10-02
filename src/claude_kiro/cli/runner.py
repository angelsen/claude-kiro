"""Hook execution runner for Claude Code integration."""

import importlib
from typing import Dict, Any, Optional, List


class HookRegistry:
    """Registry of available hooks for Claude Kiro."""

    _hooks: Dict[str, str] = {
        "post-file-ops": "claude_kiro.hooks.post_file_ops_spec_context:hook",
        # Future hooks will be added here
    }

    def get_hook(self, name: str) -> Optional[str]:
        """Get hook module path by name.

        Args:
            name: Hook name (e.g., 'post-file-ops')

        Returns:
            Module path string if hook exists, None otherwise
        """
        return self._hooks.get(name)

    def list_hooks(self) -> List[str]:
        """List all available hook names.

        Returns:
            List of hook names
        """
        return list(self._hooks.keys())


def execute_hook(
    hook_name: str, input_data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """Execute a hook by name with the provided input data.

    Args:
        hook_name: Name of the hook to execute
        input_data: JSON data to pass to the hook

    Returns:
        Hook output as dict, or None if no output

    Raises:
        ValueError: If hook is not found
        Exception: If hook execution fails
    """
    registry = HookRegistry()
    hook_path = registry.get_hook(hook_name)

    if not hook_path:
        raise ValueError(
            f"Hook '{hook_name}' not found. Available: {', '.join(registry.list_hooks())}"
        )

    # Parse module and function name
    if ":" in hook_path:
        module_path, func_name = hook_path.rsplit(":", 1)
    else:
        module_path = hook_path
        func_name = "hook"

    try:
        # Import the hook module
        module = importlib.import_module(module_path)

        # Get the hook function
        if not hasattr(module, func_name):
            raise ValueError(
                f"Hook module {module_path} does not have function '{func_name}'"
            )

        hook_func = getattr(module, func_name)

        # Execute the hook - it's now a clean function that takes dict and returns dict
        return hook_func(input_data)

    except ImportError as e:
        raise ImportError(f"Failed to import hook module {module_path}: {e}")
    except Exception as e:
        raise Exception(f"Hook execution failed: {e}")
