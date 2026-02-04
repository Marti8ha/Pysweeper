"""Game state constants for clean state machine transitions."""


class GameState:
    """Enumeration of possible game states."""

    MENU = 0
    PLAYING = 1
    GAME_OVER = 2
    WIN = 3


class Difficulty:
    """Difficulty presets for game configuration."""

    EASY = (9, 9, 10)      # rows, cols, mines
    MEDIUM = (16, 16, 40)  # rows, cols, mines
    HARD = (16, 30, 99)    # rows, cols, mines
