"""Heads-up display showing game status, timer, and mine counter."""


import pygame


class Hud:
    """Top bar displaying mine counter, timer, and game controls."""

    def __init__(self, x, y, width, height, onRestart=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.mineCount = 0
        self.timer = 0
        self.onRestart = onRestart
        self.font = pygame.font.Font(None, 48)
        self.smallFont = pygame.font.Font(None, 24)
        self.restartButton = None
        self.initRestartButton()

    def initRestartButton(self):
        """Create restart button in HUD."""
        centerX = self.rect.centerx
        self.restartButton = pygame.Rect(centerX - 25, self.rect.y + 10, 50, 40)

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

    def draw(self, surface):
        """Render HUD to screen."""
        # Background
        pygame.draw.rect(surface, (128, 128, 128), self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)

        # Left side - Mine counter
        mineText = self.font.render(str(self.mineCount).zfill(3), True, (255, 0, 0))
        surface.blit(mineText, (self.rect.x + 20, self.rect.y + 15))

        # Center - Restart button (smiley face)
        pygame.draw.rect(surface, (192, 192, 192), self.restartButton)
        pygame.draw.rect(surface, (255, 255, 255), self.restartButton, 2)

        smiley = self.smallFont.render(":-)", True, (0, 0, 0))
        smileyRect = smiley.get_rect(center=self.restartButton.center)
        surface.blit(smiley, smileyRect)

        # Right side - Timer
        minutes = self.timer // 60
        seconds = self.timer % 60
        timerText = self.font.render(f"{minutes:02}:{seconds:02}", True, (255, 0, 0))
        surface.blit(timerText, (self.rect.right - 100, self.rect.y + 15))

    def reset(self):
        """Reset HUD to initial state."""
        self.mineCount = 0
        self.timer = 0
