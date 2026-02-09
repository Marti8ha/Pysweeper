"""Tile model representing a single cell on the Minesweeper board.

Provides a minimal API used by `Board` and `Game`:
- `isMine`, `isRevealed`, `isFlagged`, `neighborCount`
- `reveal()` -> returns True if revealing this tile detonates a mine
- `toggleFlag()` -> toggles flag state
"""

class Tile:
	def __init__(self, row: int, col: int):
		self.row = row
		self.col = col
		self.isMine = False
		self.isRevealed = False
		self.isFlagged = False
		self.neighborCount = 0

	def reveal(self) -> bool:
		"""Reveal the tile.

		Returns True if the tile was a mine (exploded), False otherwise.
		"""
		if self.isRevealed or self.isFlagged:
			return False

		self.isRevealed = True
		return self.isMine

	def toggleFlag(self) -> bool:
		"""Toggle flag state and return the new flag value."""
		if self.isRevealed:
			return self.isFlagged
		self.isFlagged = not self.isFlagged
		return self.isFlagged

	def __repr__(self) -> str:
		return (
			f"Tile(r={self.row},c={self.col},mine={self.isMine},"
			f"rev={self.isRevealed},flag={self.isFlagged},n={self.neighborCount})"
		)
