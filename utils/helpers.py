"""Utility functions for coordinate conversion and UI helpers."""

import pygame
import settings


def getTileFromMouse(pos, tileSize, offsetX=0, offsetY=0):
    """Convert pixel coordinates to grid position.

    Args:
        pos: (x, y) pixel coordinates
        tileSize: size of each tile in pixels
        offsetX: horizontal offset of board
        offsetY: vertical offset of board

    Returns:
        (row, col) tuple or None if outside board
    """
    x, y = pos
    col = (x - offsetX) // tileSize
    row = (y - offsetY) // tileSize
    return (row, col) if row >= 0 and col >= 0 else None


def centerText(surface, text, font, color, yOffset=0):
    """Render centered text on a surface.

    Args:
        surface: target surface to draw on
        text: string to render
        font: pygame font object
        color: RGB color tuple
        yOffset: vertical offset from center

    Returns:
        Rect of rendered text
    """
    textSurf = font.render(text, True, color)
    textRect = textSurf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 + yOffset))
    return surface.blit(textSurf, textRect)


def drawGridLines(surface, startX, startY, rows, cols, tileSize):
    """Draw subtle grid lines for visual board separation."""
    lineColor = settings.COLORS["tile_border_dark"]
    for r in range(rows + 1):
        y = startY + r * tileSize
        pygame.draw.line(surface, lineColor, (startX, y), (startX + cols * tileSize, y), 1)

    for c in range(cols + 1):
        x = startX + c * tileSize
        pygame.draw.line(surface, lineColor, (x, startY), (x, startY + rows * tileSize), 1)


def drawRaisedRect(surface, rect, color=None):
    """Draw a 3D raised rectangle effect with dark theme."""
    if color is None:
        color = settings.COLORS["tile_unrevealed"]
    
    # Main background
    pygame.draw.rect(surface, color, rect)
    
    # Light border (top and left)
    lightColor = settings.COLORS["tile_border_light"]
    pygame.draw.line(surface, lightColor, (rect.left, rect.top), (rect.right, rect.top), 2)
    pygame.draw.line(surface, lightColor, (rect.left, rect.top), (rect.left, rect.bottom), 2)
    
    # Dark border (bottom and right)
    darkColor = settings.COLORS["tile_border_dark"]
    pygame.draw.line(surface, darkColor, (rect.left, rect.bottom), (rect.right, rect.bottom), 2)
    pygame.draw.line(surface, darkColor, (rect.right, rect.top), (rect.right, rect.bottom), 2)


def drawPressedRect(surface, rect, color=None):
    """Draw a 3D pressed/depressed rectangle effect with dark theme."""
    if color is None:
        color = settings.COLORS["tile_revealed"]
    
    # Main background
    pygame.draw.rect(surface, color, rect)
    
    # Dark inner border (gives pressed appearance)
    darkColor = settings.COLORS["tile_border_dark"]
    pygame.draw.rect(surface, darkColor, rect, 1)


def formatTime(seconds):
    """Convert seconds to MM:SS format."""
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02}:{secs:02}"


def clamp(value, minValue, maxValue):
    """Constrain a value within specified bounds."""
    return max(minValue, min(value, maxValue))


def drawGlow(surface, rect, color, radius=10, intensity=100):
    """Draw a subtle glow effect around a rectangle.
    
    Args:
        surface: target surface
        rect: pygame.Rect or (x, y, width, height)
        color: RGB color tuple
        radius: glow radius in pixels
        intensity: glow intensity (0-255)
    """
    glowRect = pygame.Rect(rect)
    glowRect = glowRect.inflate(radius * 2, radius * 2)
    
    glowSurface = pygame.Surface(glowRect.size, pygame.SRCALPHA)
    pygame.draw.rect(glowSurface, (*color, intensity), glowSurface.get_rect(), border_radius=radius)
    surface.blit(glowSurface, glowRect.topleft)
