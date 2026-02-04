"""Main menu screen with difficulty selection and game start options."""

import pygame
from .button import Button
from core.state import Difficulty
from ui.pixel_utils import draw_pixel_text
import settings


class Menu:
    """Start screen with game title and difficulty selection."""

    def __init__(self, onStartGame=None, onShowLeaderboard=None):
        """Initialize the menu.

        Args:
            onStartGame: Callback to start game with (rows, cols, mines).
            onShowLeaderboard: Optional callback to show leaderboard.
        """
        self.onStartGame = onStartGame
        self.onShowLeaderboard = onShowLeaderboard
        self.buttons = []
        self.initButtons()

    def initButtons(self):
        """Create menu buttons for difficulty selection and leaderboard."""
        self._createButtons(800, 600)  # Default size, will be updated on first draw

    def _createButtons(self, screen_width, screen_height):
        """Create or recreate buttons with proper sizing for current screen."""
        self.buttons = []
        
        center_x = screen_width // 2
        start_y = screen_height // 2 - 40  # Center vertically, offset upward
        button_spacing = 60

        # Easy button - auto-sized based on text
        self.buttons.append(Button(
            center_x, start_y, 0, 0,  # Width/height 0 = auto-size
            "Easy (9x9)",
            lambda: self.startGame(*Difficulty.EASY)
        ))

        # Medium button
        self.buttons.append(Button(
            center_x, start_y + button_spacing, 0, 0,
            "Medium (16x16)",
            lambda: self.startGame(*Difficulty.MEDIUM)
        ))

        # Hard button
        self.buttons.append(Button(
            center_x, start_y + button_spacing * 2, 0, 0,
            "Hard (30x16)",
            lambda: self.startGame(*Difficulty.HARD)
        ))

        # Leaderboard button
        self.buttons.append(Button(
            center_x, start_y + button_spacing * 3, 0, 0,
            "Leaderboard",
            self._showLeaderboard
        ))
        
        # Center all buttons horizontally
        for button in self.buttons:
            button.rect.x = center_x - button.rect.width // 2

    def startGame(self, rows, cols, mines):
        """Callback to start game with selected difficulty."""
        if self.onStartGame:
            self.onStartGame(rows, cols, mines)

    def _showLeaderboard(self):
        """Callback to show leaderboard screen."""
        if self.onShowLeaderboard:
            self.onShowLeaderboard()

    def handleEvent(self, event):
        """Process events for all menu buttons."""
        for button in self.buttons:
            button.handleEvent(event)

    def draw(self, surface):
        """Render menu to screen with pixel art style."""
        # Get current screen dimensions
        screen_width = surface.get_width()
        screen_height = surface.get_height()

        # Recreate buttons on first draw or if screen size changed significantly
        if not self.buttons:
            self._createButtons(screen_width, screen_height)

        # Fill background
        surface.fill(settings.COLORS["background"])

        # Calculate card dimensions based on screen size
        card_width = min(400, screen_width - 40)
        card_height = min(400, screen_height - 40)
        card_x = (screen_width - card_width) // 2
        card_y = (screen_height - card_height) // 2

        # Draw simple card background
        cardRect = pygame.Rect(card_x, card_y, card_width, card_height)
        pygame.draw.rect(surface, settings.COLORS["background_alt"], cardRect)

        # Single border for card
        pygame.draw.rect(surface, settings.COLORS["accent"], cardRect, 2)

        # Title with pixel art text
        titleText = "PYSWEEPER"
        from ui.pixel_utils import get_pixel_text_width
        title_width = get_pixel_text_width(titleText, size='large')
        title_x = (screen_width - title_width) // 2
        title_y = card_y + 50

        draw_pixel_text(surface, titleText, title_x, title_y, settings.COLORS["accent"], size='large')

        # Instructions
        instr_text = "Select Difficulty"
        instr_width = get_pixel_text_width(instr_text, size='medium')
        draw_pixel_text(surface, instr_text, (screen_width - instr_width) // 2,
                       card_y + 110, settings.COLORS["text_secondary"], size='medium')

        # Update button positions before drawing
        self.updateButtonPositions(screen_width, screen_height)

        # Draw buttons
        for button in self.buttons:
            button.draw(surface)

    def updateButtonPositions(self, screenWidth, screenHeight):
        """Recalculate button positions for new screen size."""
        center_x = screenWidth // 2

        # Calculate vertical center with offset for button cluster
        card_height = min(400, screenHeight - 40)
        card_y = (screenHeight - card_height) // 2
        start_y = card_y + 150  # Start below title area
        button_spacing = 55

        # Update each button position, keeping them centered
        for i, button in enumerate(self.buttons):
            new_y = start_y + i * button_spacing
            button.rect.x = center_x - button.rect.width // 2
            button.rect.y = new_y
