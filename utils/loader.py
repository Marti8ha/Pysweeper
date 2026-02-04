"""Asset loader for images, fonts, and sounds with caching."""

import pygame
from utils.assets import AssetGenerator


class AssetLoader:
    """Centralized asset management with lazy loading and caching."""

    def __init__(self, tile_size: int = 36):
        self.images = {}
        self.fonts = {};
        self.sounds = {}
        self.basePath = "assets/"
        # Initialize asset generator for programmatic assets
        self.asset_generator = AssetGenerator(tile_size)

    def loadImage(self, path, key=None):
        """Load and cache an image file.

        Args:
            path: relative path from assets/images/ OR special key like "flag", "mine"
            key: optional cache key (defaults to path)

        Returns:
            pygame.Surface object
        """
        key = key or path
        if key not in self.images:
            # Check for special generated assets first
            if key in ["unrevealed", "revealed", "flag", "mine", "mine_exploded",
                       "wrong_flag", "restart_normal", "restart_dead", "restart_win"]:
                self.images[key] = self.asset_generator.get(key)
            elif any(key.startswith(prefix) for prefix in ["revealed_", "digit_"]):
                self.images[key] = self.asset_generator.get(key)
            else:
                # Try to load from file, fall back to generated asset
                fullPath = self.basePath + "images/" + path
                try:
                    self.images[key] = pygame.image.load(fullPath).convert_alpha()
                except pygame.error:
                    # Fall back to generated asset based on key
                    self.images[key] = self._generate_fallback(key)
        return self.images[key]

    def _generate_fallback(self, key: str) -> pygame.Surface:
        """Generate fallback asset when file not found."""
        try:
            return self.asset_generator.get(key)
        except ValueError:
            return self.asset_generator.createPlaceholderSurface(32, 32)

    def loadFont(self, name, size, key=None):
        """Load and cache a font.

        Args:
            name: font filename or None for default font
            size: font size in points
            key: optional cache key

        Returns:
            pygame.font.Font object
        """
        key = key or f"{name}_{size}"
        if key not in self.fonts:
            if name:
                fullPath = self.basePath + "fonts/" + name
                self.fonts[key] = pygame.font.Font(fullPath, size)
            else:
                self.fonts[key] = pygame.font.Font(None, size)
        return self.fonts[key]

    def loadSound(self, path, key=None):
        """Load and cache a sound file.

        Args:
            path: relative path from assets/sounds/
            key: optional cache key

        Returns:
            pygame.mixer.Sound object
        """
        key = key or path
        if key not in self.sounds:
            fullPath = self.basePath + "sounds/" + path
            try:
                self.sounds[key] = pygame.mixer.Sound(fullPath)
            except pygame.error:
                self.sounds[key] = None
        return self.sounds[key]

    def createPlaceholderSurface(self, width, height, color=(128, 128, 128)):
        """Create a placeholder surface for missing assets."""
        surf = pygame.Surface((width, height))
        surf.fill(color)
        return surf

    def clearCache(self):
        """Clear all cached assets to free memory."""
        self.images.clear()
        self.fonts.clear()
        self.sounds.clear()

    def preloadCommonAssets(self):
        """Load frequently used assets upfront."""
        pass  # Uncomment when assets are available:
        # self.loadImage("tiles/covered.png", "tile_covered")
        # self.loadImage("tiles/revealed_0.png", "tile_0")
        # self.loadImage("tiles/revealed_1.png", "tile_1")
        # etc.


# Global asset loader instance
loader = AssetLoader()
