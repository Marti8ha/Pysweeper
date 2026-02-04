"""Reusable button component for menus and game interface."""


import pygame


class Button:
    """Interactive button component with hover and click states."""

    def __init__(self, x, y, width, height, text, onClick=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.onClick = onClick
        self.isHovered = False
        self.isPressed = False
        self.font = pygame.font.Font(None, 32)

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
        """Render button to screen."""
        # Button colors based on state
        if self.isPressed:
            color = (100, 100, 100)
            offset = 2
        elif self.isHovered:
            color = (170, 170, 170)
            offset = 0
        else:
            color = (192, 192, 192)
            offset = 0

        # Draw button face
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)

        # Draw text
        textSurf = self.font.render(self.text, True, (0, 0, 0))
        textRect = textSurf.get_rect(center=self.rect.center)
        surface.blit(textSurf, textRect)

    def setPosition(self, x, y):
        """Move button to new coordinates."""
        self.rect.x = x
        self.rect.y = y

    def setText(self, text):
        """Update button label."""
        self.text = text
