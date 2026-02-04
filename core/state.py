"""Game state constants and score tracking for clean state machine transitions."""


class GameState:
    """Enumeration of possible game states."""

    MENU = 0
    PLAYING = 1
    GAME_OVER = 2
    WIN = 3
    LEADERBOARD = 4  # New state for leaderboard view


class Difficulty:
    """Difficulty presets for game configuration."""

    EASY = (9, 9, 10)      # rows, cols, mines
    MEDIUM = (16, 16, 40)  # rows, cols, mines
    HARD = (16, 30, 99)    # rows, cols, mines

    # Difficulty name mapping
    NAMES = {
        EASY: "Easy",
        MEDIUM: "Medium",
        HARD: "Hard",
    }

    # Score multipliers
    MULTIPLIERS = {
        EASY: 1.0,
        MEDIUM: 1.5,
        HARD: 2.0,
    }


class Score:
    """Represents a completed game score with all relevant metadata."""

    def __init__(self, score, difficulty, timeElapsed, date=None, hintsUsed=True, flagsUsed=0):
        """Initialize a score entry.

        Args:
            score: Total points earned
            difficulty: Tuple (rows, cols, mines) identifying difficulty
            timeElapsed: Seconds taken to complete the game
            date: ISO format date string (defaults to current time)
            hintsUsed: Whether hints were used during gameplay
            flagsUsed: Number of flags placed during the game
        """
        self.score = score
        self.difficulty = difficulty
        self.timeElapsed = timeElapsed
        self.date = date or self._getCurrentDate()
        self.hintsUsed = hintsUsed
        self.flagsUsed = flagsUsed

    def _getCurrentDate(self):
        """Get current date in ISO format."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M")

    def toDict(self):
        """Convert score to dictionary for JSON serialization."""
        return {
            "score": self.score,
            "difficulty": Difficulty.NAMES.get(self.difficulty, "Unknown"),
            "date": self.date,
            "time_elapsed": self.timeElapsed,
            "hints_used": self.hintsUsed,
            "flags_used": self.flagsUsed,
        }

    @classmethod
    def fromDict(cls, data):
        """Create Score from dictionary (for loading from JSON)."""
        # Find difficulty tuple from name
        difficulty = Difficulty.MEDIUM  # Default
        for diff, name in Difficulty.NAMES.items():
            if name == data.get("difficulty", ""):
                difficulty = diff
                break

        return cls(
            score=data.get("score", 0),
            difficulty=difficulty,
            timeElapsed=data.get("time_elapsed", 0),
            date=data.get("date"),
            hintsUsed=data.get("hints_used", True),
            flagsUsed=data.get("flags_used", 0),
        )

    def getDifficultyName(self):
        """Get human-readable difficulty name."""
        return Difficulty.NAMES.get(self.difficulty, "Unknown")

    def getMultiplier(self):
        """Get the score multiplier for this difficulty."""
        return Difficulty.MULTIPLIERS.get(self.difficulty, 1.0)
