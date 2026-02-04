# Core Modules Documentation

## Tile Class

### Purpose
Represents a single cell on the Minesweeper board with its state and properties.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `row` | int | Grid row position |
| `col` | int | Grid column position |
| `isMine` | bool | True if tile contains a mine |
| `isRevealed` | bool | True if tile has been uncovered |
| `isFlagged` | bool | True if tile is marked by player |
| `neighborCount` | int | Number of adjacent mines (0-8) |

### Methods

#### `__init__(self, row, col)`
Creates a new tile at the specified grid position.

#### `reveal(self) -> bool`
Marks the tile as revealed.
- Returns: `True` if the tile contains a mine, `False` otherwise
- Does not reveal if already revealed or flagged

#### `toggleFlag(self) -> bool`
Toggles the flag state on the tile.
- Returns: The new flag state
- Does nothing if tile is already revealed

#### `__repr__(self) -> str`
String representation for debugging:
- `"F"` if flagged
- `"■"` if unrevealed
- `"M"` if revealed mine
- `" "` if revealed with 0 neighbors
- `"1-8"` for neighbor count

---

## Board Class

### Purpose
Manages the entire game board, including mine placement, game rules, and win/loss conditions.

### Constructor

```python
Board(rows: int, cols: int, mineCount: int)
```

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `rows` | int | Number of grid rows |
| `cols` | int | Number of grid columns |
| `mineCount` | int | Total mines to place |
| `tiles` | List[List[Tile]] | 2D grid of Tile objects |
| `gameState` | GameState | Current game state |
| `firstClick` | bool | True until first tile is revealed |
| `flagCount` | int | Number of flags placed |

### Methods

#### `initTiles(self)`
Creates the initial empty grid of Tile objects.

#### `placeMines(self, excludeRow, excludeCol)`
Randomly places mines on the board, excluding the 3x3 area around the first click.
- Ensures first move is never a mine
- Uses random sampling to avoid duplicates

#### `countNeighbors(self, row, col) -> int`
Counts mines in the 8 adjacent cells.
- Returns: Integer from 0 to 8

#### `calculateAllNeighbors(self)`
Pre-calculates neighbor counts for all non-mine tiles after mine placement.

#### `isValid(self, row, col) -> bool`
Checks if coordinates are within board boundaries.

#### `revealTile(self, row, col)`
Reveals a tile and triggers flood fill if it has 0 neighbors.
- Handles first click mine placement
- Detects game over on mine click
- Triggers win check after reveal

#### `floodFill(self, row, col)`
Recursively reveals all adjacent tiles starting from an empty cell.
- Uses stack-based iterative implementation (prevents stack overflow)
- Stops at already revealed tiles and flags

#### `toggleFlag(self, row, col)`
Places or removes a flag on a tile.
- Updates `flagCount` tracker

#### `revealAllMines(self)`
Shows all mine locations when player loses.

#### `checkWinCondition(self)`
Checks if all non-mine tiles have been revealed.
- Sets `gameState` to `WIN` if condition met

#### `getTile(self, row, col) -> Tile | None`
Returns the tile at specified coordinates.

#### `getRemainingCells(self) -> int`
Counts unrevealed non-mine cells remaining.

#### `reset(self, rows, cols, mineCount)`
Resets the board with new dimensions.

---

## State Class

### Purpose
Centralized state constants for clean state machine transitions.

### GameState Enumeration

| Constant | Value | Description |
|----------|-------|-------------|
| `MENU` | 0 | Main menu displayed |
| `PLAYING` | 1 | Game in progress |
| `GAME_OVER` | 2 | Player hit a mine |
| `WIN` | 3 | All safe tiles revealed |

### Difficulty Enumeration

| Constant | Tuple | Description |
|----------|-------|-------------|
| `EASY` | (9, 9, 10) | Beginner board |
| `MEDIUM` | (16, 16, 40) | Standard board |
| `HARD` | (16, 30, 99) | Expert board |

---

## Game Class

### Purpose
Main game controller managing the pygame loop, input handling, and state orchestration.

### Constructor

```python
Game()
```

Automatically initializes pygame display and clock.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `screen` | pygame.Surface | Main display surface |
| `clock` | pygame.Clock | FPS control |
| `state` | GameState | Current game state |
| `board` | Board | Active game board |
| `font` | pygame.Font | Default text font |
| `running` | bool | Game loop control |

### Methods

#### `initDisplay(self)`
Sets up pygame window caption and display mode.

#### `run(self)`
Main game loop running at 60 FPS.
- Calls `handleEvents()`
- Calls `update()`
- Calls `draw()`

#### `handleEvents(self)`
Processes all pygame events and delegates to state-specific handlers.

#### `handleMenuEvents(self, event)`
Processes menu input (button clicks).

#### `handlePlayingEvents(self, event)`
Processes gameplay input (tile clicks).

#### `handleEndGameEvents(self, event)`
Processes post-game input (R to restart, ESC for menu).

#### `handleMouseClick(self, event)`
Converts mouse position to grid coordinates and triggers board action.

#### `startGame(self, rows, cols, mines)`
Initializes a new game with specified difficulty.

#### `restartGame(self)`
Restarts the current game with same settings.

#### `switchState(self, newState)`
Changes the current game state.

#### `update(self)`
Updates game state each frame (timer, animations).

#### `draw(self)`
Renders the current game state to screen.

#### `drawMenu(self)`
Renders main menu with title and difficulty buttons.

#### `drawGame(self)`
Renders the game board and all tiles.

#### `drawTile(self, row, col)`
Renders a single tile based on its state.

#### `drawEndGameOverlay(self)`
Displays game over or win message with restart instructions.

---

## Algorithm Details

### Flood Fill (BFS Implementation)

```python
def floodFill(self, row, col):
    stack = [(row, col)]
    while stack:
        r, c = stack.pop()
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if self.isValid(nr, nc):
                    tile = self.tiles[nr][nc]
                    if not tile.isRevealed and not tile.isFlagged:
                        tile.reveal()
                        if tile.neighborCount == 0:
                            stack.append((nr, nc))
```

**Why BFS over DFS?** Prevents stack overflow on large boards.

### Mine Placement (First-Move Safety)

```python
def placeMines(self, excludeRow, excludeCol):
    safeZone = {excludeRow, excludeRow - 1, excludeRow + 1}
    safeColZone = {excludeCol, excludeCol - 1, excludeCol + 1}
    # ... random placement avoiding safe zone
```

**Guarantee**: First click is always a non-mine with at least one revealed neighbor.
