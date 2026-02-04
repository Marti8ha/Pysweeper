"""Leaderboard UI component for displaying top scores."""

import pygame
from .button import Button
from core.state import Difficulty
import settings


class LeaderboardUI:
    """Screen displaying the top 10 scores with dark theme styling."""

    def __init__(self, storage, onBack=None):
        """Initialize the leaderboard screen.

        Args:
            storage: LeaderboardStorage instance for accessing scores.
            onBack: Optional callback when back button is pressed.
        """
        self.storage = storage
        self.onBack = onBack

        # Try to use Cascadia Mono or default font
        try:
            self.titleFont = pygame.font.Font("Cascadia Mono.ttf", 48)
            self.headerFont = pygame.font.Font("Cascadia Mono.ttf", 24)
            self.font = pygame.font.Font("Cascadia Mono.ttf", 20)
        except (FileNotFoundError, IOError):
            self.titleFont = pygame.font.Font(None, 48)
            self.headerFont = pygame.font.Font(None, 24)
            self.font = pygame.font.Font(None, 20)

        self.buttons = []
        self.initButtons()

    def initButtons(self):
        """Create navigation buttons."""
        centerX = settings.WIDTH // 2

        # Back button
        self.buttons.append(Button(
            centerX - 80, settings.HEIGHT - 80, 160, 50,
            "Back",
            self._onBackClicked
        ))

    def _onBackClicked(self):
        """Handle back button click."""
        if self.onBack:
            self.onBack()

    def handleEvent(self, event):
        """Process pygame events for leaderboard components."""
        for button in self.buttons:
            button.handleEvent(event)

    def draw(self, surface):
        """Render leaderboard to screen.

        Args:
            surface: Pygame surface to draw on.
        """
        surface.fill(settings.COLORS["background"])

        # Decorative line
        pygame.draw.line(surface, settings.COLORS["accent"], (200, 100), (600, 100), 2)

        # Title
        title = self.titleFont.render("LEADERBOARD", True, settings.COLORS["accent"])
        titleRect = title.get_rect(center=(settings.WIDTH // 2, 160))
        surface.blit(title, titleRect)

        # Load and display scores
        scores = self.storage.getTopScores()
        self._drawScoreList(surface, scores)

        # Draw buttons
        for button in self.buttons:
            button.draw(surface)

    def _drawScoreList(self, surface, scores):
        """Draw the list of top scores.

        Args:
            surface: Pygame surface to draw on.
            scores: List of score dictionaries.
        """
        if not scores:
            # No scores yet message
            noScoresText = self.headerFont.render(
                "No scores yet! Complete a game to see your name here.",
                True, settings.COLORS["text_secondary"]
            )
            noScoresRect = noScoresText.get_rect(
                center=(settings.WIDTH // 2, settings.HEIGHT // 2)
            )
            surface.blit(noScoresText, noScoresRect)
            return

        # Header row
        headerY = 230
        self._drawTableHeader(surface, headerY)

        # Score rows
        rowY = headerY + 40
        for i, score in enumerate(scores):
            self._drawScoreRow(surface, i + 1, score, rowY)
            rowY += 35

    def _drawTableHeader(self, surface, y):
        """Draw column headers for the score table.

        Args:
            surface: Pygame surface to draw on.
            y: Vertical position for the header.
        """
        # Column positions
        rankX = 100
        scoreX = 250
        diffX = 380
        timeX = 520
        dateX = 620

        headers = [
            ("Rank", rankX),
            ("Score", scoreX),
            ("Difficulty", diffX),
            ("Time", timeX),
            ("Date", dateX),
        ]

        for text, x in headers:
            textSurf = self.headerFont.render(text, True, settings.COLORS["accent"])
            surface.blit(textSurf, (x, y))

        # Underline
        pygame.draw.line(
            surface, settings.COLORS["button_border"],
            (80, y + 30), (720, y + 30), 1
        )

    def _drawScoreRow(self, surface, rank, score, y):
        """Draw a single score row.

        Args:
            surface: Pygame surface to draw on.
            rank: Position in leaderboard (1-indexed).
            score: Score dictionary with keys: score, difficulty, date, time_elapsed.
            y: Vertical position for the row.
        """
        # Column positions
        rankX = 100
        scoreX = 250
        diffX = 380
        timeX = 520
        dateX = 620

        # Highlight top 3 ranks
        if rank <= 3:
            color = settings.COLORS["accent"]
        else:
            color = settings.COLORS["text_primary"]

        # Rank (with medal emoji effect via colors)
        rankText = self.font.render(f"#{rank:2}", True, color)
        surface.blit(rankText, (rankX, y))

        # Score
        scoreValue = score.get("score", 0)
        scoreText = self.font.render(f"{scoreValue:,}", True, settings.COLORS["text_primary"])
        surface.blit(scoreText, (scoreX, y))

        # Difficulty
        diffText = self.font.render(score.get("difficulty", "Unknown"), True, settings.COLORS["text_secondary"])
        surface.blit(diffText, (diffX, y))

        # Time (format as MM:SS)
        timeElapsed = score.get("time_elapsed", 0)
        minutes = timeElapsed // 60
        seconds = timeElapsed % 60
        timeText = self.font.render(f"{minutes:02}:{seconds:02}", True, settings.COLORS["text_secondary"])
        surface.blit(timeText, (timeX, y))

        # Date
        dateText = self.font.render(score.get("date", ""), True, settings.COLORS["text_secondary"])
        surface.blit(dateText, (dateX, y))

        # Subtle separator line
        pygame.draw.line(
            surface, settings.COLORS["tile_border_dark"],
            (80, y + 28), (720, y + 28), 1
        )

    def refresh(self):
        """Reload scores from storage."""
        pass  # Scores are loaded fresh each draw

    def updateButtonPositions(self, screenWidth, screenHeight):
        """Recalculate button positions for new screen size."""
        centerX = screenWidth // 2

        for button in self.buttons:
            if button.text == "Back":
                button.setPosition(centerX - 80, screenHeight - 80)
                break
