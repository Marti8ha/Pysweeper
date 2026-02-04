# Settings Reference

## Window Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `WIDTH` | 800 | Window width in pixels |
| `HEIGHT` | 700 | Window height in pixels |
| `FPS` | 60 | Target frames per second |

## Board Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `ROWS` | 16 | Number of grid rows |
| `COLS` | 16 | Number of grid columns |
| `MINES` | 40 | Total mines on board |
| `TILE_SIZE` | 36 | Pixel size of each tile |
| `BOARD_OFFSET_X` | 52 | Board horizontal offset from left edge |
| `BOARD_OFFSET_Y` | 80 | Board vertical offset from top edge |

## Difficulty Presets

Defined in `core/state.py` under `Difficulty` class:

| Level | Rows | Cols | Mines |
|-------|------|------|-------|
| `EASY` | 9 | 9 | 10 |
| `MEDIUM` | 16 | 16 | 40 |
| `HARD` | 16 | 30 | 99 |

## Font

**Primary**: Cascadia Mono (monospace)
**Fallback**: System default monospace

Used for all UI elements:
- Title: 64pt
- Subtitle: 32pt
- Body text: 36pt
- HUD numbers: 42pt
- Button text: 28pt

## Dark Theme Color Palette

### Core Colors

| Color | RGB | Usage |
|-------|-----|-------|
| `background` | (18, 18, 18) | Main application background |
| `surface` | (25, 25, 25) | UI surface elements |
| `surfaceLight` | (35, 35, 35) | Lighter surface variant |

### Tile Colors

| Color | RGB | Usage |
|-------|-----|-------|
| `tileUnrevealed` | (45, 45, 45) | Unrevealed tile background |
| `tileRevealed` | (28, 28, 28) | Revealed empty tile |
| `tileHover` | (55, 55, 55) | Hover state |
| `tileBorderLight` | (70, 70, 70) | 3D bevel highlight |
| `tileBorderDark` | (25, 25, 25) | 3D bevel shadow |

### Text Colors

| Color | RGB | Usage |
|-------|-----|-------|
| `textPrimary` | (220, 220, 220) | Primary text |
| `textSecondary` | (150, 150, 150) | Secondary text |
| `textAccent` | (100, 200, 255) | Accent/emphasis text |

### Neon Number Colors

| Number | RGB | Usage |
|--------|-----|-------|
| 1 | (80, 180, 255) | Cyan |
| 2 | (100, 255, 100) | Bright Green |
| 3 | (255, 100, 100) | Bright Red |
| 4 | (100, 150, 255) | Blue |
| 5 | (255, 150, 50) | Orange |
| 6 | (50, 200, 200) | Teal |
| 7 | (255, 255, 255) | White |
| 8 | (200, 200, 200) | Light Gray |

### Special Elements

| Color | RGB | Usage |
|-------|-----|-------|
| `mine` | (255, 60, 60) | Revealed mine |
| `flag` | (255, 180, 50) | Flag indicator |
| `accent` | (100, 200, 255) | UI accent color |
| `win` | (50, 255, 100) | Victory message |
| `lose` | (255, 80, 80) | Game over message |

### Button Colors

| Color | RGB | Usage |
|-------|-----|-------|
| `buttonBackground` | (50, 50, 50) | Button background |
| `buttonHover` | (65, 65, 65) | Button hover state |
| `buttonPressed` | (40, 40, 40) | Button pressed state |
| `buttonBorder` | (80, 80, 80) | Button border |

### HUD Colors

| Color | RGB | Usage |
|-------|-----|-------|
| `hudBackground` | (25, 25, 25) | HUD background |
| `hudBorder` | (50, 50, 50) | HUD border |

### Overlay Colors

| Color | RGB | Usage |
|-------|-----|-------|
| `overlayBackground` | (0, 0, 0, 180) | Semi-transparent overlay |
| `overlayBorder` | (100, 200, 255) | Overlay border accent |

## Coordinate System

```
Screen (800x700)
┌─────────────────────────────────────┐
│                                     │
│   HUD (top, 60px)                  │
│   ┌─────────────────────────────┐  │
│   │  [010]  :-)  [00:45]        │  │
│   └─────────────────────────────┘  │
│                                     │
│   Board Offset: (52, 80)           │
│   ┌───┬───┬───┬───┐                │
│   │ ■ │ ■ │ ■ │ ■ │                │
│   ├───┼───┼───┼───┤                │
│   │ ■ │ ■ │ 1 │ 1 │                │
│   └───┴───┴───┴───┘                │
│                                     │
└─────────────────────────────────────┘

Tile size: 36×36 pixels
Tile spacing: 2 pixels
```

## Event Mapping

| Input | Action |
|-------|--------|
| Left Click | Reveal tile |
| Right Click | Flag/Unflag tile |
| R Key | Restart game |
| ESC Key | Return to menu |
| Click Difficulty Button | Start new game |

## Game Controls

### Menu
- Click difficulty button to start game

### Playing
- Left-click tiles to reveal
- Right-click tiles to flag
- Click smiley face to restart

### Game Over / Win
- Press R to restart same game
- Press ESC to return to menu
