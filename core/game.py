"""Main game controller managing pygame loop, input handling, and state transitions."""


import pygame
import sys
from .state import GameState, Difficulty, Score
from .board import Board
from ui.hud import Hud
from ui.menu import Menu
from ui.leaderboard import LeaderboardUI
from utils.leaderboard_storage import LeaderboardStorage
from ui.pixel_utils import draw_pixel_text, draw_pixel_mine, draw_pixel_flag
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
        # Make window resizable
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        # Use pixel font for score display
        self.font = None  # Using draw_pixel_text instead

        self.hud = Hud(0, 0, settings.WIDTH, settings.HUD_HEIGHT, onRestart=self.restartGame, onMenu=self.showMainMenu)
        self.menu = Menu(onStartGame=self.startGame, onShowLeaderboard=self.showLeaderboard)
        # Initialize leaderboard UI with storage
        self.leaderboardStorage = LeaderboardStorage()
        self.leaderboardUI = LeaderboardUI(self.leaderboardStorage, onBack=self.showMainMenu)

    def resizeWindow(self, rows, cols):
        """Resize window and recalculate positions based on difficulty."""
        # Get optimal dimensions and tile size for this difficulty
        width, height = settings.get_window_dimensions(rows, cols)
        tile_size = settings.get_tile_size(rows, cols)

        # Resize pygame window (keep resizable flag)
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

        # Recalculate board offset to center in available space
        offset_x, offset_y = settings.calculate_board_offset(width, height, rows, cols, tile_size)

        # Update tracked dimensions
        self.currentRows = rows
        self.currentCols = cols
        self.currentTileSize = tile_size
        self.currentOffsetX = offset_x
        self.currentOffsetY = offset_y

        # Update HUD with new width
        self.hud = Hud(0, 0, width, settings.HUD_HEIGHT, onRestart=self.restartGame, onMenu=self.showMainMenu)

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

            elif event.type == pygame.VIDEORESIZE:
                # Handle window resize event
                self._handleWindowResize(event.w, event.h)

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

    def _handleWindowResize(self, new_width, new_height):
        """Handle window resize by recalculating positions and scaling.
        
        Args:
            new_width: New window width
            new_height: New window height
        """
        # Resize the window
        self.screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
        
        # Recalculate board scaling if in game
        if self.board and self.state in (GameState.PLAYING, GameState.GAME_OVER, GameState.WIN):
            # Calculate optimal tile size to fit board in window
            available_width = new_width - 2 * settings.BOARD_PADDING
            available_height = new_height - settings.HUD_HEIGHT - 2 * settings.BOARD_PADDING
            
            # Calculate tile size to fit board within available space
            tile_width = available_width // self.board.cols
            tile_height = available_height // self.board.rows
            self.currentTileSize = max(20, min(tile_width, tile_height))  # Min 20px, max calculated
            
            # Recalculate board offset to center it
            board_width = self.board.cols * self.currentTileSize
            board_height = self.board.rows * self.currentTileSize
            self.currentOffsetX = (new_width - board_width) // 2
            available_game_height = new_height - settings.HUD_HEIGHT - settings.BOARD_PADDING
            self.currentOffsetY = settings.HUD_HEIGHT + settings.BOARD_PADDING + (available_game_height - board_height) // 2
        
        # Update HUD width
        if self.hud:
            self.hud.rect.width = new_width
            self.hud.rect.height = settings.HUD_HEIGHT
            # Update menu button position
            self.hud.menuButton.x = new_width - 80
        
        # Update menu button positions
        if self.menu:
            self.menu.updateButtonPositions(new_width, new_height)
        
        # Update leaderboard button positions
        if self.leaderboardUI:
            self.leaderboardUI.updateButtonPositions(new_width, new_height)

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

        # Optional: Draw scanline overlay for retro feel
        # self._draw_scanlines()

        pygame.display.flip()

    def _draw_scanlines(self):
        """Draw subtle scanline overlay for retro CRT effect."""
        line_color = (0, 0, 0)
        line_height = 1
        gap = 3
        width = self.screen.get_width()
        height = self.screen.get_height()
        
        for y in range(0, height, line_height + gap):
            pygame.draw.line(self.screen, line_color, (0, y), (width, y), line_height)

    def drawScoreDisplay(self):
        """Draw the current score on the screen."""
        score_str = f"Score: {self.score:,}"
        score_x = self.screen.get_width() - 20 - len(score_str) * 16
        draw_pixel_text(self.screen, score_str, score_x, settings.HUD_HEIGHT + 10,
                       settings.COLORS["accent"], size='medium')

    def drawGame(self):
        """Render the game board."""
        if self.board:
            for r in range(self.board.rows):
                for c in range(self.board.cols):
                    self.drawTile(r, c)

    def drawTile(self, row, col):
        """Draw a single tile at grid position with pixel art style."""
        tile = self.board.getTile(row, col)
        x = self.currentOffsetX + col * self.currentTileSize
        y = self.currentOffsetY + row * self.currentTileSize
        size = self.currentTileSize - 2
        bevel_size = 2

        if tile.isRevealed:
            # Draw revealed tile - flat with pixel border
            pygame.draw.rect(
                self.screen,
                settings.COLORS["tile_revealed"],
                (x, y, size, size)
            )
            # Sharp pixel border for revealed tiles
            pygame.draw.rect(
                self.screen,
                settings.COLORS["tile_border_dark"],
                (x, y, size, size),
                1
            )

            if tile.isMine:
                # Pixel art style mine - blocky representation
                self._draw_pixel_mine(x, y, size)
            elif tile.neighborCount > 0:
                color = settings.NUMBER_COLORS.get(tile.neighborCount, settings.COLORS["text_primary"])
                # Use true pixel art text for numbers
                num_str = str(tile.neighborCount)
                num_x = x + size // 2 - len(num_str) * 8
                num_y = y + size // 2 - 7
                draw_pixel_text(self.screen, num_str, num_x, num_y, color, size='medium')
        else:
            # Draw unrevealed tile with pixel-style 3D bevel effect
            self._draw_bevel_tile(x, y, size, bevel_size, tile.isFlagged)

    def _draw_bevel_tile(self, x, y, size, bevel_size, is_flagged):
        """Draw an unrevealed tile with pixel-style raised bevel effect."""
        base_color = settings.COLORS["tile_unrevealed"]
        
        # Light color for top-left bevel
        light_color = (
            min(255, base_color[0] + 30),
            min(255, base_color[1] + 30),
            min(255, base_color[2] + 30)
        )
        
        # Dark color for bottom-right bevel
        dark_color = (
            max(0, base_color[0] - 30),
            max(0, base_color[1] - 30),
            max(0, base_color[2] - 30)
        )
        
        # Draw base tile
        pygame.draw.rect(self.screen, base_color, (x + bevel_size, y + bevel_size, 
                                                   size - bevel_size * 2, size - bevel_size * 2))
        
        # Draw top and left bevels (light)
        for i in range(bevel_size):
            pygame.draw.line(self.screen, light_color, 
                           (x + i, y + i), (x + size - 1 - i, y + i))
            pygame.draw.line(self.screen, light_color,
                           (x + i, y + i), (x + i, y + size - 1 - i))
        
        # Draw bottom and right bevels (dark)
        for i in range(bevel_size):
            pygame.draw.line(self.screen, dark_color,
                           (x + i, y + size - 1 - i), (x + size - 1 - i, y + size - 1 - i))
            pygame.draw.line(self.screen, dark_color,
                           (x + size - 1 - i, y + i), (x + size - 1 - i, y + size - 1 - i))
        
        # Draw flag if flagged
        if is_flagged:
            self._draw_pixel_flag(x, y, size)

    def _draw_pixel_mine(self, x, y, size):
        """Draw a pixel art style mine."""
        center_x = x + size // 2
        center_y = y + size // 2
        pixel_size = max(3, size // 8)
        
        # Mine color
        mine_color = settings.COLORS["mine"]
        
        # Draw center body
        body_rect = pygame.Rect(center_x - pixel_size, center_y - pixel_size,
                               pixel_size * 2, pixel_size * 2)
        pygame.draw.rect(self.screen, mine_color, body_rect)
        
        # Draw spikes (cross pattern)
        spike_length = pixel_size * 2
        # Horizontal spike
        pygame.draw.line(self.screen, mine_color,
                        (center_x - spike_length, center_y),
                        (center_x + spike_length, center_y), pixel_size)
        # Vertical spike
        pygame.draw.line(self.screen, mine_color,
                        (center_x, center_y - spike_length),
                        (center_x, center_y + spike_length), pixel_size)
        
        # Diagonal spikes
        diag_offset = int(spike_length * 0.7)
        pygame.draw.line(self.screen, mine_color,
                        (center_x - diag_offset, center_y - diag_offset),
                        (center_x + diag_offset, center_y + diag_offset), pixel_size // 2)
        pygame.draw.line(self.screen, mine_color,
                        (center_x - diag_offset, center_y + diag_offset),
                        (center_x + diag_offset, center_y - diag_offset), pixel_size // 2)

    def _draw_pixel_flag(self, x, y, size):
        """Draw a pixel art style flag."""
        center_x = x + size // 2
        base_y = y + size - 6
        flag_color = settings.COLORS["flag"]
        pole_color = settings.COLORS["text_secondary"]
        
        # Flag pole
        pole_height = size // 2
        pole_width = max(2, size // 12)
        pygame.draw.rect(self.screen, pole_color, 
                        (center_x - pole_width // 2, base_y - pole_height, 
                         pole_width, pole_height))
        
        # Flag triangle
        flag_height = size // 3
        flag_width = size // 3
        points = [
            (center_x, y + 4),
            (center_x + flag_width, y + 4 + flag_height // 2),
            (center_x, y + 4 + flag_height)
        ]
        pygame.draw.polygon(self.screen, flag_color, points)

    def drawEndGameOverlay(self):
        """Draw game over or win message with pixel art style."""
        overlayWidth = 320
        overlayHeight = 180
        borderWidth = 2

        # Calculate centered position
        overlayX = (self.screen.get_width() - overlayWidth) // 2
        overlayY = (self.screen.get_height() - overlayHeight) // 2

        # Draw main overlay background
        pygame.draw.rect(
            self.screen,
            (30, 30, 30),
            (overlayX, overlayY, overlayWidth, overlayHeight)
        )

        # Draw simple border
        pygame.draw.rect(
            self.screen,
            settings.COLORS["accent"],
            (overlayX, overlayY, overlayWidth, overlayHeight),
            borderWidth
        )

        # Main message with pixel art text
        msg = "YOU WIN!" if self.state == GameState.WIN else "GAME OVER"
        color = settings.COLORS["win"] if self.state == GameState.WIN else settings.COLORS["lose"]

        msg_x = overlayX + overlayWidth // 2 - len(msg) * 9
        draw_pixel_text(self.screen, msg, msg_x, overlayY + 25, color, size='large')

        # Score display
        score_str = f"Score: {self.score:,}"
        score_x = overlayX + overlayWidth // 2 - len(score_str) * 8
        draw_pixel_text(self.screen, score_str, score_x, overlayY + 70, settings.COLORS["accent"], size='medium')

        # Rank or status message
        if self.lastScoreRank and self.lastScoreRank > 0 and self.lastScoreRank <= settings.LEADERBOARD_MAX_ENTRIES:
            rank_str = f"Rank: #{self.lastScoreRank}"
            rank_x = overlayX + overlayWidth // 2 - len(rank_str) * 8
            draw_pixel_text(self.screen, rank_str, rank_x, overlayY + 100, settings.COLORS["text_secondary"], size='medium')

        # Instructions
        restart_str = "[R] Restart"
        restart_x = overlayX + overlayWidth // 2 - len(restart_str) * 8
        draw_pixel_text(self.screen, restart_str, restart_x, overlayY + 130, settings.COLORS["text_secondary"], size='medium')

        menu_str = "[ESC] Menu"
        menu_x = overlayX + overlayWidth // 2 - len(menu_str) * 8
        draw_pixel_text(self.screen, menu_str, menu_x, overlayY + 155, settings.COLORS["text_secondary"], size='medium')
