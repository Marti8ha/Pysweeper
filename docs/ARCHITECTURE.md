# Architecture Documentation

## Overview

Pysweeper follows a clean separation of concerns with five distinct layers:

```
┌─────────────────────────────────────────────────────────────┐
│                        main.py                              │
│                    (Entry Point)                             │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                       ui/                                   │
│            (Buttons, HUD, Menu, Rendering)                   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                       core/                                 │
│            (Game Logic, State Management)                   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                      utils/                                 │
│              (Helpers, Asset Loading)                       │
└─────────────────────────────────────────────────────────────┘
```

## Module Responsibilities

### main.py
- **Single responsibility**: Bootstrap the application
- **Contents**: Import `Game` class and call `game.run()`
- **Why**: Entry point should be minimal and never change

### core/game.py
- **Responsibility**: Main game loop and state orchestration
- **Handles**:
  - Pygame initialization
  - Event loop management
  - State machine transitions (MENU → PLAYING → GAME_OVER/WIN)
  - Drawing coordination

### core/board.py
- **Responsibility**: Pure game logic (no pygame dependencies)
- **Handles**:
  - Mine placement algorithm
  - Neighbor counting
  - Flood fill algorithm
  - Win/loss conditions

### core/tile.py
- **Responsibility**: Individual cell state
- **Properties**:
  - `isMine`, `isRevealed`, `isFlagged`, `neighborCount`

### core/state.py
- **Responsibility**: Game state constants
- **Enums**: `GameState`, `Difficulty`

### ui/button.py
- **Responsibility**: Reusable clickable component
- **Features**: Hover state, click callbacks, 3D visual effect

### ui/hud.py
- **Responsibility**: Status bar display
- **Elements**: Mine counter, timer, restart button

### ui/menu.py
- **Responsibility**: Start screen
- **Features**: Difficulty selection buttons

### utils/helpers.py
- **Responsibility**: Utility functions
- **Functions**: Coordinate conversion, text centering, grid drawing

### utils/loader.py
- **Responsibility**: Asset management
- **Features**: Lazy loading, caching, placeholder generation

## Data Flow

```
Mouse Click Event
    │
    ▼
game.handleEvents() ───► game.handlePlayingEvents()
    │
    ▼
board.revealTile(row, col) ───► tile.reveal()
    │
    ▼
floodFill() / checkWinCondition()
    │
    ▼
Game state updated
    │
    ▼
game.draw() ───► drawTile() for each tile
    │
    ▼
pygame.display.flip()
```

## State Machine

```
           ┌────────────────┐
           │     MENU       │◄──────────────┐
           └───────┬────────┘               │
                   │                        │
           Click Start                      │
                   │                        │
                   ▼                        │
           ┌────────────────┐               │
           │    PLAYING     │               │
           └───────┬────────┘               │
                   │                        │
           Mine Click        Win Condition  │
                   │                        │
                   ▼                        │
           ┌────────────────┐               │
           │   GAME_OVER    │─── R ────────┘
           └───────┬────────┘
                   │
           Win Condition
                   │
                   ▼
           ┌────────────────┐
           │      WIN       │─── R ────────┘
           └────────────────┘
```

## Key Design Principles

1. **Dependency Inversion**: Core knows nothing about pygame; UI depends on core
2. **Single Responsibility**: Each module has one clear purpose
3. **Testability**: Board logic can be tested without pygame
4. **Extensibility**: New features add files, never modify existing ones

## Naming Convention

All code uses `firstSecond` (camelCase) for:
- Variables: `playerScore`, `mineCounter`
- Functions: `calculatePosition()`, `handleMouseClick()`
- Methods: `revealTile()`, `toggleFlag()`

Classes use `PascalCase`:
- `Game`, `Board`, `Tile`, `Button`, `Hud`, `Menu`

Comments are:
- Precise and concise
- Only after function/class declarations
- Explaining complex logic blocks
- Never redundant (no "This function does X")
