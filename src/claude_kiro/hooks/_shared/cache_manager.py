"""Cache management for Claude Kiro hooks.

Provides temp file operations with TTL (time-to-live) enforcement
for session-based caching.
"""

import json
import os
import time
from pathlib import Path
import tempfile
from typing import Dict, Any, Optional


class CacheManager:
    """Manages temporary cache files with TTL enforcement."""

    def __init__(self, cache_dir: Optional[Path] = None, ttl_seconds: int = 86400):
        """Initialize cache manager.

        Args:
            cache_dir: Directory for cache files. Defaults to system temp.
            ttl_seconds: Time-to-live in seconds. Default 24 hours.
        """
        if cache_dir is None:
            cache_dir = Path(tempfile.gettempdir()) / "claude-kiro-hooks"
        self.cache_dir = Path(cache_dir)
        self.ttl_seconds = ttl_seconds
        self.cache_dir.mkdir(exist_ok=True, parents=True)

    def get_cache_path(self, cache_key: str) -> Path:
        """Get the full path for a cache file.

        Args:
            cache_key: Unique identifier for the cache file.

        Returns:
            Full path to the cache file.
        """
        # Sanitize cache key to prevent path traversal
        safe_key = "".join(
            c if c.isalnum() or c in ("_", "-", ".") else "_" for c in cache_key
        )
        return self.cache_dir / f"{safe_key}.json"

    def load(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Load cache data from file.

        Args:
            cache_key: Unique identifier for the cache file.

        Returns:
            Cache data as dictionary, or None if not found/expired.
        """
        cache_path = self.get_cache_path(cache_key)

        if not cache_path.exists():
            return None

        try:
            # Check if file is expired
            file_age = time.time() - cache_path.stat().st_mtime
            if file_age > self.ttl_seconds:
                # File is expired, delete it
                cache_path.unlink()
                return None

            with open(cache_path, "r") as f:
                return json.load(f)

        except (json.JSONDecodeError, OSError, IOError):
            # Corrupted or inaccessible cache file
            try:
                cache_path.unlink()
            except (OSError, IOError):
                pass
            return None

    def save(self, cache_key: str, data: Dict[str, Any]) -> bool:
        """Save cache data to file.

        Args:
            cache_key: Unique identifier for the cache file.
            data: Data to cache.

        Returns:
            True if successful, False otherwise.
        """
        cache_path = self.get_cache_path(cache_key)

        try:
            # Write to temp file first, then rename (atomic operation)
            temp_path = cache_path.with_suffix(".tmp")
            with open(temp_path, "w") as f:
                json.dump(data, f, indent=2)

            # Set restrictive permissions (user read/write only)
            os.chmod(temp_path, 0o600)

            # Atomic rename
            temp_path.replace(cache_path)
            return True

        except (OSError, IOError):
            # Failed to write cache - not critical
            return False

    def delete(self, cache_key: str) -> bool:
        """Delete a specific cache file.

        Args:
            cache_key: Unique identifier for the cache file.

        Returns:
            True if deleted, False if not found or error.
        """
        cache_path = self.get_cache_path(cache_key)

        try:
            if cache_path.exists():
                cache_path.unlink()
                return True
            return False
        except (OSError, IOError):
            return False

    def cleanup_expired(self) -> int:
        """Remove all expired cache files.

        Returns:
            Number of files cleaned up.
        """
        if not self.cache_dir.exists():
            return 0

        current_time = time.time()
        cleaned = 0

        try:
            for cache_file in self.cache_dir.glob("*.json"):
                try:
                    file_age = current_time - cache_file.stat().st_mtime
                    if file_age > self.ttl_seconds:
                        cache_file.unlink()
                        cleaned += 1
                except (OSError, IOError):
                    # Skip files we can't process
                    continue

        except (OSError, IOError):
            # Can't access directory
            pass

        return cleaned

    def get_cache_size(self) -> float:
        """Get total size of cache directory in MB.

        Returns:
            Total size in megabytes.
        """
        if not self.cache_dir.exists():
            return 0.0

        total_size = 0
        try:
            for cache_file in self.cache_dir.glob("*.json"):
                try:
                    total_size += cache_file.stat().st_size
                except (OSError, IOError):
                    continue
        except (OSError, IOError):
            pass

        return total_size / (1024 * 1024)  # Convert to MB
