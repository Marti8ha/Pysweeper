"""Example: How to use the asset generator in Pysweeper game.

This file demonstrates various ways to use utils/assets.py for generating
placeholder game graphics programmatically.
"""

# =============================================================================
# SIMPLE USAGE - Get individual assets
# =============================================================================

def simple_usage_example():
    """Quick way to get specific assets."""
    from utils.assets import AssetGenerator
    
    # Create generator with tile size from settings
    generator = AssetGenerator(tile_size=36)
    
    # Get individual tile assets
    unrevealed = generator.get("unrevealed")       # Raised button appearance
    revealed = generator.get("revealed")           # Flat appearance
    revealed_1 = generator.get("revealed_1")       # Number 1 on tile
    revealed_5 = generator.get("revealed_5")       # Number 5 on tile
    
    # Get special tiles
    mine = generator.get("mine")                   # Mine indicator
    flag = generator.get("flag")                   # Flag indicator
    
    # Get restart button states
    restart_normal = generator.get("restart_normal")  # Happy face
    restart_dead = generator.get("restart_dead")     # Dead face (game over)
    restart_win = generator.get("restart_win")       # Cool face (win)
    
    # Get HUD digits
    digit_0 = generator.get("digit_0")             # Individual digit 0
    digit_9 = generator.get("digit_9")             # Individual digit 9
    
    return {
        "unrevealed": unrevealed, "revealed": revealed,
        "mine": mine, "flag": flag,
        "restart_normal": restart_normal
    }


# =============================================================================
# BATCH USAGE - Generate all assets at once
# =============================================================================

def batch_usage_example():
    """Generate all assets for the game."""
    from utils.assets import generate_all_assets
    
    # Generate all assets with default tile size (36px)
    all_assets = generate_all_assets(tile_size=36)
    
    # Access assets by name
    tile_unrevealed = all_assets["unrevealed"]
    tile_revealed_3 = all_assets["revealed_3"]
    tile_mine = all_assets["mine"]
    tile_flag = all_assets["flag"]
    
    # Access restart buttons
    btn_normal = all_assets["restart_normal"]
    btn_dead = all_assets["restart_dead"]
    btn_win = all_assets["restart_win"]
    
    # Access HUD digits
    hud_digits = {k: all_assets[k] for k in [f"digit_{i}" for i in range(10)]}
    
    return all_assets


# =============================================================================
# INTEGRATION WITH EXISTING CODE
# =============================================================================

def integrate_with_game():
    """How to integrate with existing game code."""
    from utils.assets import AssetGenerator
    from utils.loader import AssetLoader
    
    # Option 1: Use AssetLoader (already integrated)
    # The loader now falls back to generated assets when files don't exist
    loader = AssetLoader(tile_size=36)
    tile = loader.loadImage("tiles/unrevealed.png")  # Will generate if file missing
    
    # Option 2: Direct asset generation
    generator = AssetGenerator(tile_size=36)
    
    # For board rendering
    def get_tile_image(state, number=0, is_mine=False):
        """Get appropriate tile image based on game state."""
        if not state:  # unrevealed
            return generator.get("unrevealed")
        if is_mine:
            return generator.get("mine")
        if number == 0:
            return generator.get("revealed_0")
        return generator.get(f"revealed_{number}")
    
    # For HUD
    def get_restart_button(game_over=False, won=False):
        """Get restart button based on game state."""
        if won:
            return generator.get("restart_win")
        if game_over:
            return generator.get("restart_dead")
        return generator.get("restart_normal")
    
    return get_tile_image, get_restart_button


# =============================================================================
# CUSTOM TILE SIZES
# =============================================================================

def custom_sizes_example():
    """Generate assets with custom tile sizes for different difficulties."""
    from utils.assets import AssetGenerator, create_unrevealed_tile, create_number_tile
    import settings
    
    # Get tile size from settings based on difficulty
    tile_size = settings.get_tile_size(16, 16)  # Returns 36 for medium
    
    # Create generator with correct size
    generator = AssetGenerator(tile_size=tile_size)
    
    # Generate all assets for this difficulty
    assets = generator.preload_all()
    
    return assets


# =============================================================================
# HUD NUMBER DISPLAY
# =============================================================================

def hud_numbers_example():
    """Create HUD counter numbers."""
    from utils.assets import create_digit, create_hud_number
    
    # Create single digit
    digit_5 = create_digit(5, size=36)
    
    # Create multi-digit number (automatically pads with zeros)
    mine_count = create_hud_number(42, width=3, size=36)
    timer_value = create_hud_number(125, width=3, size=36)
    
    # Or use the generator
    from utils.assets import AssetGenerator
    gen = AssetGenerator(tile_size=36)
    
    mine_display = gen.get("hud_042")  # Number 42 with 3 digits
    timer_display = gen.get("hud_3125")  # Number 125
    
    return mine_count, timer_value


# =============================================================================
# DIRECT FUNCTION ACCESS
# =============================================================================

def direct_functions_example():
    """Use individual creation functions directly."""
    from utils.assets import (
        create_unrevealed_tile,
        create_revealed_tile,
        create_number_tile,
        create_mine_tile,
        create_flag_tile,
        create_restart_button,
        create_digit,
    )
    
    # Create tiles
    size = 36
    tile_unrevealed = create_unrevealed_tile(size)
    tile_revealed = create_revealed_tile(size)
    tile_number_3 = create_number_tile(3, size)
    
    # Create special tiles
    mine = create_mine_tile(size)
    mine_exploded = create_mine_tile(size, exploded=True)
    flag = create_flag_tile(size)
    wrong_flag = create_wrong_flag_tile(size)
    
    # Create restart buttons
    restart_normal = create_restart_button(50, "normal")
    restart_dead = create_restart_button(50, "dead")
    restart_win = create_restart_button(50, "win")
    
    # Create HUD digits
    digit_7 = create_digit(7, size=36, color=(255, 180, 50))
    
    return {
        "tile": tile_unrevealed,
        "mine": mine,
        "flag": flag,
        "restart": restart_normal,
        "digit": digit_7
    }


if __name__ == "__main__":
    # Run all examples
    print("=" * 60)
    print("Pysweeper Asset Generator - Usage Examples")
    print("=" * 60)
    
    # Initialize pygame for font rendering
    import pygame
    pygame.init()
    
    print("\n1. Simple Usage Example:")
    simple = simple_usage_example()
    print(f"   - Generated {len(simple)} assets")
    
    print("\n2. Batch Usage Example:")
    batch = batch_usage_example()
    print(f"   - Generated {len(batch)} total assets")
    
    print("\n3. Available Asset Names:")
    all_names = [
        "unrevealed", "revealed", "revealed_0" through "revealed_8",
        "mine", "mine_exploded", "flag", "wrong_flag",
        "restart_normal", "restart_dead", "restart_win",
        "digit_0" through "digit_9"
    ]
    print(f"   Total: 3 + 9 + 4 + 3 + 10 = 29 unique assets")
    
    print("\n4. Integration:")
    print("   from utils.assets import AssetGenerator")
    print("   generator = AssetGenerator(tile_size=36)")
    print("   tile = generator.get('flag')")
    
    print("\nDone! Run 'python -m utils.assets' to generate sample PNG files.")
