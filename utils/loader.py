"""Asset loader for images, fonts, and sounds with caching."""


import pygame


class AssetLoader:
    """Centralized asset management with lazy loading and caching."""

    def __init__(self):
        self.images = {}
        self.fonts = {}
        self.sounds = {}
        self.basePath = "assets/"

    def loadImage(self, path, key=None):
        """Load and cache an image file.

        Args:
            path: relative path from assets/images/
            key: optional cache key (defaults to path)

        Returns:
            pygame.Surface object
        """
        key = key or path
        if key not in self.images:
            fullPath = self.basePath + "images/" + path
            try:
                self.images[key] = pygame.image.load(fullPath).convert_alpha()
            except pygame.error:
                self.images[key] = self.createPlaceholderSurface(32, 32)
        return self.images[key]

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
