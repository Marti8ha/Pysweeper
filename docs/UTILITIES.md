# Utilities Documentation

## AssetLoader Class

### Purpose
Centralized asset management with lazy loading, caching, and placeholder generation.

### Constructor

```python
AssetLoader()
```

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `images` | Dict[str, Surface] | Cached image surfaces |
| `fonts` | Dict[str, Font] | Cached font objects |
| `sounds` | Dict[str, Sound] | Cached sound objects |
| `basePath` | str | Root asset directory ("assets/") |

### Methods

#### `loadImage(self, path, key=None) -> pygame.Surface`
Loads an image from `assets/images/{path}`.
- Automatically converts with alpha channel
- Creates 32×32 gray placeholder on error
- Caches by path or optional key

#### `loadFont(self, name, size, key=None) -> pygame.font.Font`
Loads a font from `assets/fonts/{name}`.
- Falls back to system default if name is None
- Caches by "{name}_{size}" or optional key

#### `loadSound(self, path, key=None) -> pygame.mixer.Sound | None`
Loads a sound from `assets/sounds/{path}`.
- Returns None on error (non-fatal)
- Caches by path or optional key

#### `createPlaceholderSurface(self, width, height, color) -> pygame.Surface`
Generates a solid color surface for missing assets.

#### `clearCache(self)`
Empties all asset caches to free memory.

#### `preloadCommonAssets(self)`
Pre-loads frequently used assets (commented out until assets available).

### Usage

```python
loader = AssetLoader()

# Load with automatic caching
tileImage = loader.loadImage("tiles/covered.png")
flagImage = loader.loadImage("tiles/flag.png", "my_flag")

# Load font
font = loader.loadFont("arial.ttf", 24)

# Global instance available
from utils.loader import loader
```

---

## Helper Functions

### `getTileFromMouse(pos, tileSize, offsetX=0, offsetY=0)`

Converts pixel coordinates to grid position.

**Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| `pos` | Tuple[int, int] | (x, y) pixel coordinates |
| `tileSize` | int | Size of each tile in pixels |
| `offsetX` | int | Board horizontal offset |
| `offsetY` | int | Board vertical offset |

**Returns:** `(row, col)` tuple or `None` if outside board

**Example:**
```python
mousePos = (250, 180)
tileSize = 40
offsetX, offsetY = 100, 100

gridPos = getTileFromMouse(mousePos, tileSize, offsetX, offsetY)
# Returns (2, 3) if within board
```

---

### `centerText(surface, text, font, color, yOffset=0)`

Renders centered text on a surface.

**Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| `surface` | pygame.Surface | Target surface |
| `text` | str | Text to render |
| `font` | pygame.Font | Font to use |
| `color` | Tuple[int, int, int] | RGB color |
| `yOffset` | int | Vertical offset from center |

**Returns:** `pygame.Rect` of rendered text

---

### `drawGridLines(surface, startX, startY, rows, cols, tileSize)`

Draws grid lines for visual board separation.

**Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| `surface` | pygame.Surface | Target surface |
| `startX` | int | Grid left edge |
| `startY` | int | Grid top edge |
| `rows` | int | Number of rows |
| `cols` | int | Number of columns |
| `tileSize` | int | Size of each cell |

---

### `drawRaisedRect(surface, rect, color)`

Draws a 3D raised rectangle with highlight and shadow borders.

**Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| `surface` | pygame.Surface | Target surface |
| `rect` | pygame.Rect | Rectangle to draw |
| `color` | Tuple[int, int, int] | Fill color |

---

### `drawPressedRect(surface, rect, color)`

Draws a 3D pressed/depressed rectangle with inner shadow.

**Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| `surface` | pygame.Surface | Target surface |
| `rect` | pygame.Rect | Rectangle to draw |
| `color` | Tuple[int, int, int] | Fill color |

---

### `formatTime(seconds) -> str`

Converts seconds to MM:SS format.

**Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| `seconds` | int | Elapsed time in seconds |

**Returns:** Formatted string (e.g., "01:25", "00:05")

**Examples:**
```python
formatTime(85)   # Returns "01:25"
formatTime(5)     # Returns "00:05"
formatTime(3661)  # Returns "61:01"
```

---

### `clamp(value, minValue, maxValue)`

Constrains a value within specified bounds.

**Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| `value` | int/float | Value to constrain |
| `minValue` | int/float | Lower bound |
| `maxValue` | int/float | Upper bound |

**Returns:** Value clipped to [minValue, maxValue]

**Examples:**
```python
clamp(5, 0, 10)    # Returns 5
clamp(15, 0, 10)   # Returns 10
clamp(-5, 0, 10)   # Returns 0
```

---

## Asset Directory Structure

```
assets/
├── fonts/
│   ├── arial.ttf
│   ├── bold.ttf
│   └── ...
├── images/
│   ├── tiles/
│   │   ├── covered.png
│   │   ├── revealed_0.png
│   │   ├── revealed_1.png
│   │   ├── ...
│   │   ├── flag.png
│   │   └── mine.png
│   └── ui/
│       ├── button_normal.png
│       ├── button_hover.png
│       └── ...
└── sounds/
    ├── click.wav
    ├── flag.wav
    ├── explode.wav
    └── win.wav
```

---

## Best Practices

1. **Lazy Loading**: Assets load on first use, not at startup
2. **Caching**: Subsequent accesses use cached versions
3. **Placeholders**: Missing assets show gray squares instead of crashing
4. **Error Handling**: Sound errors are non-fatal (returns None)
5. **Global Instance**: Use `from utils.loader import loader` for single instance
