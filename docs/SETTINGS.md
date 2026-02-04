# Settings Reference

## Window Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `WIDTH` | 800 | Window width in pixels |
| `HEIGHT` | 600 | Window height in pixels |
| `FPS` | 60 | Target frames per second |

## Board Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `ROWS` | 16 | Number of grid rows |
| `COLS` | 16 | Number of grid columns |
| `MINES` | 40 | Total mines on board |
| `TILE_SIZE` | 40 | Pixel size of each tile |

## Difficulty Presets

Defined in `core/state.py` under `Difficulty` class:

| Level | Rows | Cols | Mines |
|-------|------|------|-------|
| `EASY` | 9 | 9 | 10 |
| `MEDIUM` | 16 | 16 | 40 |
| `HARD` | 16 | 30 | 99 |

## Color Palette

| Color | RGB | Usage |
|-------|-----|-------|
| Background | (192, 192, 192) | Classic Windows gray |
| Tile Raised | (192, 192, 192) | Unrevealed tiles |
| Tile Pressed | (128, 128, 128) | Revealed empty tiles |
| Border Light | (255, 255, 255) | 3D bevel effect |
| Border Dark | (128, 128, 128) | 3D bevel shadow |

## Number Colors

| Number | Color | RGB |
|--------|-------|-----|
| 1 | Blue | (0, 0, 255) |
| 2 | Green | (0, 128, 0) |
| 3 | Red | (255, 0, 0) |
| 4 | Dark Blue | (0, 0, 128) |
| 5 | Dark Red | (128, 0, 0) |
| 6 | Cyan | (0, 128, 128) |
| 7 | Black | (0, 0, 0) |
| 8 | Gray | (128, 128, 128) |

## Coordinate System

```
Screen (800x600)
┌─────────────────────────────────────┐
│                                     │
│   HUD (top, ~60px)                 │
│   ┌─────────────────────────────┐  │
│   │  [010]  :-)  [00:45]        │  │
│   └─────────────────────────────┘  │
│                                     │
│   Board Offset: (100, 100)         │
│   ┌───┬───┬───┬───┐                │
│   │ ■ │ ■ │ ■ │ ■ │                │
│   ├───┼───┼───┼───┤                │
│   │ ■ │ ■ │ 1 │ 1 │                │
│   └───┴───┴───┴───┘                │
│                                     │
└─────────────────────────────────────┘
```

## Event Mapping

| Input | Action |
|-------|--------|
| Left Click | Reveal tile |
| Right Click | Flag/Unflag tile |
| R Key | Restart game |
| ESC Key | Return to menu |
