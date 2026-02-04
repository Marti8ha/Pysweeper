"""Main menu screen with difficulty selection and game start options."""


import pygame
from .button import Button
from ..core.state import Difficulty


class Menu:
    """Start screen with game title and difficulty selection."""

    def __init__(self, onStartGame=None):
        self.onStartGame = onStartGame
        self.font = pygame.font.Font(None, 72)
        self.smallFont = pygame.font.Font(None, 36)
        self.buttons = []
        self.initButtons()

    def initButtons(self):
        """Create menu buttons for difficulty selection."""
        centerX = 400
        startY = 250

        # Easy button
        self.buttons.append(Button(
            centerX - 100, startY, 200, 50,
            "Easy (9x9)",
            lambda: self.startGame(*Difficulty.EASY)
        ))

        # Medium button
        self.buttons.append(Button(
            centerX - 100, startY + 70, 200, 50,
            "Medium (16x16)",
            lambda: self.startGame(*Difficulty.MEDIUM)
        ))

        # Hard button
        self.buttons.append(Button(
            centerX - 100, startY + 140, 200, 50,
            "Hard (30x16)",
            lambda: self.startGame(*Difficulty.HARD)
        ))

    def startGame(self, rows, cols, mines):
        """Callback to start game with selected difficulty."""
        if self.onStartGame:
            self.onStartGame(rows, cols, mines)

    def handleEvent(self, event):
        """Process events for all menu buttons."""
        for button in self.buttons:
            button.handleEvent(event)

    def draw(self, surface):
        """Render menu to screen."""
        surface.fill((192, 192, 192))

        # Title
        title = self.font.render("PYSWEEPER", True, (0, 0, 128))
        titleRect = title.get_rect(center=(400, 150))
        surface.blit(title, titleRect)

        # Subtitle
        subtitle = self.smallFont.render("Minesweeper Clone", True, (64, 64, 64))
        subRect = subtitle.get_rect(center=(400, 190))
        surface.blit(subtitle, subRect)

        # Instructions
        instruction = self.smallFont.render("Select Difficulty:", True, (0, 0, 0))
        instrRect = instruction.get_rect(center=(400, 220))
        surface.blit(instruction, instrRect)

        # Draw buttons
        for button in self.buttons:
            button.draw(surface)

    def updateButtonPositions(self, screenWidth, screenHeight):
        """Recalculate button positions for new screen size."""
        centerX = screenWidth // 2
        startY = 250
        positions = [(centerX - 100, startY), (centerX - 100, startY + 70), (centerX - 100, startY + 140)]

        for button, pos in zip(self.buttons, positions):
            button.setPosition(*pos)
