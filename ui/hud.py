"""Heads-up display showing game status, timer, and mine counter."""

import pygame
import settings


class Hud:
    """Top bar displaying mine counter, timer, and game controls."""

    def __init__(self, x, y, width, height, onRestart=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.mineCount = 0
        self.timer = 0
        self.onRestart = onRestart
        # Use monospace font for consistent number display
        try:
            self.font = pygame.font.Font("Cascadia Mono.ttf", 42)
        except (FileNotFoundError, IOError):
            self.font = pygame.font.Font(None, 42)
        self.smallFont = pygame.font.Font(None, 20)
        self.restartButtonY = y + 10
        self.restartButton = pygame.Rect(x + width // 2 - 25, self.restartButtonY, 50, 40)
        
        # Animation state
        self.buttonHovered = False

    def setMineCount(self, count):
        """Update displayed mine count."""
        self.mineCount = count

    def setTimer(self, seconds):
        """Update displayed timer value."""
        self.timer = seconds

    def handleEvent(self, event):
        """Process events for HUD components."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.restartButton.collidepoint(event.pos):
                if self.onRestart:
                    self.onRestart()
        elif event.type == pygame.MOUSEMOTION:
            self.buttonHovered = self.restartButton.collidepoint(event.pos)

    def draw(self, surface):
        """Render HUD to screen with dark theme."""
        # Dark HUD background
        pygame.draw.rect(surface, settings.COLORS["hud_background"], self.rect)
        
        # Subtle top border accent
        pygame.draw.rect(surface, settings.COLORS["accent"], (self.rect.x, self.rect.y, self.rect.width, 2))

        # Mine counter - bright color for visibility
        mineText = self.font.render(str(self.mineCount).zfill(3), True, settings.COLORS["flag"])
        surface.blit(mineText, (self.rect.x + 20, self.rect.y + 8))

        # Restart button with modern styling
        btnColor = settings.COLORS["button_pressed"] if self.buttonHovered else settings.COLORS["button_background"]
        pygame.draw.rect(surface, btnColor, self.restartButton)
        pygame.draw.rect(surface, settings.COLORS["accent"], self.restartButton, 2)

        # Smiley face with color
        smileyColor = settings.COLORS["accent"] if self.buttonHovered else settings.COLORS["text_secondary"]
        smiley = self.smallFont.render(":-)", True, smileyColor)
        smileyRect = smiley.get_rect(center=self.restartButton.center)
        surface.blit(smiley, smileyRect)

        # Timer - bright color
        minutes = self.timer // 60
        seconds = self.timer % 60
        timerText = self.font.render(f"{minutes:02}:{seconds:02}", True, settings.COLORS["accent"])
        surface.blit(timerText, (self.rect.right - 110, self.rect.y + 8))

    def reset(self):
        """Reset HUD to initial state."""
        self.mineCount = 0
        self.timer = 0
