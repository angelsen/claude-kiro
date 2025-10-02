"""Session tracking for Claude Kiro hooks.

Tracks which files have been processed in a session to prevent duplicate notifications.
"""

import time
from typing import Dict, Any, Optional
from pathlib import Path

from claude_kiro.hooks._shared.cache_manager import CacheManager


class FileNotificationRecord:
    """Record of a file notification in a session."""

    def __init__(
        self,
        timestamp: float,
        in_spec: bool,
        spec_name: Optional[str] = None,
        task_num: Optional[str] = None,
        context: Optional[str] = None,
    ):
        """Initialize notification record.

        Args:
            timestamp: Unix timestamp of notification.
            in_spec: Whether file is part of a spec.
            spec_name: Name of the spec if applicable.
            task_num: Task number if applicable.
            context: Additional context (e.g., "formatter", "linter").
        """
        self.timestamp = timestamp
        self.in_spec = in_spec
        self.spec_name = spec_name
        self.task_num = task_num
        self.context = context

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "timestamp": self.timestamp,
            "in_spec": self.in_spec,
            "spec_name": self.spec_name,
            "task_num": self.task_num,
            "context": self.context,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FileNotificationRecord":
        """Create from dictionary."""
        return cls(
            timestamp=data.get("timestamp", time.time()),
            in_spec=data.get("in_spec", False),
            spec_name=data.get("spec_name"),
            task_num=data.get("task_num"),
            context=data.get("context"),
        )


class SessionTracker:
    """Tracks notifications within a Claude Code session."""

    def __init__(self, session_id: str, cache_manager: Optional[CacheManager] = None):
        """Initialize session tracker.

        Args:
            session_id: Unique session identifier from Claude Code.
            cache_manager: Optional cache manager. Creates default if not provided.
        """
        self.session_id = session_id or "unknown"
        self.cache_manager = cache_manager or CacheManager()
        self._cache_key = f"session_{self.session_id}"
        self._cache = None
        self._load_cache()

    def _load_cache(self):
        """Load session cache from disk."""
        cache_data = self.cache_manager.load(self._cache_key)

        if cache_data:
            # Convert file notification dicts back to objects
            files_notified = {}
            for file_path, record_data in cache_data.get("files_notified", {}).items():
                if isinstance(record_data, dict):
                    files_notified[file_path] = record_data
                else:
                    # Handle old format or corrupted data
                    files_notified[file_path] = {
                        "timestamp": time.time(),
                        "in_spec": False,
                    }

            self._cache = {
                "session_id": self.session_id,
                "session_start": cache_data.get("session_start", time.time()),
                "files_notified": files_notified,
            }
        else:
            # Initialize new cache
            self._cache = {
                "session_id": self.session_id,
                "session_start": time.time(),
                "files_notified": {},
            }

    def _save_cache(self):
        """Save session cache to disk."""
        if self._cache:
            self.cache_manager.save(self._cache_key, self._cache)

    def has_notified(self, file_path: str, context: Optional[str] = None) -> bool:
        """Check if we've already notified about this file.

        Args:
            file_path: Path to the file.
            context: Optional context to check separately (e.g., "formatter").

        Returns:
            True if already notified, False otherwise.
        """
        if not self._cache:
            return False

        # Normalize file path
        file_path = str(Path(file_path))

        # Check if file has been notified
        if file_path not in self._cache["files_notified"]:
            return False

        # If context specified, check if this specific context was notified
        if context:
            record = self._cache["files_notified"][file_path]
            return record.get("context") == context

        return True

    def mark_notified(
        self,
        file_path: str,
        in_spec: bool = False,
        spec_name: Optional[str] = None,
        task_num: Optional[str] = None,
        context: Optional[str] = None,
    ):
        """Mark a file as notified in this session.

        Args:
            file_path: Path to the file.
            in_spec: Whether file is part of a spec.
            spec_name: Name of the spec if applicable.
            task_num: Task number if applicable.
            context: Additional context (e.g., "formatter", "linter").
        """
        if not self._cache:
            self._load_cache()

        # Normalize file path
        file_path = str(Path(file_path))

        # Create notification record
        record = FileNotificationRecord(
            timestamp=time.time(),
            in_spec=in_spec,
            spec_name=spec_name,
            task_num=task_num,
            context=context,
        )

        # Store in cache
        self._cache["files_notified"][file_path] = record.to_dict()

        # Save to disk
        self._save_cache()

    def get_notification_count(self) -> int:
        """Get total number of files notified in this session.

        Returns:
            Number of unique files notified.
        """
        if not self._cache:
            return 0
        return len(self._cache.get("files_notified", {}))

    def cleanup_old_sessions(self, current_session_id: Optional[str] = None):
        """Clean up old session cache files.

        Args:
            current_session_id: Optional current session to preserve.
        """
        # Use cache manager's cleanup, but preserve current session
        if current_session_id and current_session_id == self.session_id:
            # Don't clean up our own session
            pass
        else:
            self.cache_manager.cleanup_expired()

    def get_session_age(self) -> float:
        """Get age of current session in seconds.

        Returns:
            Session age in seconds.
        """
        if not self._cache:
            return 0.0
        return time.time() - self._cache.get("session_start", time.time())

    def clear(self):
        """Clear all notifications for this session."""
        if self._cache:
            self._cache["files_notified"] = {}
            self._save_cache()
