"""Reusable button component for menus and game interface."""

import pygame
import settings
from ui.pixel_utils import draw_pixel_text, draw_pixel_button, get_pixel_text_width, get_pixel_text_height


class Button:
    """Interactive button component with true pixel art styling."""

    # Padding around text inside button
    PADDING_X = 24
    PADDING_Y = 16

    def __init__(self, x, y, width, height, text, onClick=None):
        self.text = text
        self.onClick = onClick
        self.isHovered = False
        self.isPressed = False
        
        # Calculate size based on text if width/height not provided or too small
        text_width = get_pixel_text_width(text, size='medium')
        text_height = get_pixel_text_height(size='medium')
        
        min_width = text_width + self.PADDING_X * 2
        min_height = text_height + self.PADDING_Y * 2
        
        # Use provided dimensions if they're larger than minimum required
        final_width = max(width, min_width)
        final_height = max(height, min_height)
        
        self.rect = pygame.Rect(x, y, final_width, final_height)

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
        """Render true pixel art button to screen."""
        # Determine colors based on state
        if self.isPressed:
            baseColor = settings.COLORS["button_pressed"]
            borderColor = settings.COLORS["accent"]
        elif self.isHovered:
            baseColor = (
                min(255, settings.COLORS["button_background"][0] + 20),
                min(255, settings.COLORS["button_background"][1] + 20),
                min(255, settings.COLORS["button_background"][2] + 20)
            )
            borderColor = settings.COLORS["accent"]
        else:
            baseColor = settings.COLORS["button_background"]
            borderColor = settings.COLORS["button_border"]

        # Draw pixel art button with slight rounding and bevel
        draw_pixel_button(surface, self.rect, baseColor, borderColor, 
                         pressed=self.isPressed, hovered=self.isHovered)

        # Calculate text position (centered with slight offset when pressed)
        text_width = get_pixel_text_width(self.text, size='medium')
        text_height = get_pixel_text_height(size='medium')
        
        text_x = self.rect.x + (self.rect.width - text_width) // 2
        text_y = self.rect.y + (self.rect.height - text_height) // 2
        
        if self.isPressed:
            text_x += 1
            text_y += 1

        # Draw true pixel art text
        draw_pixel_text(surface, self.text, text_x, text_y, 
                       settings.COLORS["text_primary"], size='medium')

    def setPosition(self, x, y):
        """Move button to new coordinates."""
        self.rect.x = x
        self.rect.y = y

    def setText(self, text):
        """Update button label and recalculate size if needed."""
        self.text = text
        
        # Recalculate minimum required size
        text_width = get_pixel_text_width(text, size='medium')
        text_height = get_pixel_text_height(size='medium')
        
        min_width = text_width + self.PADDING_X * 2
        min_height = text_height + self.PADDING_Y * 2
        
        # Update rect if current size is too small
        if self.rect.width < min_width:
            self.rect.width = min_width
        if self.rect.height < min_height:
            self.rect.height = min_height
    
    def recenter(self, screen_width, screen_height, y_offset=0):
        """Center button horizontally on screen."""
        self.rect.x = (screen_width - self.rect.width) // 2
        self.rect.y = y_offset
