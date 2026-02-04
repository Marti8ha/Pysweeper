"""Main game controller managing pygame loop, input handling, and state transitions."""


import pygame
import sys
from .state import GameState, Difficulty, Score
from .board import Board
from ui.hud import Hud
from ui.menu import Menu
from ui.leaderboard import LeaderboardUI
from utils.leaderboard_storage import LeaderboardStorage
import settings


class Game:
    """Main game controller handling the pygame event loop and state management."""

    def __init__(self):
        pygame.init()
        self.screen = None
        self.clock = None
        self.state = GameState.MENU
        self.board = None
        self.font = None
        self.hud = None
        self.menu = None
        self.leaderboardUI = None
        # Track current game dimensions for dynamic sizing
        self.currentRows = 0
        self.currentCols = 0
        self.currentTileSize = settings.TILE_SIZE
        self.currentOffsetX = settings.BOARD_OFFSET_X
        self.currentOffsetY = settings.BOARD_OFFSET_Y
        # Scoring tracking
        self.score = 0
        self.currentScoreDisplay = 0
        self.revealedCount = 0
        self.leaderboardStorage = None
        self.lastScoreRank = None
        self._endGameOverlay = False
        self.initDisplay()
        self.running = True
        self.startTime = 0

    def initDisplay(self):
        """Initialize pygame display and clock."""
        pygame.display.set_caption("Pysweeper")
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.clock = pygame.time.Clock()

        try:
            self.font = pygame.font.Font("Cascadia Mono.ttf", 36)
        except (FileNotFoundError, IOError):
            self.font = pygame.font.Font(None, 36)

        self.hud = Hud(0, 0, settings.WIDTH, settings.HUD_HEIGHT, onRestart=self.restartGame)
        self.menu = Menu(onStartGame=self.startGame, onShowLeaderboard=self.showLeaderboard)
        # Initialize leaderboard UI with storage
        self.leaderboardStorage = LeaderboardStorage()
        self.leaderboardUI = LeaderboardUI(self.leaderboardStorage, onBack=self.showMainMenu)

    def resizeWindow(self, rows, cols):
        """Resize window and recalculate positions based on difficulty."""
        # Get optimal dimensions and tile size for this difficulty
        width, height = settings.get_window_dimensions(rows, cols)
        tile_size = settings.get_tile_size(rows, cols)

        # Resize pygame window
        self.screen = pygame.display.set_mode((width, height))

        # Recalculate board offset to center in available space
        offset_x, offset_y = settings.calculate_board_offset(width, height, rows, cols, tile_size)

        # Update tracked dimensions
        self.currentRows = rows
        self.currentCols = cols
        self.currentTileSize = tile_size
        self.currentOffsetX = offset_x
        self.currentOffsetY = offset_y

        # Update HUD with new width
        self.hud = Hud(0, 0, width, settings.HUD_HEIGHT, onRestart=self.restartGame)

        # Update menu and leaderboard button positions
        self.menu.updateButtonPositions(width, height)
        self.leaderboardUI.updateButtonPositions(width, height)

    def run(self):
        """Main game loop running at specified FPS."""
        while self.running:
            self.handleEvents()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def handleEvents(self):
        """Process all pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.hud:
                self.hud.handleEvent(event)

            if self.state == GameState.MENU:
                self.menu.handleEvent(event)
                self.handleMenuEvents(event)
            elif self.state == GameState.PLAYING:
                self.handlePlayingEvents(event)
            elif self.state in (GameState.GAME_OVER, GameState.WIN):
                self.handleEndGameEvents(event)
            elif self.state == GameState.LEADERBOARD:
                self.handleLeaderboardEvents(event)

    def handleMenuEvents(self, event):
        """Handle events in menu state."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False

    def handlePlayingEvents(self, event):
        """Handle events during active gameplay."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handleMouseClick(event)

    def handleEndGameEvents(self, event):
        """Handle events after game ends."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.restartGame()
            elif event.key == pygame.K_ESCAPE:
                self.state = GameState.MENU

    def handleLeaderboardEvents(self, event):
        """Handle events in leaderboard state."""
        self.leaderboardUI.handleEvent(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = GameState.MENU

    def showLeaderboard(self):
        """Switch to leaderboard view."""
        self.leaderboardUI.refresh()
        self.state = GameState.LEADERBOARD

    def showMainMenu(self):
        """Return to main menu."""
        self.state = GameState.MENU

    def handleMouseClick(self, event):
        """Process mouse clicks on the game board."""
        if not self.board:
            return

        boardStartX = self.currentOffsetX
        boardStartY = self.currentOffsetY
        tileSize = self.currentTileSize

        col = (event.pos[0] - boardStartX) // tileSize
        row = (event.pos[1] - boardStartY) // tileSize

        if 0 <= row < self.board.rows and 0 <= col < self.board.cols:
            if event.button == 1:
                self.board.revealTile(row, col)
            elif event.button == 3:
                self.board.toggleFlag(row, col)

    def startGame(self, rows, cols, mines):
        """Initialize a new game with specified difficulty."""
        # Resize window for the selected difficulty
        self.resizeWindow(rows, cols)

        self.board = Board(rows, cols, mines)
        self.state = GameState.PLAYING
        self.startTime = pygame.time.get_ticks()

        # Reset scoring
        self.score = 0
        self.currentScoreDisplay = 0
        self.revealedCount = 0
        self.lastScoreRank = None

    def restartGame(self):
        """Restart the current game with same settings."""
        if self.board:
            self.startGame(self.board.rows, self.board.cols, self.board.mineCount)
        else:
            self.startGame(*Difficulty.MEDIUM)

    def switchState(self, newState):
        """Change the current game state."""
        self.state = newState

    def update(self):
        """Update game state each frame."""
        if self.state == GameState.PLAYING and self.board:
            elapsed = (pygame.time.get_ticks() - self.startTime) // 1000
            self.hud.setTimer(elapsed)
            self.hud.setMineCount(self.board.mineCount - self.board.flagCount)

            # Update score display
            self._updateScore(elapsed)

            # Check for game end
            if self.board.gameState == GameState.GAME_OVER:
                self._endGameOverlay = True
                self._handleGameOver(elapsed)
            elif self.board.gameState == GameState.WIN:
                self._endGameOverlay = True
                self._handleWin(elapsed)

    def _updateScore(self, elapsed):
        """Update the current score based on tiles revealed.

        Args:
            elapsed: Current elapsed time in seconds.
        """
        if not self.board:
            return

        # Count revealed tiles
        revealed = 0
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                if self.board.getTile(r, c).isRevealed:
                    revealed += 1

        # Calculate score
        self._calculateScore(revealed, elapsed)

    def _calculateScore(self, revealed, elapsed):
        """Calculate the score based on game progress.

        Args:
            revealed: Number of tiles revealed.
            elapsed: Time elapsed in seconds.
        """
        if revealed <= self.revealedCount:
            return

        # Find difficulty tuple
        difficulty = (self.board.rows, self.board.cols, self.board.mineCount)
        multiplier = Difficulty.MULTIPLIERS.get(difficulty, 1.0)

        # Base points per tile
        basePoints = revealed * settings.POINTS_BASE_PER_TILE

        # Time bonus: max(0, 1000 - seconds_elapsed)
        timeBonus = max(0, settings.POINTS_TIME_BONUS_MAX - elapsed)

        # No flags bonus (if no flags used)
        flagsUsed = self.board.flagCount
        noFlagsBonus = settings.POINTS_NO_FLAGS_BONUS if flagsUsed == 0 else 0

        # Calculate total: base * multiplier * noHintsMultiplier + time bonus + no flags bonus
        self.score = int(basePoints * multiplier * settings.POINTS_NO_HINTS_MULTIPLIER)
        self.score += timeBonus + noFlagsBonus

        self.revealedCount = revealed

    def _handleGameOver(self, elapsed):
        """Handle game over state.

        Args:
            elapsed: Time elapsed in seconds.
        """
        self._saveScore(elapsed, gameWon=False)

    def _handleWin(self, elapsed):
        """Handle win state - calculate and save final score.

        Args:
            elapsed: Time elapsed in seconds.
        """
        # Recalculate score with final revealed count
        totalTiles = (self.board.rows * self.board.cols) - self.board.mineCount
        self._calculateScore(totalTiles, elapsed)

        self._saveScore(elapsed, gameWon=True)

    def _saveScore(self, elapsed, gameWon):
        """Save the score to leaderboard.

        Args:
            elapsed: Time elapsed in seconds.
            gameWon: Whether the game was won.
        """
        difficulty = (self.board.rows, self.board.cols, self.board.mineCount)
        flagsUsed = self.board.flagCount

        score = Score(
            score=self.score,
            difficulty=difficulty,
            timeElapsed=elapsed,
            hintsUsed=False,  # No hints system yet
            flagsUsed=flagsUsed,
        )

        # Save to leaderboard
        self.lastScoreRank = self.leaderboardStorage.addScore(score.toDict())

    def draw(self):
        """Render current game state to screen."""
        self.screen.fill(settings.COLORS["background"])

        if self.hud:
            self.hud.draw(self.screen)

        if self.state == GameState.MENU:
            self.menu.draw(self.screen)
        elif self.state == GameState.PLAYING:
            self.drawGame()
            self.drawScoreDisplay()
        elif self.state in (GameState.GAME_OVER, GameState.WIN):
            self.drawGame()
            self.drawEndGameOverlay()
        elif self.state == GameState.LEADERBOARD:
            self.leaderboardUI.draw(self.screen)

        pygame.display.flip()

    def drawScoreDisplay(self):
        """Draw the current score on the screen."""
        scoreText = self.font.render(f"Score: {self.score:,}", True, settings.COLORS["accent"])
        scoreRect = scoreText.get_rect(topright=(self.screen.get_width() - 20, settings.HUD_HEIGHT + 10))
        self.screen.blit(scoreText, scoreRect)

    def drawGame(self):
        """Render the game board."""
        if self.board:
            for r in range(self.board.rows):
                for c in range(self.board.cols):
                    self.drawTile(r, c)

    def drawTile(self, row, col):
        """Draw a single tile at grid position."""
        tile = self.board.getTile(row, col)
        x = self.currentOffsetX + col * self.currentTileSize
        y = self.currentOffsetY + row * self.currentTileSize
        size = self.currentTileSize - 2

        if tile.isRevealed:
            pygame.draw.rect(self.screen, settings.COLORS["tile_revealed"], (x, y, size, size))
            pygame.draw.rect(self.screen, settings.COLORS["tile_border_dark"], (x, y, size, size), 1)

            if tile.isMine:
                text = self.font.render("M", True, settings.COLORS["mine"])
                textRect = text.get_rect(center=(x + size // 2, y + size // 2))
                self.screen.blit(text, textRect)
            elif tile.neighborCount > 0:
                color = settings.NUMBER_COLORS.get(tile.neighborCount, settings.COLORS["text_primary"])
                text = self.font.render(str(tile.neighborCount), True, color)
                textRect = text.get_rect(center=(x + size // 2, y + size // 2))
                self.screen.blit(text, textRect)
        else:
            pygame.draw.rect(self.screen, settings.COLORS["tile_unrevealed"], (x, y, size, size))

            pygame.draw.line(self.screen, settings.COLORS["tile_border_light"],
                           (x, y), (x + size, y), 2)
            pygame.draw.line(self.screen, settings.COLORS["tile_border_light"],
                           (x, y), (x, y + size), 2)

            pygame.draw.line(self.screen, settings.COLORS["tile_border_dark"],
                           (x + size, y + size), (x + size, y), 2)
            pygame.draw.line(self.screen, settings.COLORS["tile_border_dark"],
                           (x + size, y + size), (x, y + size), 2)

            if tile.isFlagged:
                text = self.font.render("F", True, settings.COLORS["flag"])
                textRect = text.get_rect(center=(x + size // 2, y + size // 2))
                self.screen.blit(text, textRect)

    def drawEndGameOverlay(self):
        """Draw game over or win message with score and rank."""
        overlayWidth = 400
        overlayHeight = 200
        overlay = pygame.Surface((overlayWidth, overlayHeight), pygame.SRCALPHA)
        overlay.fill(settings.COLORS["overlay_background"])

        pygame.draw.rect(overlay, settings.COLORS["overlay_border"],
                        overlay.get_rect(), 2)

        # Main message
        msg = "YOU WIN!" if self.state == GameState.WIN else "GAME OVER"
        color = settings.COLORS["win"] if self.state == GameState.WIN else settings.COLORS["lose"]
        text = self.font.render(msg, True, color)
        textRect = text.get_rect(center=(overlayWidth // 2, 40))
        overlay.blit(text, textRect)

        # Score display
        scoreText = pygame.font.Font(None, 28).render(f"Final Score: {self.score:,}", True, settings.COLORS["accent"])
        scoreRect = scoreText.get_rect(center=(overlayWidth // 2, 80))
        overlay.blit(scoreText, scoreRect)

        # Rank (if on leaderboard)
        if self.lastScoreRank and self.lastScoreRank > 0 and self.lastScoreRank <= settings.LEADERBOARD_MAX_ENTRIES:
            rankText = pygame.font.Font(None, 24).render(f"Rank: #{self.lastScoreRank}", True, settings.COLORS["text_secondary"])
            rankRect = rankText.get_rect(center=(overlayWidth // 2, 110))
            overlay.blit(rankText, rankRect)
        elif self.lastScoreRank == -1:
            # Not in top 10
            rankText = pygame.font.Font(None, 24).render("Score saved!", True, settings.COLORS["text_secondary"])
            rankRect = rankText.get_rect(center=(overlayWidth // 2, 110))
            overlay.blit(rankText, rankRect)

        # Restart instruction
        restartText = pygame.font.Font(None, 24).render("Press R to Restart", True, settings.COLORS["text_secondary"])
        restartRect = restartText.get_rect(center=(overlayWidth // 2, 150))
        overlay.blit(restartText, restartRect)

        # Menu instruction
        menuText = pygame.font.Font(None, 20).render("Press ESC for Menu", True, settings.COLORS["text_secondary"])
        menuRect = menuText.get_rect(center=(overlayWidth // 2, 175))
        overlay.blit(menuText, menuRect)

        overlayX = (self.screen.get_width() - overlayWidth) // 2
        overlayY = (self.screen.get_height() - overlayHeight) // 2
        self.screen.blit(overlay, (overlayX, overlayY))
