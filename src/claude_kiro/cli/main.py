"""Main CLI entry point for Claude Kiro.

Provides the `ck` command with subcommands for project management and a hidden
hook runner for Claude Code integration.
"""

import sys
import json
import logging
from pathlib import Path
from typing import Optional

import click

from .hooks import hook
from .runner import execute_hook


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stderr)
logger = logging.getLogger(__name__)


@click.group(invoke_without_command=True)
@click.option(
    "--hook",
    "hook_name",
    hidden=True,
    help="Execute a hook (for Claude Code integration)",
)
@click.pass_context
def cli(ctx: click.Context, hook_name: Optional[str]):
    """Claude Kiro - Spec-driven development methodology for use with Claude Code.

    Initialize projects with spec-driven workflow, configure Claude Code hooks,
    and verify setup with the unified `ck` command.
    """
    if hook_name:
        # Hidden hook execution mode for Claude Code
        try:
            # Read JSON from stdin
            input_data = sys.stdin.read()
            input_json = json.loads(input_data) if input_data else {}

            # Execute the hook
            result = execute_hook(hook_name, input_json)

            # Write result to stdout
            if result is not None:
                print(json.dumps(result), file=sys.stdout, flush=True)

            sys.exit(0)
        except Exception as e:
            logger.error(f"Hook execution failed: {e}")
            sys.exit(1)
    elif ctx.invoked_subcommand is None:
        # No subcommand, show help
        click.echo(ctx.get_help())


@cli.command()
@click.option("--force", is_flag=True, help="Overwrite existing files")
def init(force: bool):
    """Initialize a Claude Kiro project in the current directory.

    Creates .claude directory structure with output styles, slash commands,
    and configures hooks in settings.local.json.
    """
    from ..resources import ResourceLoader
    import json

    project_dir = Path.cwd()
    claude_dir = project_dir / ".claude"

    # Track what we create/skip
    created = []
    skipped = []

    # Create directory structure
    directories = [
        claude_dir,
        claude_dir / "output-styles",
        claude_dir / "commands",
        claude_dir / "commands" / "spec",
        claude_dir / "specs",
    ]

    for directory in directories:
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
            created.append(str(directory.relative_to(project_dir)))

    # Load resources and create files
    loader = ResourceLoader()

    files_to_create = [
        (".claude/CLAUDE.md", "claude_md.md"),
        (".claude/output-styles/spec-driven.md", "output_styles/spec_driven.md"),
        (".claude/commands/spec/create.md", "commands/spec/create.md"),
        (".claude/commands/spec/implement.md", "commands/spec/implement.md"),
        (".claude/commands/spec/review.md", "commands/spec/review.md"),
    ]

    for target_path, resource_path in files_to_create:
        target = project_dir / target_path

        if target.exists() and not force:
            skipped.append(target_path)
            continue

        try:
            content = loader.get_resource(resource_path)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
            created.append(target_path)
        except Exception as e:
            logger.error(f"Failed to create {target_path}: {e}")

    # Configure hooks in settings.local.json
    settings_file = claude_dir / "settings.local.json"
    settings = {}

    if settings_file.exists():
        try:
            settings = json.loads(settings_file.read_text())
        except json.JSONDecodeError:
            # Backup corrupted file
            backup = settings_file.with_suffix(".json.bak")
            settings_file.rename(backup)
            logger.warning(f"Backed up corrupted settings to {backup}")
            settings = {}

    # Add hook configuration in proper Claude Code format
    if "hooks" not in settings:
        settings["hooks"] = {}

    # Use Claude Code's required structure
    settings["hooks"]["PostToolUse"] = [
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

    # Write settings
    settings_file.write_text(json.dumps(settings, indent=2))
    created.append(".claude/settings.local.json")

    # Report results
    click.echo("\n✨ Claude Kiro initialized successfully!")

    if created:
        click.echo("\n📁 Created:")
        for item in created:
            click.echo(f"  ✓ {item}")

    if skipped:
        click.echo("\n⏭️  Skipped (already exists):")
        for item in skipped:
            click.echo(f"  - {item}")
        click.echo("\n💡 Use --force to overwrite existing files")

    # Show next steps
    click.echo("\n🚀 Next steps:")
    click.echo("  1. Review .claude/CLAUDE.md and customize for your project")
    click.echo("  2. Run 'ck doctor' to verify setup")
    click.echo("  3. Use /spec:create to start spec-driven development")
    click.echo(
        "\n📚 Claude Code hooks docs: https://docs.claude.com/en/docs/claude-code/hooks"
    )


@cli.command()
def doctor():
    """Check Claude Kiro setup health.

    Verifies installation, directory structure, file presence, and hook configuration.
    """
    import shutil
    import json

    project_dir = Path.cwd()
    claude_dir = project_dir / ".claude"
    issues = []
    warnings = []

    click.echo("🔍 Checking Claude Kiro setup...\n")

    # Check 1: ck command installed
    if shutil.which("ck"):
        click.echo("✓ ck command is installed")
    else:
        issues.append("ck command not found in PATH")

    # Check 2: .claude directory exists
    if claude_dir.exists():
        click.echo("✓ .claude directory exists")
    else:
        issues.append(".claude directory not found - run 'ck init'")
        # Can't continue other checks without .claude
        _report_doctor_results(issues, warnings)
        return

    # Check 3: Required files present
    required_files = [
        ".claude/output-styles/spec-driven.md",
        ".claude/commands/spec/create.md",
        ".claude/commands/spec/implement.md",
        ".claude/commands/spec/review.md",
    ]

    missing_files = []
    for file_path in required_files:
        if not (project_dir / file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        issues.append(f"Missing files: {', '.join(missing_files)}")
    else:
        click.echo("✓ All required files present")

    # Check 4: Hooks configured
    settings_file = claude_dir / "settings.local.json"
    if settings_file.exists():
        try:
            settings = json.loads(settings_file.read_text())
            hooks = settings.get("hooks", {})

            # Check for Claude Code PostToolUse format
            hook_found = False
            if "PostToolUse" in hooks:
                for hook_config in hooks["PostToolUse"]:
                    if isinstance(hook_config, dict) and "hooks" in hook_config:
                        for hook_item in hook_config["hooks"]:
                            if isinstance(hook_item, dict) and "command" in hook_item:
                                cmd = hook_item["command"]
                                if "ck --hook" in cmd or "ckh-post-file-ops" in cmd:
                                    click.echo(f"✓ Hook configured: {cmd}")
                                    hook_found = True
                                    break
                        if hook_found:
                            break

            if not hook_found:
                issues.append("PostToolUse hook not configured - run 'ck init' to fix")
        except json.JSONDecodeError:
            issues.append("settings.local.json is corrupted")
    else:
        warnings.append("settings.local.json not found - hooks may not be configured")

    # Check 5: Count existing specs
    specs_dir = claude_dir / "specs"
    if specs_dir.exists():
        spec_count = len(list(specs_dir.glob("**/requirements.md")))
        if spec_count > 0:
            click.echo(f"✓ Found {spec_count} spec(s)")
        else:
            click.echo("ℹ️  No specs created yet")
    else:
        click.echo("ℹ️  Specs directory not found")

    _report_doctor_results(issues, warnings)


def _report_doctor_results(issues: list, warnings: list):
    """Report the results of doctor command."""
    if warnings:
        click.echo("\n⚠️  Warnings:")
        for warning in warnings:
            click.echo(f"  - {warning}")

    if issues:
        click.echo("\n❌ Issues found:")
        for issue in issues:
            click.echo(f"  - {issue}")

        click.echo("\n💡 To fix:")
        click.echo("  1. Run 'ck init' to set up project")
        click.echo("  2. Run 'ck hook config' for settings snippet")
        click.echo(
            "  3. Claude Code settings docs: https://docs.claude.com/en/docs/claude-code/settings"
        )
    else:
        click.echo("\n✅ Everything looks good!")
        click.echo("\n🎉 Your Claude Kiro setup is healthy and ready to use!")


# Add hook subcommand group
cli.add_command(hook)


if __name__ == "__main__":
    cli()
