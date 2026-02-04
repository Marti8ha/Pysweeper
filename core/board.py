"""Manages the Minesweeper game board, mine placement, and game rules."""


import random
from .tile import Tile
from .state import GameState


class Board:
    """Game board managing grid state, mine operations, and win/loss conditions."""

    def __init__(self, rows, cols, mineCount):
        self.rows = rows
        self.cols = cols
        self.mineCount = mineCount
        self.tiles = []
        self.gameState = GameState.PLAYING
        self.firstClick = True
        self.initTiles()
        self.flagCount = 0

    def initTiles(self):
        """Create empty grid of Tile objects."""
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                row.append(Tile(r, c))
            self.tiles.append(row)

    def placeMines(self, excludeRow, excludeCol):
        """Randomly place mines avoiding the first clicked tile."""
        safeZone = {excludeRow, excludeRow - 1, excludeRow + 1}
        safeColZone = {excludeCol, excludeCol - 1, excludeCol + 1}

        minesPlaced = 0
        while minesPlaced < self.mineCount:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)

            if (r in safeZone or r in safeColZone) and (c in safeColZone or c in safeZone):
                continue

            if not self.tiles[r][c].isMine:
                self.tiles[r][c].isMine = True
                minesPlaced += 1

        self.calculateAllNeighbors()

    def calculateAllNeighbors(self):
        """Pre-calculate neighbor counts for all tiles."""
        for r in range(self.rows):
            for c in range(self.cols):
                if not self.tiles[r][c].isMine:
                    self.tiles[r][c].neighborCount = self.countNeighbors(r, c)

    def countNeighbors(self, row, col):
        """Count mines in 8 adjacent cells."""
        count = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if self.isValid(nr, nc) and self.tiles[nr][nc].isMine:
                    count += 1
        return count

    def isValid(self, row, col):
        """Check if coordinates are within board boundaries."""
        return 0 <= row < self.rows and 0 <= col < self.cols

    def revealTile(self, row, col):
        """Reveal a tile and handle flood fill for empty cells."""
        if not self.isValid(row, col):
            return

        tile = self.tiles[row][col]
        if tile.isRevealed or tile.isFlagged or self.gameState != GameState.PLAYING:
            return

        if self.firstClick:
            self.placeMines(row, col)
            self.firstClick = False

        if tile.reveal():
            self.gameState = GameState.GAME_OVER
            self.revealAllMines()
            return

        if tile.neighborCount == 0:
            self.floodFill(row, col)

        self.checkWinCondition()

    def floodFill(self, row, col):
        """Recursively reveal adjacent empty tiles."""
        stack = [(row, col)]
        while stack:
            r, c = stack.pop()
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if self.isValid(nr, nc):
                        tile = self.tiles[nr][nc]
                        if not tile.isRevealed and not tile.isFlagged:
                            tile.reveal()
                            if tile.neighborCount == 0:
                                stack.append((nr, nc))

    def toggleFlag(self, row, col):
        """Toggle flag state on a tile."""
        if not self.isValid(row, col):
            return

        tile = self.tiles[row][col]
        if tile.isRevealed:
            return

        wasFlagged = tile.isFlagged
        tile.toggleFlag()
        self.flagCount += 1 if not wasFlagged else -1

    def revealAllMines(self):
        """Show all mine locations on game over."""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.tiles[r][c].isMine:
                    self.tiles[r][c].isRevealed = True

    def checkWinCondition(self):
        """Check if player has revealed all non-mine tiles."""
        for r in range(self.rows):
            for c in range(self.cols):
                tile = self.tiles[r][c]
                if not tile.isMine and not tile.isRevealed:
                    return
        self.gameState = GameState.WIN

    def getTile(self, row, col):
        """Return tile at specified coordinates."""
        if self.isValid(row, col):
            return self.tiles[row][col]
        return None

    def getRemainingCells(self):
        """Calculate unrevealed non-mine cells remaining."""
        count = 0
        for r in range(self.rows):
            for c in range(self.cols):
                tile = self.tiles[r][c]
                if not tile.isMine and not tile.isRevealed:
                    count += 1
        return count

    def reset(self, rows, cols, mineCount):
        """Reset board with new dimensions."""
        self.rows = rows
        self.cols = cols
        self.mineCount = mineCount
        self.tiles = []
        self.gameState = GameState.PLAYING
        self.firstClick = True
        self.flagCount = 0
        self.initTiles()
