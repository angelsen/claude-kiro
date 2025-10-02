"""Spec file parsing for Claude Kiro hooks.

Parses tasks.md files to find which files are associated with which tasks.
"""

import os
import glob
import re
from pathlib import Path
from typing import List, Tuple, Optional, NamedTuple


class TaskMatch(NamedTuple):
    """Result of matching a file to a spec task."""

    spec_name: str
    task_num: str
    task_title: str


class SpecParser:
    """Parser for Claude Kiro spec files."""

    def __init__(self, project_dir: Optional[Path] = None):
        """Initialize spec parser.

        Args:
            project_dir: Project root directory. Defaults to current directory.
        """
        self.project_dir = Path(project_dir) if project_dir else Path.cwd()
        self.specs_dir = self.project_dir / ".claude" / "specs"

    def find_spec_files(self) -> List[Path]:
        """Find all tasks.md files in .claude/specs/*/.

        Returns:
            List of paths to tasks.md files.
        """
        if not self.specs_dir.exists():
            return []

        pattern = str(self.specs_dir / "*" / "tasks.md")
        return [Path(p) for p in glob.glob(pattern)]

    def parse_task_file(self, task_file_path: Path) -> List[Tuple[str, str, List[str]]]:
        """Parse tasks.md and extract file mentions.

        Expected format:
            ### Task 11: Implement accessibility features
            **Files:**
            - `docs/index.html` - Enhance with accessibility attributes
            - `src/components/Header.tsx` - Add ARIA labels

        Args:
            task_file_path: Path to tasks.md file.

        Returns:
            List of tuples: (task_number, task_title, [files])
        """
        tasks = []

        try:
            with open(task_file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except (OSError, IOError):
            return tasks

        # Split by task headers (### Task N: Title)
        task_pattern = r"### Task (\d+): (.+?)(?=\n### Task |\Z)"
        task_matches = re.finditer(task_pattern, content, re.DOTALL)

        for match in task_matches:
            task_num = match.group(1)
            # Extract just the title (first line, no newlines)
            task_title = match.group(2).split("\n")[0].strip()
            task_content = match.group(0)  # Use full match for file extraction

            # Extract files from **Files:** section
            files = []
            # Look for files in backticks with dash prefix
            file_pattern = r"- `([^`]+)`"
            file_matches = re.finditer(file_pattern, task_content)

            for file_match in file_matches:
                file_path = file_match.group(1)
                # Normalize the path (remove ./ prefix if present)
                file_path = file_path.lstrip("./")
                files.append(file_path)

            if files:
                tasks.append((task_num, task_title, files))

        return tasks

    def find_matching_task(self, file_path: str) -> Optional[TaskMatch]:
        """Find which spec task mentions this file.

        Args:
            file_path: Path to the file being edited.

        Returns:
            TaskMatch if found, None otherwise.
        """
        # Normalize the file path (make relative to project)
        try:
            if os.path.isabs(file_path):
                file_path = os.path.relpath(file_path, self.project_dir)
        except ValueError:
            # Can't make relative path (different drives on Windows)
            return None

        # Remove leading ./ if present
        file_path = file_path.lstrip("./")

        spec_files = self.find_spec_files()

        # Sort by modification time (most recent first)
        # This ensures we return matches from the most recently worked on spec
        spec_files = sorted(spec_files, key=lambda f: f.stat().st_mtime, reverse=True)

        for spec_file in spec_files:
            # Extract spec name from directory
            spec_name = spec_file.parent.name
            tasks = self.parse_task_file(spec_file)

            for task_num, task_title, files in tasks:
                # Check if modified file matches any task file
                for task_file in files:
                    # Normalize task file path
                    task_file = task_file.lstrip("./")

                    # Direct match or suffix match
                    if file_path == task_file or file_path.endswith(task_file):
                        return TaskMatch(spec_name, task_num, task_title)

                    # Also check if task_file is a suffix of file_path
                    # This handles cases where file_path is absolute
                    if task_file and file_path.endswith(task_file):
                        return TaskMatch(spec_name, task_num, task_title)

        return None

    def get_all_spec_names(self) -> List[str]:
        """Get list of all spec names in the project.

        Returns:
            List of spec directory names.
        """
        if not self.specs_dir.exists():
            return []

        spec_names = []
        for spec_dir in self.specs_dir.iterdir():
            if spec_dir.is_dir() and (spec_dir / "tasks.md").exists():
                spec_names.append(spec_dir.name)

        return sorted(spec_names)

    def get_spec_files(self, spec_name: str) -> dict:
        """Get all spec files for a given spec.

        Args:
            spec_name: Name of the spec directory.

        Returns:
            Dictionary mapping file type to path.
        """
        spec_dir = self.specs_dir / spec_name
        files = {}

        if spec_dir.exists():
            for file_type in ["requirements.md", "design.md", "tasks.md"]:
                file_path = spec_dir / file_type
                if file_path.exists():
                    files[file_type.replace(".md", "")] = file_path

        return files
