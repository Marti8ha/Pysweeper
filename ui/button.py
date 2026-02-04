"""Reusable button component for menus and game interface."""

import pygame
import settings


class Button:
    """Interactive button component with hover and click states."""

    def __init__(self, x, y, width, height, text, onClick=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.onClick = onClick
        self.isHovered = False
        self.isPressed = False
        # Try to use Cascadia Mono Bold or monospace font
        try:
            self.font = pygame.font.Font("CascadiaMono-Bold.ttf", 28)
        except (FileNotFoundError, IOError):
            self.font = pygame.font.Font(None, 28)
        
        # Animation state
        self.hoverProgress = 0.0
        self.pressProgress = 0.0

    def handleEvent(self, event):
        """Process pygame events for this button."""
        if event.type == pygame.MOUSEMOTION:
            self.isHovered = self.rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.isPressed = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.isPressed and self.rect.collidepoint(event.pos):
                    if self.onClick:
                        self.onClick()
                self.isPressed = False

    def draw(self, surface):
        """Render button to screen with smooth visual feedback."""
        # Smooth hover animation
        targetHover = 1.0 if self.isHovered else 0.0
        self.hoverProgress += (targetHover - self.hoverProgress) * 0.15
        
        # Smooth press animation
        targetPress = 1.0 if self.isPressed else 0.0
        self.pressProgress += (targetPress - self.pressProgress) * 0.2

        # Calculate colors based on state
        if self.isPressed:
            baseColor = settings.COLORS["button_pressed"]
            borderColor = settings.COLORS["button_border"]
            offset = 2
        elif self.isHovered:
            # Interpolate between normal and hover
            baseColor = self._interpolateColor(
                settings.COLORS["button_background"],
                settings.COLORS["button_hover"],
                self.hoverProgress
            )
            borderColor = settings.COLORS["accent"]
            offset = 0
        else:
            baseColor = settings.COLORS["button_background"]
            borderColor = settings.COLORS["button_border"]
            offset = 0

        # Draw button background
        pygame.draw.rect(surface, baseColor, self.rect)

        # Draw subtle glow effect on hover
        if self.isHovered:
            glowRect = self.rect.inflate(4, 4)
            glowSurface = pygame.Surface(glowRect.size, pygame.SRCALPHA)
            glowColor = (*settings.COLORS["accent"], int(40 * self.hoverProgress))
            pygame.draw.rect(glowSurface, glowColor, glowSurface.get_rect(), border_radius=8)
            surface.blit(glowSurface, glowRect.topleft)

        # Draw border
        borderWidth = 2 if not self.isHovered else 3
        pygame.draw.rect(surface, borderColor, self.rect, borderWidth)

        # Draw text with slight offset when pressed
        textColor = settings.COLORS["text_primary"]
        textSurf = self.font.render(self.text, True, textColor)
        textRect = textSurf.get_rect(center=self.rect.center)
        
        # Subtle text shadow
        shadowSurf = self.font.render(self.text, True, settings.COLORS["text_inverse"])
        shadowRect = textRect.copy()
        shadowRect.x += 1
        shadowRect.y += 1
        surface.blit(shadowSurf, shadowRect)
        
        surface.blit(textSurf, textRect)

    def _interpolateColor(self, color1, color2, factor):
        """Interpolate between two colors."""
        return (
            int(color1[0] + (color2[0] - color1[0]) * factor),
            int(color1[1] + (color2[1] - color1[1]) * factor),
            int(color1[2] + (color2[2] - color1[2]) * factor)
        )

    def setPosition(self, x, y):
        """Move button to new coordinates."""
        self.rect.x = x
        self.rect.y = y

    def setText(self, text):
        """Update button label."""
        self.text = text
