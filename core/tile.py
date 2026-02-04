"""Represents a single cell on the Minesweeper board."""


class Tile:
    """Individual game tile with mine status and visibility state."""

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.isMine = False
        self.isRevealed = False
        self.isFlagged = False
        self.neighborCount = 0

    def reveal(self):
        """Mark tile as revealed. Returns True if tile contains a mine."""
        if self.isRevealed or self.isFlagged:
            return False
        self.isRevealed = True
        return self.isMine

    def toggleFlag(self):
        """Toggle flag state. Returns new flag state."""
        if not self.isRevealed:
            self.isFlagged = not self.isFlagged
        return self.isFlagged

    def __repr__(self):
        if self.isFlagged:
            return "F"
        if not self.isRevealed:
            return "■"
        if self.isMine:
            return "M"
        if self.neighborCount == 0:
            return " "
        return str(self.neighborCount)
