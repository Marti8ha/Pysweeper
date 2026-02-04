# UI Components Documentation

## Button Class

### Purpose
Reusable interactive button component with hover detection and click callbacks.

### Constructor

```python
Button(x, y, width, height, text, onClick=None)
```

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `rect` | pygame.Rect | Button position and size |
| `text` | str | Button label |
| `onClick` | Callable | Function called on click |
| `isHovered` | bool | Mouse over button |
| `isPressed` | bool | Mouse button held down |
| `font` | pygame.Font | Text rendering font |

### Visual States

| State | Color | Offset | Effect |
|-------|-------|--------|--------|
| Normal | (192, 192, 192) | 0 | Raised appearance |
| Hovered | (170, 170, 170) | 0 | Slightly lighter |
| Pressed | (100, 100, 100) | 2 | Depressed appearance |

### Methods

#### `handleEvent(self, event)`
Processes pygame events:
- `MOUSEMOTION`: Updates hover state
- `MOUSEBUTTONDOWN`: Sets pressed state
- `MOUSEBUTTONUP`: Triggers callback if still hovering

#### `draw(self, surface)`
Renders button with 3D bevel effect and centered text.

#### `setPosition(self, x, y)`
Moves button to new coordinates.

#### `setText(self, text)`
Updates button label.

---

## Hud Class

### Purpose
Heads-up display showing game status (mine counter, timer, restart button).

### Constructor

```python
Hud(x, y, width, height, onRestart=None)
```

### Layout

```
┌─────────────────────────────────┐
│  [010]      [ :-) ]      [00:45] │
└─────────────────────────────────┘
   ^            ^            ^
   |            |            |
 Mine       Restart       Timer
 Counter    Button       (MM:SS)
```

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `rect` | pygame.Rect | HUD area |
| `mineCount` | int | Remaining unflagged mines |
| `timer` | int | Elapsed seconds |
| `restartButton` | pygame.Rect | Restart button area |
| `onRestart` | Callable | Restart callback |

### Methods

#### `setMineCount(self, count)`
Updates the displayed mine counter.

#### `setTimer(self, seconds)`
Updates the timer display in MM:SS format.

#### `handleEvent(self, event)`
Detects clicks on restart button.

#### `draw(self, surface)`
Renders HUD with:
- Left-aligned mine counter (red text)
- Centered restart button (smiley face)
- Right-aligned timer (red text)

#### `reset(self)`
Resets counter and timer to zero.

---

## Menu Class

### Purpose
Start screen with game title and difficulty selection.

### Constructor

```python
Menu(onStartGame=None)
```

### Layout

```
┌─────────────────────────────────┐
│                                 │
│           PYSWEEPER             │
│      Minesweeper Clone          │
│                                 │
│      Select Difficulty:         │
│                                 │
│    ┌─────────────────────┐     │
│    │    Easy (9x9)       │     │
│    └─────────────────────┘     │
│                                 │
│    ┌─────────────────────┐     │
│    │   Medium (16x16)    │     │
│    └─────────────────────┘     │
│                                 │
│    ┌─────────────────────┐     │
│    │    Hard (30x16)     │     │
│    └─────────────────────┘     │
│                                 │
└─────────────────────────────────┘
```

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `font` | pygame.Font | Title font (72pt) |
| `smallFont` | pygame.Font | Subtitle font (36pt) |
| `buttons` | List[Button] | Difficulty selection buttons |
| `onStartGame` | Callable | Game start callback |

### Methods

#### `initButtons(self)`
Creates three difficulty buttons centered on screen.

#### `startGame(self, rows, cols, mines)`
Invokes callback with selected difficulty parameters.

#### `handleEvent(self, event)`
Delegates events to all menu buttons.

#### `draw(self, surface)`
Renders:
- Title (large, centered, blue)
- Subtitle (medium, centered, dark gray)
- Instruction text
- All difficulty buttons

#### `updateButtonPositions(self, screenWidth, screenHeight)`
Recalculates button positions for new window size.

---

## Rendering Constants

### Button Dimensions
- Width: 200 pixels
- Height: 50 pixels
- Corner radius: 4 pixels

### HUD Dimensions
- Height: 60 pixels
- Restart button: 50×40 pixels

### Font Sizes
- Title: 72 points
- Subtitle: 36 points
- Button text: 32 points
- HUD numbers: 48 points

### 3D Effect Colors

| Element | Color | RGB |
|---------|-------|-----|
| Button face | Light gray | (192, 192, 192) |
| Highlight | White | (255, 255, 255) |
| Shadow | Dark gray | (128, 128, 128) |
| Text | Black | (0, 0, 0) |

---

## Usage Examples

### Creating a Custom Button

```python
def onCustomClick():
    print("Button clicked!")

button = Button(100, 100, 150, 40, "Click Me", onCustomClick)
```

### Integrating HUD with Game

```python
hud = Hud(0, 0, 800, 60, onRestart=restartGame)
hud.setMineCount(board.mineCount - board.flagCount)
```

### Creating Custom Menu

```python
def startCustomGame():
    # Custom game initialization logic
    pass

menu = Menu(onStartGame=startCustomGame)
```

---

## Event Handling Flow

```
pygame.MOUSEMOTION
    │
    ▼
Button.handleEvent()
    │
    ├── isHovered = True (if collision)
    │
pygame.MOUSEBUTTONDOWN
    │
    ▼
Button.handleEvent()
    │
    ├── isPressed = True
    │
pygame.MOUSEBUTTONUP
    │
    ▼
Button.handleEvent()
    │
    ├── Trigger onClick()
    │
    └── isPressed = False
```
