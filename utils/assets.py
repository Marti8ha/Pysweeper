"""Programmatic placeholder image generation for Pysweeper game elements.

This module provides functions to generate placeholder images for all game assets
when actual image files are not available. Images are drawn using pygame shapes
with consistent dark theme styling.
"""

import pygame
import settings


def create_unrevealed_tile(size: int) -> pygame.Surface:
    """Create unrevealed tile with raised 3D button appearance."""
    surf = pygame.Surface((size, size))
    surf.fill(settings.COLORS["tile_unrevealed"])
    
    # Light border (top and left) for 3D effect
    pygame.draw.line(surf, settings.COLORS["tile_border_light"],
                     (0, 0), (size, 0), 3)
    pygame.draw.line(surf, settings.COLORS["tile_border_light"],
                     (0, 0), (0, size), 3)
    
    # Dark border (bottom and right) for 3D effect
    pygame.draw.line(surf, settings.COLORS["tile_border_dark"],
                     (0, size - 1), (size, size - 1), 2)
    pygame.draw.line(surf, settings.COLORS["tile_border_dark"],
                     (size - 1, 0), (size - 1, size), 2)
    
    return surf


def create_revealed_tile(size: int, show_mines: bool = False, 
                         is_mine: bool = False) -> pygame.Surface:
    """Create revealed tile with flat appearance.
    
    Args:
        size: tile size in pixels
        show_mines: whether to show mine indicator
        is_mine: whether this tile contains a mine
    """
    surf = pygame.Surface((size, size))
    surf.fill(settings.COLORS["tile_revealed"])
    
    # Subtle inner border for revealed tile
    pygame.draw.rect(surf, settings.COLORS["tile_border_dark"], 
                     (0, 0, size, size), 1)
    
    # Show mine if flagged
    if show_mines and is_mine:
        # Draw mine circle
        center = (size // 2, size // 2)
        radius = size // 4
        pygame.draw.circle(surf, settings.COLORS["mine"], center, radius)
        
        # Inner detail
        pygame.draw.circle(surf, (200, 50, 50), center, radius - 4)
        
        # "X" mark
        padding = size // 6
        pygame.draw.line(surf, (50, 0, 0), 
                        (padding, padding), (size - padding, size - padding), 2)
        pygame.draw.line(surf, (50, 0, 0),
                        (size - padding, padding), (padding, size - padding), 2)
    
    return surf


def create_number_tile(number: int, size: int) -> pygame.Surface:
    """Create revealed tile with adjacent mine count number.
    
    Args:
        number: 0-8, the adjacent mine count
        size: tile size in pixels
    """
    surf = create_revealed_tile(size)
    
    if number == 0:
        return surf
    
    # Use appropriate font
    font_size = int(size * 0.7)
    try:
        font = pygame.font.Font("CascadiaMono-Bold.ttf", font_size)
    except (FileNotFoundError, IOError):
        font = pygame.font.Font(None, font_size)
    
    # Get number color from settings
    color = settings.NUMBER_COLORS.get(number, settings.COLORS["text_primary"])
    
    # Render number
    text = font.render(str(number), True, color)
    text_rect = text.get_rect(center=(size // 2, size // 2))
    surf.blit(text, text_rect)
    
    return surf


def create_mine_tile(size: int, exploded: bool = False) -> pygame.Surface:
    """Create mine tile with mine indicator.
    
    Args:
        size: tile size in pixels
        exploded: whether mine has exploded (red background)
    """
    surf = pygame.Surface((size, size))
    
    if exploded:
        surf.fill((180, 50, 50))  # Red background for exploded mine
    else:
        surf.fill(settings.COLORS["tile_revealed"])
    
    # Draw mine circle
    center = (size // 2, size // 2)
    radius = size // 3
    
    # Outer circle
    pygame.draw.circle(surf, settings.COLORS["mine"], center, radius)
    
    # Inner highlight
    highlight_color = (255, 100, 100)
    pygame.draw.circle(surf, highlight_color, (center[0] - 2, center[1] - 2), radius - 4)
    
    # "M" letter
    font_size = int(size * 0.5)
    try:
        font = pygame.font.Font("CascadiaMono-Bold.ttf", font_size)
    except (FileNotFoundError, IOError):
        font = pygame.font.Font(None, font_size)
    
    text = font.render("M", True, (20, 20, 20))
    text_rect = text.get_rect(center=center)
    surf.blit(text, text_rect)
    
    return surf


def create_flag_tile(size: int) -> pygame.Surface:
    """Create flag tile with red flag indicator.
    
    Args:
        size: tile size in pixels
    """
    surf = create_revealed_tile(size)
    
    # Draw flag pole (left side)
    pole_x = size // 3
    pole_top = size // 6
    pole_bottom = size - size // 6
    pygame.draw.line(surf, (200, 200, 200), 
                    (pole_x, pole_top), (pole_x, pole_bottom), 3)
    
    # Draw flag (triangle)
    flag_color = settings.COLORS["flag"]
    pole_right = pole_x + size // 3
    flag_top = pole_top + size // 12
    flag_mid_y = size // 2
    flag_bottom = size - size // 6
    
    flag_points = [
        (pole_x, pole_top),      # Top at pole
        (pole_right, flag_mid_y),  # Right point
        (pole_x, flag_bottom),     # Bottom at pole
    ]
    pygame.draw.polygon(surf, flag_color, flag_points)
    
    # Flag outline
    pygame.draw.polygon(surf, (150, 100, 0), flag_points, 2)
    
    return surf


def create_wrong_flag_tile(size: int) -> pygame.Surface:
    """Create wrong flag indicator (shows where player wrongly flagged).
    
    Args:
        size: tile size in pixels
    """
    surf = create_revealed_tile(size)
    
    # Draw green checkmark
    check_color = settings.COLORS["win"]
    padding = size // 4
    
    # Checkmark points
    start_x = padding
    mid_x = size // 2
    end_x = size - padding
    top_y = size // 2
    bottom_y = size - padding
    
    pygame.draw.line(surf, check_color, (start_x, top_y), (mid_x, bottom_y), 4)
    pygame.draw.line(surf, check_color, (mid_x, bottom_y), (end_x, padding), 4)
    
    return surf


def create_restart_button(size: int, state: str = "normal") -> pygame.Surface:
    """Create restart button face.
    
    Args:
        size: button size in pixels
        state: "normal", "dead", or "win"
    
    Returns:
        pygame.Surface with drawn face
    """
    surf = pygame.Surface((size, size))
    surf.fill(settings.COLORS["hud_background"])
    
    # Face background circle
    center = (size // 2, size // 2)
    radius = size // 2 - 4
    
    face_color = settings.COLORS["accent"]
    if state == "dead":
        face_color = settings.COLORS["lose"]
    elif state == "win":
        face_color = settings.COLORS["win"]
    
    pygame.draw.circle(surf, (60, 60, 60), center, radius)
    pygame.draw.circle(surf, face_color, center, radius, 2)
    
    # Get font for face
    font_size = int(size * 0.7)
    try:
        font = pygame.font.Font("CascadiaMono-Bold.ttf", font_size)
    except (FileNotFoundError, IOError):
        font = pygame.font.Font(None, font_size)
    
    # Draw face based on state
    if state == "normal":
        # Happy face ":-)"
        face_text = ":-)"
        color = settings.COLORS["text_primary"]
    elif state == "dead":
        # Dead face "X_X"
        face_text = "X_X"
        color = settings.COLORS["lose"]
    elif state == "win":
        # Cool face "B-)"
        face_text = "B-)"
        color = settings.COLORS["win"]
    else:
        face_text = ":-)"
        color = settings.COLORS["text_primary"]
    
    text = font.render(face_text, True, color)
    text_rect = text.get_rect(center=center)
    surf.blit(text, text_rect)
    
    return surf


def create_digit(digit: int, size: int = 36, color: tuple = (255, 200, 100)) -> pygame.Surface:
    """Create a single digit image for HUD counters.
    
    Args:
        digit: 0-9, the digit to draw
        size: digit size in pixels
        color: RGB color tuple
        
    Returns:
        pygame.Surface with the digit drawn
    """
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Use font for digit
    font_size = int(size * 0.8)
    try:
        font = pygame.font.Font("CascadiaMono-Bold.ttf", font_size)
    except (FileNotFoundError, IOError):
        font = pygame.font.Font(None, font_size)
    
    text = font.render(str(digit), True, color)
    text_rect = text.get_rect(center=(size // 2, size // 2))
    
    # For transparency, create a transparent surface and blit
    temp_surf = pygame.Surface(text.get_size(), pygame.SRCALPHA)
    temp_surf.blit(text, (0, 0))
    
    # Blit centered onto the main surface
    offset_x = (size - text.get_width()) // 2
    offset_y = (size - text.get_height()) // 2
    surf.blit(temp_surf, (offset_x, offset_y))
    
    return surf


def create_hud_number(number: int, width: int = 3, 
                      size: int = 36, color = None) -> pygame.Surface:
    """Create a multi-digit number for HUD display.
    
    Args:
        number: the number to display
        width: minimum number of digits (for zero-padding)
        size: digit size in pixels
        color: RGB color tuple (defaults to flag orange)
    
    Returns:
        pygame.Surface with the full number
    """
    if color is None:
        color = settings.COLORS["flag"]
    
    digit_surf = create_digit(0, size, color)
    digit_width = digit_surf.get_width()
    
    # Create surface for full number
    num_str = str(number).zfill(width)
    total_width = digit_width * len(num_str)
    surf = pygame.Surface((total_width, size))
    surf.fill((0, 0, 0))  # Transparent background for blitting
    
    for i, char in enumerate(num_str):
        digit = int(char)
        digit_img = create_digit(digit, size, color)
        surf.blit(digit_img, (i * digit_width, 0))
    
    return surf


def generate_all_assets(tile_size: int = 36) -> dict:
    """Generate all game assets and return as dictionary.
    
    Args:
        tile_size: size of tiles in pixels
    
    Returns:
        Dictionary mapping asset names to pygame.Surface objects
    """
    assets = {}
    
    # Tile states
    assets["unrevealed"] = create_unrevealed_tile(tile_size)
    assets["revealed"] = create_revealed_tile(tile_size)
    assets["revealed_0"] = create_number_tile(0, tile_size)
    
    # Number tiles 1-8
    for i in range(1, 9):
        assets[f"revealed_{i}"] = create_number_tile(i, tile_size)
    
    # Special tiles
    assets["mine"] = create_mine_tile(tile_size)
    assets["mine_exploded"] = create_mine_tile(tile_size, exploded=True)
    assets["flag"] = create_flag_tile(tile_size)
    assets["wrong_flag"] = create_wrong_flag_tile(tile_size)
    
    # Restart button states
    button_size = 50  # HUD restart button size
    assets["restart_normal"] = create_restart_button(button_size, "normal")
    assets["restart_dead"] = create_restart_button(button_size, "dead")
    assets["restart_win"] = create_restart_button(button_size, "win")
    
    # HUD digits
    hud_digit_size = 36
    for i in range(10):
        assets[f"digit_{i}"] = create_digit(i, hud_digit_size)
    
    return assets


class AssetGenerator:
    """Generator for programmatic game assets."""
    
    def __init__(self, tile_size: int = 36):
        """Initialize asset generator.
        
        Args:
            tile_size: default tile size in pixels
        """
        self.tile_size = tile_size
        self._cache = {}
    
    def get(self, name: str) -> pygame.Surface:
        """Get an asset by name, generating if needed.
        
        Args:
            name: asset name (e.g., "unrevealed", "flag", "digit_5")
        
        Returns:
            pygame.Surface for the asset
        """
        if name not in self._cache:
            self._cache[name] = self._generate(name)
        return self._cache[name]
    
    def _generate(self, name: str) -> pygame.Surface:
        """Generate a specific asset.
        
        Args:
            name: asset name
        
        Returns:
            Generated pygame.Surface
        """
        # Handle tile numbers
        if name == "unrevealed":
            return create_unrevealed_tile(self.tile_size)
        elif name == "revealed":
            return create_revealed_tile(self.tile_size)
        elif name.startswith("revealed_"):
            number = int(name.split("_")[1])
            return create_number_tile(number, self.tile_size)
        
        # Handle special tiles
        elif name == "mine":
            return create_mine_tile(self.tile_size)
        elif name == "mine_exploded":
            return create_mine_tile(self.tile_size, exploded=True)
        elif name == "flag":
            return create_flag_tile(self.tile_size)
        elif name == "wrong_flag":
            return create_wrong_flag_tile(self.tile_size)
        
        # Handle restart buttons
        elif name == "restart_normal":
            return create_restart_button(50, "normal")
        elif name == "restart_dead":
            return create_restart_button(50, "dead")
        elif name == "restart_win":
            return create_restart_button(50, "win")
        
        # Handle digits
        elif name.startswith("digit_"):
            digit = int(name.split("_")[1])
            return create_digit(digit)
        
        # Handle HUD numbers
        elif name.startswith("hud_"):
            # e.g., "hud_042" -> number 42 with 3 digits
            parts = name.split("_")[1:]
            if len(parts) == 1:
                number = int(parts[0])
                width = len(str(number))
            else:
                number = int(parts[1])
                width = int(parts[0])
            return create_hud_number(number, width)
        
        raise ValueError(f"Unknown asset name: {name}")
    
    def preload_all(self) -> dict:
        """Generate and cache all assets.
        
        Returns:
            Dictionary of all assets
        """
        assets = generate_all_assets(self.tile_size)
        self._cache.update(assets)
        return assets
    
    def clear_cache(self):
        """Clear the asset cache."""
        self._cache.clear()
    
    def createPlaceholderSurface(self, width: int, height: int, 
                                  color: tuple = (128, 128, 128)) -> pygame.Surface:
        """Create a simple placeholder surface.
        
        Args:
            width: surface width
            height: surface height
            color: RGB color tuple
            
        Returns:
            pygame.Surface with placeholder color
        """
        surf = pygame.Surface((width, height))
        surf.fill(color)
        return surf


# Example usage and demonstration
if __name__ == "__main__":
    """Demo script showing how to use the asset generator."""
    import os
    
    # Initialize pygame for font access
    pygame.init()
    
    # Create generator with default tile size
    generator = AssetGenerator(tile_size=36)
    
    # Generate all assets
    print("Generating all Pysweeper assets...")
    assets = generator.preload_all()
    
    # Save all assets as PNG files for reference
    output_dir = "generated_assets"
    os.makedirs(output_dir, exist_ok=True)
    
    for name, surface in assets.items():
        # Scale up for visibility
        scale = 2 if "digit" not in name else 3
        scaled = pygame.transform.scale(surface, 
                                        (surface.get_width() * scale, 
                                         surface.get_height() * scale))
        pygame.image.save(scaled, f"{output_dir}/{name}.png")
    
    print(f"Generated {len(assets)} assets in {output_dir}/")
    print("\nAsset names:")
    for name in sorted(assets.keys()):
        print(f"  - {name}")
    
    print("\nUsage in game code:")
    print("""
    from utils.assets import AssetGenerator
    
    # Initialize with your tile size
    generator = AssetGenerator(tile_size=36)
    
    # Get individual assets
    unrevealed = generator.get("unrevealed")
    flag = generator.get("flag")
    number_5 = generator.get("revealed_5")
    
    # Get restart button
    restart_normal = generator.get("restart_normal")
    
    # Get HUD digits
    digit_7 = generator.get("digit_7")
    
    # Generate all at once
    all_assets = generator.preload_all()
    """)
