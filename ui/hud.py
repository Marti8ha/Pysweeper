"""Heads-up display showing game status, timer, and mine counter."""

import pygame
import settings
from ui.pixel_utils import draw_pixel_text, draw_pixel_button, draw_smiley


class Hud:
    """Top bar displaying mine counter, timer, and game controls."""

    def __init__(self, x, y, width, height, onRestart=None, onMenu=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.mineCount = 0
        self.timer = 0
        self.onRestart = onRestart
        self.onMenu = onMenu
        self.restartButtonY = y + 10
        self.restartButton = pygame.Rect(x + width // 2 - 25, self.restartButtonY, 50, 40)

        # Menu button
        self.menuButtonWidth = 60
        self.menuButtonHeight = 30
        self.menuButton = pygame.Rect(
            x + width - 80,
            y + (height - self.menuButtonHeight) // 2,
            self.menuButtonWidth,
            self.menuButtonHeight
        )

        # Animation state
        self.buttonHovered = False
        self.isPressed = False
        self.menuButtonHovered = False
        self.menuButtonPressed = False

    def setMineCount(self, count):
        """Update displayed mine count."""
        self.mineCount = count

    def setTimer(self, seconds):
        """Update displayed timer value."""
        self.timer = seconds

    def handleEvent(self, event):
        """Process events for HUD components."""
        if event.type == pygame.MOUSEMOTION:
            self.buttonHovered = self.restartButton.collidepoint(event.pos)
            self.menuButtonHovered = self.menuButton.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.restartButton.collidepoint(event.pos):
                    self.isPressed = True
                elif self.menuButton.collidepoint(event.pos):
                    self.menuButtonPressed = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.isPressed and self.restartButton.collidepoint(event.pos):
                    if self.onRestart:
                        self.onRestart()
                if self.menuButtonPressed and self.menuButton.collidepoint(event.pos):
                    if self.onMenu:
                        self.onMenu()
                self.isPressed = False
                self.menuButtonPressed = False

    def draw(self, surface):
        """Render HUD to screen with true pixel art style."""
        from ui.pixel_utils import get_pixel_text_width, draw_pixel_button, draw_smiley, draw_pixel_text

        # Update rect to match current surface width
        self.rect.width = surface.get_width()

        # Dark HUD background
        pygame.draw.rect(surface, settings.COLORS["hud_background"], self.rect)

        # Sharp top border accent (pixel style)
        pygame.draw.rect(surface, settings.COLORS["accent"],
                        (self.rect.x, self.rect.y, self.rect.width, 3))

        # Mine counter - pixel art numbers
        mine_str = str(self.mineCount).zfill(3)
        mine_width = get_pixel_text_width(mine_str, size='large')
        # Position from left edge with padding
        mine_x = self.rect.x + 20
        draw_pixel_text(surface, mine_str, mine_x, self.rect.y + 15,
                       settings.COLORS["flag"], size='large')

        # Update restart button position to center of HUD
        button_width = 50
        button_height = 40
        self.restartButton = pygame.Rect(
            self.rect.x + (self.rect.width - button_width) // 2,
            self.rect.y + 10,
            button_width, button_height
        )

        # Determine button colors
        if self.isPressed:
            btnColor = settings.COLORS["button_pressed"]
            borderColor = settings.COLORS["accent"]
        elif self.buttonHovered:
            btnColor = (
                min(255, settings.COLORS["button_background"][0] + 20),
                min(255, settings.COLORS["button_background"][1] + 20),
                min(255, settings.COLORS["button_background"][2] + 20)
            )
            borderColor = settings.COLORS["accent"]
        else:
            btnColor = settings.COLORS["button_background"]
            borderColor = settings.COLORS["button_border"]

        # Draw restart button with pixel art styling
        draw_pixel_button(surface, self.restartButton, btnColor, borderColor,
                         pressed=self.isPressed, hovered=self.buttonHovered)

        # Draw pixel art smiley in the button
        smiley_size = 22
        smiley_x = self.restartButton.x + (self.restartButton.width - smiley_size) // 2
        smiley_y = self.restartButton.y + (self.restartButton.height - smiley_size) // 2
        expression = 'happy' if not self.isPressed else 'neutral'
        draw_smiley(surface, smiley_x, smiley_y, smiley_size, expression=expression)

        # Timer - pixel art time display
        minutes = self.timer // 60
        seconds = self.timer % 60
        timer_str = f"{minutes:02}:{seconds:02}"
        timer_width = get_pixel_text_width(timer_str, size='large')
        # Position before menu button
        timer_x = self.rect.right - 100 - timer_width
        draw_pixel_text(surface, timer_str, timer_x, self.rect.y + 15,
                       settings.COLORS["accent"], size='large')

        # Update and draw menu button
        self.menuButton = pygame.Rect(
            self.rect.right - 80,
            self.rect.y + (self.rect.height - self.menuButtonHeight) // 2,
            self.menuButtonWidth,
            self.menuButtonHeight
        )

        # Menu button colors
        if self.menuButtonPressed:
            menuBtnColor = settings.COLORS["button_pressed"]
            menuBorderColor = settings.COLORS["accent"]
        elif self.menuButtonHovered:
            menuBtnColor = (
                min(255, settings.COLORS["button_background"][0] + 20),
                min(255, settings.COLORS["button_background"][1] + 20),
                min(255, settings.COLORS["button_background"][2] + 20)
            )
            menuBorderColor = settings.COLORS["accent"]
        else:
            menuBtnColor = settings.COLORS["button_background"]
            menuBorderColor = settings.COLORS["button_border"]

        # Draw menu button
        draw_pixel_button(surface, self.menuButton, menuBtnColor, menuBorderColor,
                         pressed=self.menuButtonPressed, hovered=self.menuButtonHovered)

        # Draw MENU text on button
        menu_text = "MENU"
        menu_text_width = get_pixel_text_width(menu_text, size='small')
        menu_text_x = self.menuButton.x + (self.menuButton.width - menu_text_width) // 2
        menu_text_y = self.menuButton.y + (self.menuButton.height - 14) // 2
        draw_pixel_text(surface, menu_text, menu_text_x, menu_text_y,
                       settings.COLORS["text_primary"], size='small')

    def reset(self):
        """Reset HUD to initial state."""
        self.mineCount = 0
        self.timer = 0
        self.buttonHovered = False
        self.isPressed = False
        self.menuButtonHovered = False
        self.menuButtonPressed = False
