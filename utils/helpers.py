"""Utility functions for coordinate conversion and UI helpers."""


import pygame


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
    """Draw grid lines for visual board separation."""
    for r in range(rows + 1):
        y = startY + r * tileSize
        pygame.draw.line(surface, (128, 128, 128), (startX, y), (startX + cols * tileSize, y))

    for c in range(cols + 1):
        x = startX + c * tileSize
        pygame.draw.line(surface, (128, 128, 128), (x, startY), (x, startY + rows * tileSize))


def drawRaisedRect(surface, rect, color=(192, 192, 192)):
    """Draw a 3D raised rectangle effect."""
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, (255, 255, 255), rect, 2)
    pygame.draw.rect(surface, (128, 128, 128), (rect.right - 2, rect.top, 2, rect.height))
    pygame.draw.rect(surface, (128, 128, 128), (rect.left, rect.bottom - 2, rect.width, 2))


def drawPressedRect(surface, rect, color=(128, 128, 128)):
    """Draw a 3D pressed/depressed rectangle effect."""
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, (128, 128, 128), rect, 2)
    pygame.draw.rect(surface, (255, 255, 255), (rect.left, rect.top, rect.width, 2))
    pygame.draw.rect(surface, (255, 255, 255), (rect.left, rect.top, 2, rect.height))


def formatTime(seconds):
    """Convert seconds to MM:SS format."""
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02}:{secs:02}"


def clamp(value, minValue, maxValue):
    """Constrain a value within specified bounds."""
    return max(minValue, min(value, maxValue))
