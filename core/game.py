"""Main game controller managing pygame loop, input handling, and state transitions."""


import pygame
import sys
from .state import GameState, Difficulty
from .board import Board
from ui.hud import Hud
from ui.menu import Menu
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

        self.hud = Hud(0, 0, settings.WIDTH, 60, onRestart=self.restartGame)
        self.menu = Menu(onStartGame=self.startGame)

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

    def handleMouseClick(self, event):
        """Process mouse clicks on the game board."""
        if not self.board:
            return

        boardStartX = settings.BOARD_OFFSET_X
        boardStartY = settings.BOARD_OFFSET_Y
        tileSize = settings.TILE_SIZE

        col = (event.pos[0] - boardStartX) // tileSize
        row = (event.pos[1] - boardStartY) // tileSize

        if 0 <= row < self.board.rows and 0 <= col < self.board.cols:
            if event.button == 1:
                self.board.revealTile(row, col)
            elif event.button == 3:
                self.board.toggleFlag(row, col)

    def startGame(self, rows, cols, mines):
        """Initialize a new game with specified difficulty."""
        self.board = Board(rows, cols, mines)
        self.state = GameState.PLAYING
        self.startTime = pygame.time.get_ticks()

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

    def draw(self):
        """Render current game state to screen."""
        self.screen.fill(settings.COLORS["background"])

        if self.hud:
            self.hud.draw(self.screen)

        if self.state == GameState.MENU:
            self.menu.draw(self.screen)
        elif self.state == GameState.PLAYING:
            self.drawGame()
        elif self.state in (GameState.GAME_OVER, GameState.WIN):
            self.drawGame()
            self.drawEndGameOverlay()

        pygame.display.flip()

    def drawGame(self):
        """Render the game board."""
        if self.board:
            for r in range(self.board.rows):
                for c in range(self.board.cols):
                    self.drawTile(r, c)

    def drawTile(self, row, col):
        """Draw a single tile at grid position."""
        tile = self.board.getTile(row, col)
        x = settings.BOARD_OFFSET_X + col * settings.TILE_SIZE
        y = settings.BOARD_OFFSET_Y + row * settings.TILE_SIZE
        size = settings.TILE_SIZE - 2

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
                           (x, y + size), (x + size, y + size), 2)
            pygame.draw.line(self.screen, settings.COLORS["tile_border_dark"],
                           (x + size, y), (x + size, y + size), 2)

            if tile.isFlagged:
                text = self.font.render("F", True, settings.COLORS["flag"])
                textRect = text.get_rect(center=(x + size // 2, y + size // 2))
                self.screen.blit(text, textRect)

    def drawEndGameOverlay(self):
        """Draw game over or win message."""
        overlay = pygame.Surface((350, 120), pygame.SRCALPHA)
        overlay.fill(settings.COLORS["overlay_background"])

        pygame.draw.rect(overlay, settings.COLORS["overlay_border"],
                        overlay.get_rect(), 2)

        msg = "GAME OVER" if self.state == GameState.GAME_OVER else "YOU WIN!"
        color = settings.COLORS["lose"] if self.state == GameState.GAME_OVER else settings.COLORS["win"]
        text = self.font.render(msg, True, color)

        textRect = text.get_rect(center=(overlay.get_width() // 2, 35))
        overlay.blit(text, textRect)

        restartText = pygame.font.Font(None, 28).render("Press R to Restart", True, settings.COLORS["text_secondary"])
        restartRect = restartText.get_rect(center=(overlay.get_width() // 2, 75))
        overlay.blit(restartText, restartRect)

        overlayX = (settings.WIDTH - overlay.get_width()) // 2
        overlayY = (settings.HEIGHT - overlay.get_height()) // 2
        self.screen.blit(overlay, (overlayX, overlayY))
