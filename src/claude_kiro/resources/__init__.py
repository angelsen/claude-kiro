"""Resource loader for bundled Claude Kiro templates and configuration files."""

from importlib import resources
from typing import List


class ResourceLoader:
    """Load bundled resources from the Claude Kiro package.

    Resources are stored in the package and accessed using importlib.resources
    for compatibility with different installation methods (pip, uv, editable).
    """

    def __init__(self):
        """Initialize the resource loader."""
        self._package = "claude_kiro.resources.templates"

    def get_resource(self, path: str) -> str:
        """Load resource content by path.

        Args:
            path: Resource path relative to templates directory
                  e.g., "claude_md.md", "output_styles/spec_driven.md"

        Returns:
            Resource content as string

        Raises:
            FileNotFoundError: If resource does not exist
            IOError: If resource cannot be read
        """
        try:
            # Handle nested paths
            if "/" in path:
                parts = path.split("/")
                # Convert path like "output_styles/spec_driven.md" to package notation
                package_parts = parts[:-1]
                filename = parts[-1]

                # Replace underscores in filenames for Python module compatibility
                package_suffix = ".".join(package_parts)
                full_package = (
                    f"{self._package}.{package_suffix}"
                    if package_suffix
                    else self._package
                )
            else:
                full_package = self._package
                filename = path

            # Use importlib.resources to read the file
            return resources.read_text(full_package, filename)

        except (FileNotFoundError, ModuleNotFoundError) as e:
            raise FileNotFoundError(f"Resource not found: {path}") from e
        except Exception as e:
            raise IOError(f"Failed to read resource {path}: {e}") from e

    def list_resources(self) -> List[str]:
        """List all available resources.

        Returns:
            List of resource paths
        """
        resources_list = []

        # Walk through the templates package
        try:
            # List resources in main templates directory
            for resource in resources.contents(self._package):
                if resource.endswith(".md"):
                    resources_list.append(resource)

            # Check subdirectories
            subdirs = ["output_styles", "commands", "commands.spec"]
            for subdir in subdirs:
                try:
                    subpackage = f"{self._package}.{subdir.replace('/', '.')}"
                    for resource in resources.contents(subpackage):
                        if resource.endswith(".md"):
                            resources_list.append(f"{subdir}/{resource}")
                except (FileNotFoundError, ModuleNotFoundError):
                    # Subdirectory doesn't exist or isn't a package
                    pass

        except Exception:
            # Return empty list if we can't enumerate resources
            pass

        return sorted(resources_list)
