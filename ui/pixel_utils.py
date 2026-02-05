"""True pixel art utilities for crisp pixel-perfect graphics."""

import pygame
import settings


class PixelArtist:
    """Creates true pixel art graphics drawn pixel by pixel."""
    
    @staticmethod
    def draw_pixel_button(surface, rect, base_color, border_color, pressed=False, hovered=False):
        """Draw a pixel art button with slight rounding at corners.
        
        Args:
            surface: Pygame surface to draw on
            rect: Button rectangle (x, y, width, height)
            base_color: Main button color
            border_color: Border color
            pressed: Whether button is pressed (inset look)
            hovered: Whether button is hovered
        """
        x, y, w, h = rect
        
        # Slightly adjust colors for hover effect
        if hovered and not pressed:
            base_color = (
                min(255, base_color[0] + 20),
                min(255, base_color[1] + 20),
                min(255, base_color[2] + 20)
            )
        
        # Draw the main body with slight corner rounding (pixel art style)
        # Corners are 2 pixels cut off for slight rounding
        for row in range(h):
            for col in range(w):
                # Skip corner pixels for slight rounding
                if (row < 2 and col < 2) or \
                   (row < 2 and col >= w - 2) or \
                   (row >= h - 2 and col < 2) or \
                   (row >= h - 2 and col >= w - 2):
                    continue
                
                # Draw pixel
                pixel_x = x + col
                pixel_y = y + row
                
                # Determine if this is a border pixel
                is_border = (row < 2 or row >= h - 2 or col < 2 or col >= w - 2)
                
                if is_border:
                    # Border with 3D bevel effect
                    if pressed:
                        # Inset border - dark on top/left, light on bottom/right
                        if row < h // 2 or col < w // 2:
                            color = (
                                max(0, border_color[0] - 30),
                                max(0, border_color[1] - 30),
                                max(0, border_color[2] - 30)
                            )
                        else:
                            color = (
                                min(255, border_color[0] + 20),
                                min(255, border_color[1] + 20),
                                min(255, border_color[2] + 20)
                            )
                    else:
                        # Raised border - light on top/left, dark on bottom/right
                        if row < h // 2 or col < w // 2:
                            color = (
                                min(255, border_color[0] + 40),
                                min(255, border_color[1] + 40),
                                min(255, border_color[2] + 40)
                            )
                        else:
                            color = (
                                max(0, border_color[0] - 20),
                                max(0, border_color[1] - 20),
                                max(0, border_color[2] - 20)
                            )
                    
                    surface.set_at((pixel_x, pixel_y), color)
                else:
                    surface.set_at((pixel_x, pixel_y), base_color)
    
    @staticmethod
    def draw_pixel_text(surface, text, x, y, color, size='medium'):
        """Draw pixel art text character by character.
        
        Args:
            surface: Pygame surface
            text: String to draw
            x, y: Top-left position
            color: RGB color tuple
            size: 'small', 'medium', 'large'
        """
        sizes = {'small': 1, 'medium': 2, 'large': 3}
        scale = sizes.get(size, 2)
        
        # Simple 5x7 pixel font definitions
        font_5x7 = {
            'A': [
                "  XXX  ",
                " X   X ",
                " X   X ",
                " XXXXX ",
                " X   X ",
                " X   X ",
                " X   X ",
            ],
            'B': [
                " XXXX  ",
                " X   X ",
                " X   X ",
                " XXXX  ",
                " X   X ",
                " X   X ",
                " XXXX  ",
            ],
            'C': [
                "  XXXX ",
                " X     ",
                " X     ",
                " X     ",
                " X     ",
                " X     ",
                "  XXXX ",
            ],
            'D': [
                " XXXX  ",
                " X   X ",
                " X   X ",
                " X   X ",
                " X   X ",
                " X   X ",
                " XXXX  ",
            ],
            'E': [
                " XXXXX ",
                " X     ",
                " X     ",
                " XXXX  ",
                " X     ",
                " X     ",
                " XXXXX ",
            ],
            'F': [
                " XXXXX ",
                " X     ",
                " X     ",
                " XXXX  ",
                " X     ",
                " X     ",
                " X     ",
            ],
            'G': [
                "  XXXX ",
                " X     ",
                " X     ",
                " X  XX ",
                " X   X ",
                " X   X ",
                "  XXXX ",
            ],
            'H': [
                " X   X ",
                " X   X ",
                " X   X ",
                " XXXXX ",
                " X   X ",
                " X   X ",
                " X   X ",
            ],
            'I': [
                " XXXXX ",
                "   X   ",
                "   X   ",
                "   X   ",
                "   X   ",
                "   X   ",
                " XXXXX ",
            ],
            'J': [
                " XXXXX ",
                "    X  ",
                "    X  ",
                "    X  ",
                " X  X  ",
                " X  X  ",
                "  XX   ",
            ],
            'K': [
                " X   X ",
                " X  X  ",
                " X X   ",
                " XX    ",
                " X X   ",
                " X  X  ",
                " X   X ",
            ],
            'L': [
                " X     ",
                " X     ",
                " X     ",
                " X     ",
                " X     ",
                " X     ",
                " XXXXX ",
            ],
            'M': [
                " X   X ",
                " XX XX ",
                " X X X ",
                " X   X ",
                " X   X ",
                " X   X ",
                " X   X ",
            ],
            'N': [
                " X   X ",
                " XX  X ",
                " X X X ",
                " X  XX ",
                " X   X ",
                " X   X ",
                " X   X ",
            ],
            'O': [
                "  XXX  ",
                " X   X ",
                " X   X ",
                " X   X ",
                " X   X ",
                " X   X ",
                "  XXX  ",
            ],
            'P': [
                " XXXX  ",
                " X   X ",
                " X   X ",
                " XXXX  ",
                " X     ",
                " X     ",
                " X     ",
            ],
            'Q': [
                "  XXX  ",
                " X   X ",
                " X   X ",
                " X   X ",
                " X X X ",
                " X  X  ",
                "  XX X ",
            ],
            'R': [
                " XXXX  ",
                " X   X ",
                " X   X ",
                " XXXX  ",
                " X X   ",
                " X  X  ",
                " X   X ",
            ],
            'S': [
                "  XXXX ",
                " X     ",
                " X     ",
                "  XXX  ",
                "     X ",
                "     X ",
                " XXXX  ",
            ],
            'T': [
                " XXXXX ",
                "   X   ",
                "   X   ",
                "   X   ",
                "   X   ",
                "   X   ",
                "   X   ",
            ],
            'U': [
                " X   X ",
                " X   X ",
                " X   X ",
                " X   X ",
                " X   X ",
                " X   X ",
                "  XXX  ",
            ],
            'V': [
                " X   X ",
                " X   X ",
                " X   X ",
                " X   X ",
                " X   X ",
                "  X X  ",
                "   X   ",
            ],
            'W': [
                " X   X ",
                " X   X ",
                " X   X ",
                " X X X ",
                " X X X ",
                " XX XX ",
                " X   X ",
            ],
            'X': [
                " X   X ",
                " X   X ",
                "  X X  ",
                "   X   ",
                "  X X  ",
                " X   X ",
                " X   X ",
            ],
            'Y': [
                " X   X ",
                " X   X ",
                " X   X ",
                "  X X  ",
                "   X   ",
                "   X   ",
                "   X   ",
            ],
            'Z': [
                " XXXXX ",
                "    X  ",
                "   X   ",
                "  X    ",
                " X     ",
                " X     ",
                " XXXXX ",
            ],
            '0': [
                "  XXX  ",
                " X  XX ",
                " X X X ",
                " X X X ",
                " X X X ",
                " XX  X ",
                "  XXX  ",
            ],
            '1': [
                "   X   ",
                "  XX   ",
                "   X   ",
                "   X   ",
                "   X   ",
                "   X   ",
                " XXXXX ",
            ],
            '2': [
                "  XXX  ",
                " X   X ",
                "     X ",
                "    X  ",
                "   X   ",
                "  X    ",
                " XXXXX ",
            ],
            '3': [
                "  XXX  ",
                " X   X ",
                "     X ",
                "   XX  ",
                "     X ",
                " X   X ",
                "  XXX  ",
            ],
            '4': [
                "    X  ",
                "   XX  ",
                "  X X  ",
                " X  X  ",
                " XXXXX ",
                "    X  ",
                "    X  ",
            ],
            '5': [
                " XXXXX ",
                " X     ",
                " XXXX  ",
                "     X ",
                "     X ",
                " X   X ",
                "  XXX  ",
            ],
            '6': [
                "  XXX  ",
                " X     ",
                " X     ",
                " XXXX  ",
                " X   X ",
                " X   X ",
                "  XXX  ",
            ],
            '7': [
                " XXXXX ",
                "     X ",
                "    X  ",
                "   X   ",
                "   X   ",
                "   X   ",
                "   X   ",
            ],
            '8': [
                "  XXX  ",
                " X   X ",
                " X   X ",
                "  XXX  ",
                " X   X ",
                " X   X ",
                "  XXX  ",
            ],
            '9': [
                "  XXX  ",
                " X   X ",
                " X   X ",
                "  XXXX ",
                "     X ",
                "    X  ",
                "  XX   ",
            ],
            ':': [
                "       ",
                "       ",
                "   X   ",
                "       ",
                "       ",
                "   X   ",
                "       ",
            ],
            ' ': [
                "       ",
                "       ",
                "       ",
                "       ",
                "       ",
                "       ",
                "       ",
            ],
            '-': [
                "       ",
                "       ",
                "       ",
                " XXXXX ",
                "       ",
                "       ",
                "       ",
            ],
            '(': [
                "   X   ",
                "  X    ",
                " X     ",
                " X     ",
                " X     ",
                "  X    ",
                "   X   ",
            ],
            ')': [
                "   X   ",
                "    X  ",
                "     X ",
                "     X ",
                "     X ",
                "    X  ",
                "   X   ",
            ],
            'x': [
                "       ",
                "       ",
                " X   X ",
                "  X X  ",
                "   X   ",
                "  X X  ",
                " X   X ",
            ],
        }
        
        char_width = 7 * scale
        char_height = 7 * scale
        spacing = 2 * scale
        
        current_x = x
        for char in text.upper():
            if char in font_5x7:
                pattern = font_5x7[char]
                for row_idx, row in enumerate(pattern):
                    for col_idx, pixel in enumerate(row):
                        if pixel == 'X':
                            # Draw scaled pixel
                            for dy in range(scale):
                                for dx in range(scale):
                                    surface.set_at((
                                        current_x + col_idx * scale + dx,
                                        y + row_idx * scale + dy
                                    ), color)
            current_x += char_width + spacing
    
    @staticmethod
    def draw_pixel_mine(surface, x, y, size):
        """Draw a pixel art mine (bomb).
        
        Args:
            surface: Pygame surface
            x, y: Top-left position
            size: Size of the mine area
        """
        center_x = x + size // 2
        center_y = y + size // 2
        
        # Mine body (circle-ish pixel shape)
        mine_color = settings.COLORS["mine"]
        
        # Draw the main body (3x3 center)
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                surface.set_at((center_x + dx, center_y + dy), mine_color)
        
        # Add spikes
        spikes = [
            (0, -3), (0, 3),  # Vertical
            (-3, 0), (3, 0),  # Horizontal
            (-2, -2), (2, -2), (-2, 2), (2, 2),  # Diagonal
        ]
        for dx, dy in spikes:
            surface.set_at((center_x + dx, center_y + dy), mine_color)
    
    @staticmethod
    def draw_pixel_flag(surface, x, y, size):
        """Draw a pixel art flag.
        
        Args:
            surface: Pygame surface
            x, y: Top-left position
            size: Size of the flag area
        """
        flag_color = settings.COLORS["flag"]
        pole_color = (180, 180, 180)  # Light gray
        
        center_x = x + size // 2
        base_y = y + size - 3
        top_y = y + 3
        
        # Draw pole
        for py in range(top_y, base_y + 1):
            surface.set_at((center_x, py), pole_color)
        
        # Draw flag (triangle)
        flag_points = [
            (center_x + 1, top_y),
            (center_x + 1, top_y + 4),
            (center_x + 5, top_y + 2),
        ]
        # Fill triangle
        for dy in range(5):
            width = 5 - dy if dy < 3 else 1
            for dx in range(width):
                surface.set_at((center_x + 1 + dx, top_y + dy), flag_color)
    
    @staticmethod
    def draw_smiley(surface, x, y, size, expression='happy'):
        """Draw a pixel art smiley face.
        
        Args:
            surface: Pygame surface
            x, y: Top-left position
            size: Size of smiley
            expression: 'happy', 'sad', 'neutral'
        """
        color = settings.COLORS["accent"]
        
        # Face outline (square with slight rounding)
        face_pixels = []
        center_x = x + size // 2
        center_y = y + size // 2
        
        # Draw face border
        for i in range(size):
            for j in range(size):
                # Skip corners for slight rounding
                if (i < 2 and j < 2) or (i < 2 and j >= size - 2) or \
                   (i >= size - 2 and j < 2) or (i >= size - 2 and j >= size - 2):
                    continue
                # Border
                if i < 2 or i >= size - 2 or j < 2 or j >= size - 2:
                    surface.set_at((x + j, y + i), color)
        
        # Eyes (two pixels)
        left_eye_x = center_x - 3
        right_eye_x = center_x + 2
        eye_y = center_y - 2
        surface.set_at((left_eye_x, eye_y), color)
        surface.set_at((right_eye_x, eye_y), color)
        
        # Mouth
        if expression == 'happy':
            # Smile
            mouth_pixels = [
                (center_x - 3, center_y + 2),
                (center_x - 2, center_y + 3),
                (center_x - 1, center_y + 3),
                (center_x, center_y + 3),
                (center_x + 1, center_y + 3),
                (center_x + 2, center_y + 2),
            ]
        elif expression == 'sad':
            # Frown
            mouth_pixels = [
                (center_x - 3, center_y + 3),
                (center_x - 2, center_y + 2),
                (center_x - 1, center_y + 2),
                (center_x, center_y + 2),
                (center_x + 1, center_y + 2),
                (center_x + 2, center_y + 3),
            ]
        else:
            # Neutral
            mouth_pixels = [
                (center_x - 2, center_y + 2),
                (center_x - 1, center_y + 2),
                (center_x, center_y + 2),
                (center_x + 1, center_y + 2),
            ]
        
        for px, py in mouth_pixels:
            surface.set_at((px, py), color)


# Global pixel artist instance
pixel_artist = PixelArtist()


def draw_pixel_button(surface, rect, base_color, border_color, pressed=False, hovered=False):
    """Convenience function for drawing pixel buttons."""
    pixel_artist.draw_pixel_button(surface, rect, base_color, border_color, pressed, hovered)


def draw_pixel_text(surface, text, x, y, color, size='medium'):
    """Convenience function for drawing pixel text."""
    pixel_artist.draw_pixel_text(surface, text, x, y, color, size)


def draw_pixel_mine(surface, x, y, size):
    """Convenience function for drawing pixel mine."""
    pixel_artist.draw_pixel_mine(surface, x, y, size)


def draw_pixel_flag(surface, x, y, size):
    """Convenience function for drawing pixel flag."""
    pixel_artist.draw_pixel_flag(surface, x, y, size)


def draw_smiley(surface, x, y, size, expression='happy'):
    """Convenience function for drawing pixel smiley."""
    pixel_artist.draw_smiley(surface, x, y, size, expression)


def get_pixel_text_width(text, size='medium'):
    """Calculate the width of pixel text in pixels.
    
    Args:
        text: String to measure
        size: 'small', 'medium', 'large'
        
    Returns:
        Width in pixels
    """
    sizes = {'small': 1, 'medium': 2, 'large': 3}
    scale = sizes.get(size, 2)
    char_width = 7 * scale
    spacing = 2 * scale
    return len(text) * char_width + (len(text) - 1) * spacing


def get_pixel_text_height(size='medium'):
    """Calculate the height of pixel text in pixels.
    
    Args:
        size: 'small', 'medium', 'large'
        
    Returns:
        Height in pixels
    """
    sizes = {'small': 1, 'medium': 2, 'large': 3}
    scale = sizes.get(size, 2)
    return 7 * scale
