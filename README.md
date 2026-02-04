# Pysweeper

A clean, professional Minesweeper clone built with Pygame.

## Features

- **Three difficulty levels**: Easy (9×9), Medium (16×16), Hard (16×30)
- **Classic gameplay**: Left-click to reveal, right-click to flag
- **First-move guarantee**: Never lose on your first click
- **Modern dark theme**: Sleek black/grey color palette
- **Cascadia Mono font**: Clean monospace typography
- **Smooth animations**: Hover effects and visual feedback
- **Professional architecture**: Clean separation of concerns
- **Comprehensive documentation**: Full API reference and gameplay guide

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

## Visual Design

- **Theme**: Dark modern aesthetic with black background
- **Font**: Cascadia Mono (monospace)
- **Colors**: Neon accent colors on dark surfaces
- **Effects**: Subtle hover states and smooth transitions

## Project Structure

```
pysweeper/
├── main.py              # Entry point
├── settings.py          # Configuration & colors
├── requirements.txt     # Dependencies
├── core/                # Game logic
│   ├── game.py         # Main controller
│   ├── board.py        # Board management
│   ├── tile.py         # Tile objects
│   └── state.py        # State constants
├── ui/                  # User interface
│   ├── button.py       # Button component
│   ├── hud.py          # Status bar
│   └── menu.py         # Main menu
├── utils/               # Utilities
│   ├── loader.py       # Asset loading
│   └── helpers.py      # Helper functions
└── docs/                # Documentation
    ├── ARCHITECTURE.md  # System design
    ├── SETTINGS.md      # Configuration reference
    ├── CORE_MODULES.md  # API documentation
    ├── UI_COMPONENTS.md # UI docs
    ├── UTILITIES.md     # Utils API
    └── GAMEPLAY.md      # How to play
```

## Controls

- **Left Click**: Reveal tile
- **Right Click**: Flag/Unflag tile
- **R**: Restart game
- **ESC**: Return to menu
- **Click Difficulty**: Start new game with selected difficulty

## Architecture Highlights

- **Core/UI separation**: Game logic contains zero pygame dependencies
- **State machine**: Clean transitions between menu/playing/game over/win
- **Event delegation**: Input handling scales with new features
- **Testability**: Board logic can be tested without pygame
- **Configurable theme**: All colors defined in settings.py

## Requirements

- Python 3.12+
- Pygame 2.6.1+

## Optional

- Cascadia Mono font file (falls back to system default if not found)

## License

MIT License
