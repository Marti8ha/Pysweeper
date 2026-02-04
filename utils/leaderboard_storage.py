"""JSON persistence for the leaderboard system."""

import json
import os
from pathlib import Path


# Default leaderboard file location
DEFAULT_LEADERBOARD_PATH = Path.home() / ".pysweeper" / "leaderboard.json"


class LeaderboardStorage:
    """Handles loading and saving leaderboard data to JSON file."""

    def __init__(self, filePath=None):
        """Initialize storage with optional custom file path.

        Args:
            filePath: Optional custom path for the leaderboard JSON file.
                      Defaults to ~/.pysweeper/leaderboard.json
        """
        self.filePath = Path(filePath) if filePath else DEFAULT_LEADERBOARD_PATH
        self._ensureDirectory()

    def _ensureDirectory(self):
        """Create parent directory if it doesn't exist."""
        self.filePath.parent.mkdir(parents=True, exist_ok=True)

    def load(self):
        """Load leaderboard entries from JSON file.

        Returns:
            List of score dictionaries sorted by score (highest first).
            Returns empty list if file doesn't exist or is corrupted.
        """
        if not self.filePath.exists():
            return []

        try:
            with open(self.filePath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return sorted(data, key=lambda x: x.get('score', 0), reverse=True)
                return []
        except (json.JSONDecodeError, IOError, OSError):
            return []

    def save(self, entries):
        """Save leaderboard entries to JSON file.

        Args:
            entries: List of score dictionaries to save.
                     Only top entries will be kept (based on config).
        """
        self._ensureDirectory()

        try:
            with open(self.filePath, 'w', encoding='utf-8') as f:
                json.dump(entries, f, indent=2, ensure_ascii=False)
        except (IOError, OSError):
            pass  # Silently fail on write errors

    def addScore(self, scoreEntry):
        """Add a new score entry and maintain top entries limit.

        Args:
            scoreEntry: Dictionary containing score data with keys:
                        - score: int (required)
                        - difficulty: str (required)
                        - date: str in ISO format (required)
                        - time_elapsed: int seconds (required)

        Returns:
            int: The rank of the new score (1-indexed), or -1 if not in top 10.
        """
        entries = self.load()

        # Add new entry
        entries.append(scoreEntry)

        # Sort by score descending
        entries = sorted(entries, key=lambda x: x.get('score', 0), reverse=True)

        # Find rank of new entry
        rank = -1
        for i, entry in enumerate(entries):
            if entry == scoreEntry and rank == -1:
                rank = i + 1
                break

        # Keep only top entries
        maxEntries = 10
        entries = entries[:maxEntries]

        self.save(entries)

        return rank if rank <= maxEntries else -1

    def getTopScores(self, limit=10):
        """Retrieve top scores from the leaderboard.

        Args:
            limit: Maximum number of entries to return.

        Returns:
            List of score dictionaries sorted by score (highest first).
        """
        entries = self.load()
        return entries[:limit]

    def clear(self):
        """Clear all leaderboard entries."""
        self._ensureDirectory()
        self.save([])
