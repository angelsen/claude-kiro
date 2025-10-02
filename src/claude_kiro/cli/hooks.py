"""Hook management subcommands for the Claude Kiro CLI."""

import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any

import click

from .runner import HookRegistry


@click.group()
def hook():
    """Manage hooks for Claude Code integration with Claude Kiro specs."""
    pass


@hook.command()
def list():
    """List all available hook modules."""
    registry = HookRegistry()
    hooks = registry.list_hooks()

    if not hooks:
        click.echo("No hooks available.")
        return

    click.echo("Available hooks:")
    for hook_name in sorted(hooks):
        hook_func = registry.get_hook(hook_name)
        if hook_func:
            # Try to get docstring from the hook module
            module_path = (
                hook_func if isinstance(hook_func, str) else hook_func.__module__
            )
            click.echo(f"\n  📎 {hook_name}")
            click.echo(f"     Module: {module_path}")

            # Get description if available
            if hook_name == "post-file-ops":
                click.echo(
                    "     Description: Injects spec context after file operations"
                )


@hook.command()
def status():
    """Show which hooks are configured in settings.local.json."""
    claude_dir = Path.cwd() / ".claude"
    settings_file = claude_dir / "settings.local.json"

    if not settings_file.exists():
        click.echo("❌ No settings.local.json found")
        click.echo("\n💡 Run 'ck init' to create it")
        return

    try:
        settings = json.loads(settings_file.read_text())
        hooks = settings.get("hooks", {})

        if not hooks:
            click.echo("⚠️  No hooks configured in settings.local.json")
            click.echo("\n💡 Run 'ck hook config' to generate configuration")
            return

        click.echo("Configured hooks:")
        for hook_name, command in hooks.items():
            status_icon = "✓" if "ck --hook" in command else "⚠️"
            click.echo(f"\n  {status_icon} {hook_name}")
            click.echo(f"     Command: {command}")

            if "ckh-" in command:
                click.echo("     ⚠️  Using deprecated command style")
                click.echo(f"     💡 Update to: ck --hook {hook_name}")

    except json.JSONDecodeError as e:
        click.echo(f"❌ Failed to parse settings.local.json: {e}")


@hook.command()
@click.argument("name")
@click.argument("json_file", type=click.Path(exists=True), required=False)
def test(name: str, json_file: Optional[str]):
    """Test a hook with sample JSON data.

    \b
    NAME: Hook name to test (e.g., post-file-ops)
    JSON_FILE: Path to JSON file with test data (optional, uses empty JSON if not provided)
    """
    registry = HookRegistry()

    # Check if hook exists
    if name not in registry.list_hooks():
        click.echo(f"❌ Hook '{name}' not found")
        click.echo("\nAvailable hooks:")
        for hook_name in registry.list_hooks():
            click.echo(f"  - {hook_name}")
        sys.exit(1)

    # Load test data
    test_data: Dict[str, Any] = {}
    if json_file:
        try:
            with open(json_file, "r") as f:
                test_data = json.load(f)
            click.echo(f"📄 Loaded test data from {json_file}")
        except json.JSONDecodeError as e:
            click.echo(f"❌ Failed to parse JSON: {e}")
            sys.exit(1)
    else:
        click.echo("📄 Using empty JSON input")

    # Execute the hook
    click.echo(f"\n🔧 Executing hook: {name}")
    click.echo("=" * 40)

    try:
        from .runner import execute_hook

        result = execute_hook(name, test_data)

        if result:
            click.echo("\n📤 Output:")
            click.echo(json.dumps(result, indent=2))
        else:
            click.echo("\n✓ Hook executed successfully (no output)")

    except Exception as e:
        click.echo(f"\n❌ Hook execution failed: {e}")
        sys.exit(1)


@hook.command()
def config():
    """Generate settings.json snippet for hook configuration."""
    click.echo("📋 Add this to your .claude/settings.local.json:\n")

    config_snippet = {
        "hooks": {
            "PostToolUse": [
                {
                    "matcher": "Edit|Write|MultiEdit",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "ck --hook post-file-ops",
                            "timeout": 5000,
                        }
                    ],
                }
            ]
        }
    }

    click.echo(json.dumps(config_snippet, indent=2))

    click.echo("\n💡 Tips:")
    click.echo("  - settings.local.json is for local overrides")
    click.echo("  - settings.json is for shared project settings")
    click.echo("  - Claude Code merges both, with local taking precedence")
    click.echo(
        "\n📚 Learn more about hooks: https://docs.claude.com/en/docs/claude-code/hooks"
    )
