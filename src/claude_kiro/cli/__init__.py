"""Claude Kiro CLI package.

This package provides the unified `ck` command-line interface for:
- Project initialization (ck init)
- Hook management (ck hook)
- Health checking (ck doctor)
- Hook execution for Claude Code (ck --hook)
"""

from .main import cli

__all__ = ["cli"]
