"""Leaderboard UI component for displaying top scores."""

import pygame
from .button import Button
from core.state import Difficulty
from ui.pixel_utils import draw_pixel_text
import settings


class LeaderboardUI:
    """Screen displaying the top 10 scores with pixel art styling."""

    def __init__(self, storage, onBack=None):
        """Initialize the leaderboard screen.

        Args:
            storage: LeaderboardStorage instance for accessing scores.
            onBack: Optional callback when back button is pressed.
        """
        self.storage = storage
        self.onBack = onBack
        self.buttons = []
        self.initButtons()

    def initButtons(self):
        """Create navigation buttons."""
        self._createButtons(settings.WIDTH, settings.HEIGHT)
    
    def _createButtons(self, screen_width, screen_height):
        """Create buttons with proper sizing for current screen."""
        self.buttons = []
        center_x = screen_width // 2

        # Back button - auto-sized
        self.buttons.append(Button(
            center_x, screen_height - 80, 0, 0,  # Auto-size
            "Back",
            self._onBackClicked
        ))
        
        # Center the button
        for button in self.buttons:
            button.rect.x = center_x - button.rect.width // 2

    def _onBackClicked(self):
        """Handle back button click."""
        if self.onBack:
            self.onBack()

    def handleEvent(self, event):
        """Process pygame events for leaderboard components."""
        for button in self.buttons:
            button.handleEvent(event)

    def draw(self, surface):
        """Render leaderboard to screen with pixel art style.

        Args:
            surface: Pygame surface to draw on.
        """
        from ui.pixel_utils import get_pixel_text_width

        # Get current dimensions
        screen_width = surface.get_width()
        screen_height = surface.get_height()

        # Recreate buttons if needed
        if not self.buttons:
            self._createButtons(screen_width, screen_height)

        surface.fill(settings.COLORS["background"])

        # Title with pixel art text - centered
        title_text = "LEADERBOARD"
        title_width = get_pixel_text_width(title_text, size='large')
        title_x = (screen_width - title_width) // 2
        title_y = min(80, screen_height // 10)
        draw_pixel_text(surface, title_text, title_x, title_y, settings.COLORS["accent"], size='large')

        # Update button positions
        self.updateButtonPositions(screen_width, screen_height)

        # Load and display scores
        scores = self.storage.getTopScores()
        self._drawScoreList(surface, scores, screen_width, screen_height)

        # Draw buttons
        for button in self.buttons:
            button.draw(surface)

    def _drawScoreList(self, surface, scores, screen_width=None, screen_height=None):
        """Draw the list of top scores with pixel art styling.

        Args:
            surface: Pygame surface to draw on.
            scores: List of score dictionaries.
            screen_width: Current screen width (optional).
            screen_height: Current screen height (optional).
        """
        from ui.pixel_utils import get_pixel_text_width
        
        if screen_width is None:
            screen_width = settings.WIDTH
        if screen_height is None:
            screen_height = settings.HEIGHT
            
        if not scores:
            # No scores yet message
            no_scores_text = "No scores yet!"
            text_width = get_pixel_text_width(no_scores_text, size='medium')
            draw_pixel_text(surface, no_scores_text, (screen_width - text_width) // 2,
                           screen_height // 2 - 25, settings.COLORS["text_primary"], size='medium')

            hint_text = "Complete a game to see your name here."
            hint_width = get_pixel_text_width(hint_text, size='medium')
            draw_pixel_text(surface, hint_text, (screen_width - hint_width) // 2,
                           screen_height // 2 + 15, settings.COLORS["text_secondary"], size='medium')
            return

        # Draw simple table container
        container_margin = min(40, screen_width // 16)
        container_width = screen_width - 2 * container_margin
        container_height = min(380, screen_height - 220)
        container_y = min(140, screen_height // 4)
        containerRect = pygame.Rect(container_margin, container_y, container_width, container_height)
        pygame.draw.rect(
            surface,
            settings.COLORS["background_alt"],
            containerRect
        )
        pygame.draw.rect(
            surface,
            settings.COLORS["button_border"],
            containerRect,
            1
        )

        # Header row
        headerY = container_y + 20
        self._drawTableHeader(surface, headerY, container_margin, container_width)

        # Score rows
        rowY = headerY + 50
        for i, score in enumerate(scores):
            self._drawScoreRow(surface, i + 1, score, rowY, container_margin, container_width)
            rowY += 35
            # Stop if we're running out of space
            if rowY > container_y + container_height - 30:
                break

    def _drawTableHeader(self, surface, y, container_margin, container_width):
        """Draw column headers for the score table.

        Args:
            surface: Pygame surface to draw on.
            y: Vertical position for the header.
            container_margin: Left margin of container.
            container_width: Width of container.
        """
        # Calculate column positions proportionally
        rankX = container_margin + 15
        scoreX = container_margin + container_width * 0.25
        diffX = container_margin + container_width * 0.45
        timeX = container_margin + container_width * 0.65
        dateX = container_margin + container_width * 0.80

        # Simple header background
        headerRect = pygame.Rect(container_margin + 5, y - 8, container_width - 10, 40)
        pygame.draw.rect(
            surface,
            settings.COLORS["hud_background"],
            headerRect
        )

        headers = [
            ("Rank", rankX),
            ("Score", scoreX),
            ("Diff", diffX),
            ("Time", timeX),
            ("Date", dateX),
        ]

        for text, x in headers:
            draw_pixel_text(surface, text, int(x), y, settings.COLORS["accent"], size='small')

    def _drawScoreRow(self, surface, rank, score, y, container_margin, container_width):
        """Draw a single score row.

        Args:
            surface: Pygame surface to draw on.
            rank: Position in leaderboard (1-indexed).
            score: Score dictionary with keys: score, difficulty, date, time_elapsed.
            y: Vertical position for the row.
            container_margin: Left margin of container.
            container_width: Width of container.
        """
        # Calculate column positions proportionally
        rankX = container_margin + 15
        scoreX = container_margin + container_width * 0.25
        diffX = container_margin + container_width * 0.45
        timeX = container_margin + container_width * 0.65
        dateX = container_margin + container_width * 0.80

        # Highlight top 3 ranks with medal colors
        if rank == 1:
            color = settings.COLORS["accent"]  # Gold
        elif rank == 2:
            color = (192, 192, 192)  # Silver
        elif rank == 3:
            color = (205, 127, 50)   # Bronze
        else:
            color = settings.COLORS["text_primary"]

        rankLabel = f"#{rank:2}"

        # Rank (with medal colors for top 3)
        draw_pixel_text(surface, rankLabel, int(rankX), y, color, size='small')

        # Score
        scoreValue = score.get("score", 0)
        draw_pixel_text(surface, f"{scoreValue:,}", int(scoreX), y, settings.COLORS["text_primary"], size='small')

        # Difficulty (truncate if needed for small screens)
        diff_text = score.get("difficulty", "Unknown")[:8]  # Truncate to 8 chars
        draw_pixel_text(surface, diff_text, int(diffX), y, settings.COLORS["text_secondary"], size='small')

        # Time (format as MM:SS)
        timeElapsed = score.get("time_elapsed", 0)
        minutes = timeElapsed // 60
        seconds = timeElapsed % 60
        draw_pixel_text(surface, f"{minutes:02}:{seconds:02}", int(timeX), y, settings.COLORS["text_secondary"], size='small')

        # Date (show first 10 chars to fit)
        date_text = score.get("date", "")[:10]
        draw_pixel_text(surface, date_text, int(dateX), y, settings.COLORS["text_secondary"], size='small')

    def refresh(self):
        """Reload scores from storage."""
        pass  # Scores are loaded fresh each draw

    def updateButtonPositions(self, screenWidth, screenHeight):
        """Recalculate button positions for new screen size."""
        center_x = screenWidth // 2

        for button in self.buttons:
            if button.text == "Back":
                button.rect.x = center_x - button.rect.width // 2
                button.rect.y = screenHeight - 80
                break
