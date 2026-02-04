"""Main game controller managing pygame loop, input handling, and state transitions."""


import pygame
import sys
from .state import GameState, Difficulty
from .board import Board


class Game:
    """Main game controller handling the pygame event loop and state management."""

    def __init__(self):
        pygame.init()
        self.screen = None
        self.clock = None
        self.state = GameState.MENU
        self.board = None
        self.font = None
        self.initDisplay()
        self.running = True

    def initDisplay(self):
        """Initialize pygame display and clock."""
        pygame.display.set_caption("Pysweeper")
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

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

            if self.state == GameState.MENU:
                self.handleMenuEvents(event)
            elif self.state == GameState.PLAYING:
                self.handlePlayingEvents(event)
            elif self.state in (GameState.GAME_OVER, GameState.WIN):
                self.handleEndGameEvents(event)

    def handleMenuEvents(self, event):
        """Handle events in menu state."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self.startGame(*Difficulty.MEDIUM)

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
        if event.button == 1:  # Left click - reveal
            pass  # Will integrate with UI

        elif event.button == 3:  # Right click - flag
            pass  # Will integrate with UI

    def startGame(self, rows, cols, mines):
        """Initialize a new game with specified difficulty."""
        self.board = Board(rows, cols, mines)
        self.state = GameState.PLAYING

    def restartGame(self):
        """Restart the current game with same settings."""
        if self.board:
            self.startGame(self.board.rows, self.board.cols, self.board.mineCount)

    def switchState(self, newState):
        """Change the current game state."""
        self.state = newState

    def update(self):
        """Update game state each frame."""
        if self.state == GameState.PLAYING:
            pass  # Update timer, animations, etc.

    def draw(self):
        """Render current game state to screen."""
        self.screen.fill((192, 192, 192))  # Classic gray background

        if self.state == GameState.MENU:
            self.drawMenu()
        elif self.state == GameState.PLAYING:
            self.drawGame()
        elif self.state in (GameState.GAME_OVER, GameState.WIN):
            self.drawGame()
            self.drawEndGameOverlay()

        pygame.display.flip()

    def drawMenu(self):
        """Render main menu screen."""
        title = self.font.render("PYSWEEPER", True, (0, 0, 128))
        titleRect = title.get_rect(center=(400, 200))
        self.screen.blit(title, titleRect)

        instruction = self.font.render("Click to Start", True, (0, 0, 0))
        instrRect = instruction.get_rect(center=(400, 300))
        self.screen.blit(instruction, instrRect)

    def drawGame(self):
        """Render the game board."""
        if self.board:
            for r in range(self.board.rows):
                for c in range(self.board.cols):
                    self.drawTile(r, c)

    def drawTile(self, row, col):
        """Draw a single tile at grid position."""
        tile = self.board.getTile(row, col)
        x = 100 + col * 40
        y = 100 + row * 40

        # Draw tile background
        color = (128, 128, 128) if tile.isRevealed else (192, 192, 192)
        pygame.draw.rect(self.screen, color, (x, y, 38, 38))
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, 38, 38), 2)

        # Draw content
        if tile.isRevealed:
            if tile.isMine:
                text = self.font.render("M", True, (255, 0, 0))
            elif tile.neighborCount > 0:
                colors = {1: (0, 0, 255), 2: (0, 128, 0), 3: (255, 0, 0),
                          4: (0, 0, 128), 5: (128, 0, 0), 6: (0, 128, 128),
                          7: (0, 0, 0), 8: (128, 128, 128)}
                text = self.font.render(str(tile.neighborCount), True, colors.get(tile.neighborCount, (0, 0, 0)))
                textRect = text.get_rect(center=(x + 19, y + 19))
                self.screen.blit(text, textRect)
        elif tile.isFlagged:
            text = self.font.render("F", True, (255, 0, 0))
            textRect = text.get_rect(center=(x + 19, y + 19))
            self.screen.blit(text, textRect)

    def drawEndGameOverlay(self):
        """Draw game over or win message."""
        overlay = pygame.Surface((300, 100))
        overlay.fill((255, 255, 255))
        overlay.set_alpha(200)

        msg = "GAME OVER" if self.state == GameState.GAME_OVER else "YOU WIN!"
        color = (255, 0, 0) if self.state == GameState.GAME_OVER else (0, 128, 0)
        text = self.font.render(msg, True, color)

        self.screen.blit(overlay, (250, 250))
        self.screen.blit(text, (340, 280))

        restartText = self.font.render("Press R to Restart", True, (0, 0, 0))
        self.screen.blit(restartText, (290, 320))
