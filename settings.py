WIDTH = 800
HEIGHT = 800
FPS = 60

ROWS = 16
COLS = 16
MINES = 40

TILE_SIZE = 36
BOARD_OFFSET_X = 52
BOARD_OFFSET_Y = 80

# Dark Theme Color Palette
COLORS = {
    # Background colors
    "background": (18, 18, 18),
    "background_alt": (24, 24, 24),
    
    # Tile colors
    "tile_unrevealed": (45, 45, 45),
    "tile_revealed": (30, 30, 30),
    "tile_hover": (60, 60, 60),
    "tile_border_light": (70, 70, 70),
    "tile_border_dark": (25, 25, 25),
    
    # Text colors
    "text_primary": (220, 220, 220),
    "text_secondary": (160, 160, 160),
    "text_inverse": (18, 18, 18),
    
    # HUD colors
    "hud_background": (25, 25, 25),
    "hud_border": (50, 50, 50),
    
    # Accent colors
    "accent": (100, 200, 255),
    "accent_hover": (120, 220, 255),
    "accent_pressed": (80, 180, 230),
    
    # Button colors
    "button_background": (50, 50, 50),
    "button_hover": (65, 65, 65),
    "button_pressed": (40, 40, 40),
    "button_border": (80, 80, 80),
    
    # Number colors (neon/bright for visibility on dark)
    "number_1": (80, 255, 255),    # Cyan
    "number_2": (100, 255, 100),   # Bright Green
    "number_3": (255, 100, 100),   # Bright Red
    "number_4": (100, 150, 255),   # Blue
    "number_5": (255, 150, 50),    # Orange
    "number_6": (100, 255, 200),   # Teal
    "number_7": (255, 100, 200),   # Pink
    "number_8": (200, 200, 200),   # Light Grey
    
    # Game element colors
    "mine": (255, 80, 80),         # Bright Red
    "flag": (255, 180, 50),        # Orange
    "explosion": (255, 50, 50),    # Red
    
    # Overlay colors
    "overlay_background": (0, 0, 0, 180),
    "overlay_border": (100, 100, 100),
    
    # Win/Lose colors
    "win": (100, 255, 100),        # Bright Green
    "lose": (255, 80, 80),         # Bright Red
}

# Number color mapping for easy access
NUMBER_COLORS = {
    1: COLORS["number_1"],
    2: COLORS["number_2"],
    3: COLORS["number_3"],
    4: COLORS["number_4"],
    5: COLORS["number_5"],
    6: COLORS["number_6"],
    7: COLORS["number_7"],
    8: COLORS["number_8"],
}
