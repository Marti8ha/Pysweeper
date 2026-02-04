# Pysweeper

A modern, feature-rich Minesweeper clone built with Pygame.

## Features

- **Three difficulty levels**: Easy (9×9), Medium (16×16), Hard (16×30)
- **Dynamic window sizing**: Window scales optimally for each difficulty
- **Classic gameplay**: Left-click to reveal, right-click to flag
- **First-move guarantee**: Never lose on your first click
- **Points system**: Score based on tiles revealed, time, and strategy
- **Leaderboard**: Track your top 10 scores locally
- **Modern dark theme**: Sleek black/grey color palette with yellow accents
- **Cascadia Mono font**: Clean monospace typography
- **Smooth animations**: Hover effects and visual feedback
- **Generated assets**: Placeholder graphics for tiles, mines, flags, and buttons
- **Professional architecture**: Clean separation of concerns

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

## Visual Design

- **Theme**: Dark modern aesthetic with black background
- **Accent color**: Yellow (#FFD700) for highlights and emphasis
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
│   └── state.py        # State constants & scoring
├── ui/                  # User interface
│   ├── button.py       # Button component
│   ├── hud.py          # Status bar
│   ├── menu.py         # Main menu
│   └── leaderboard.py  # Score leaderboard
├── utils/               # Utilities
│   ├── loader.py       # Asset loading
│   ├── helpers.py      # Helper functions
│   ├── assets.py       # Generated placeholder assets
│   └── leaderboard_storage.py  # JSON persistence
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

## Points System

| Factor | Points |
|--------|--------|
| Base per tile | 10 |
| No hints multiplier | 2.0x |
| Time bonus | max(0, 1000 - seconds) |
| No flags bonus | +500 |
| Difficulty multiplier | Easy=1.0, Medium=1.5, Hard=2.0 |

**Formula**: `(tiles × 10 × 2.0 × difficulty) + time_bonus + no_flags_bonus`

## Leaderboard

- Stores top 10 scores in JSON format
- Tracks difficulty, time, and date
- Viewable from main menu

## Generated Assets

The game includes programmatically generated placeholder assets:
- Tile states (unrevealed, revealed, empty)
- Numbers 1-8 in neon colors
- Mine and flag icons
- Restart button states (smile, dead, win)
- HUD digit displays

## Architecture Highlights

- **Core/UI separation**: Game logic contains zero pygame dependencies
- **State machine**: Clean transitions between menu/playing/game over/win/leaderboard
- **Event delegation**: Input handling scales with new features
- **Testability**: Board logic can be tested without pygame
- **Configurable theme**: All colors defined in settings.py
- **Dynamic sizing**: Window and tiles adapt to difficulty

## Requirements

- Python 3.12+
- Pygame 2.6.1+

## Optional

- Cascadia Mono Bold font file (falls back to system default if not found)

## License

MIT License
