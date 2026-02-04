# Gameplay Guide

## Objective

Clear the minefield without detonating any mines. Reveal all safe tiles to win.

## Controls

| Input | Action |
|-------|--------|
| **Left Click** | Reveal a tile |
| **Right Click** | Flag/Unflag a tile |
| **R Key** | Restart current game |
| **ESC Key** | Return to main menu |

## Game Elements

### Tile States

```
┌─────────────────┬─────────────────────────────────┐
│ Visual          │ Meaning                         │
├─────────────────┼─────────────────────────────────┤
│ ■ (raised)      │ Unrevealed, unknown             │
│ F (flag icon)   │ Flagged by player              │
│ [number]        │ Revealed, adjacent mines count  │
│ M (red)         │ Mine (game over)               │
└─────────────────┴─────────────────────────────────┘
```

### Number Meanings

Each number indicates how many mines touch that tile:

```
Example: A "3" means three mines are adjacent:

┌───┬───┬───┐
│ M │ 3 │ M │  ← This tile touches 3 mines
├───┼───┼───┤
│ 3 │ 5 │ 3 │  ← This tile touches 5 mines
├───┼───┼───┤
│ M │ 3 │ M │
└───┴───┴───┘
```

### Difficulty Levels

| Level | Grid | Mines | Difficulty |
|-------|------|-------|------------|
| Easy | 9×9 | 10 | Beginner |
| Medium | 16×16 | 40 | Standard |
| Hard | 16×30 | 99 | Expert |

## Strategy Tips

### 1. Start with Corners and Edges
Safe starting points. Numbers are more informative when tile has fewer neighbors.

### 2. Look for Guaranteed Moves
When a number equals its potential neighbors, you know exactly what's there:
```
If a "1" is in a corner → the only adjacent tile is a mine
If a "1" is on an edge → one of the two adjacent tiles is a mine
```

### 3. The "1-2-1" Pattern
```
M 1 1 M
1 2 2 1
M 1 1 M
```
The "2" tiles must both be safe because all surrounding mines are already identified.

### 4. The "1-2-1-2" Pattern
```
M 1 1 M 1 1 M
1 2 2 1 2 2 1
M 1 1 M 1 1 M
```
The two "2" tiles in the middle are safe.

### 5. Use Flags to Track Mines
Flag suspected mines to:
- Prevent accidental clicks
- Help count known mines around a number
- Mark completed areas

### 6. Chord on Numbers
If you flag all mines around a number, you can click the number to reveal all remaining neighbors at once.

```
Flagged: F F F
Number:  3 ──Click──► Reveals safe tiles
```

### 7. Work from Known to Unknown
Always expand from confirmed safe areas. Numbers only make sense in context.

## First-Move Guarantee

Your first click is **always safe**:
- Mines are placed after your first click
- The first clicked tile and its 8 neighbors are guaranteed to be mine-free
- This guarantees at least one tile (and its neighbors) are revealed

## Winning Conditions

Win when ALL non-mine tiles are revealed:
```
✓ All safe tiles uncovered
✓ All mines remain unclicked
✓ HUD shows completion time
```

## Losing Conditions

Lose when you click a mine:
```
✗ Mine detonated
✗ All mines revealed
✗ Game over screen displayed
```

## HUD Elements

```
┌─────────────────────────────────────┐
│  [010]      [ :-) ]      [00:45]    │
└─────────────────────────────────────┘
    │           │           │
    │           │           └── Elapsed time
    │           └── Restart button
    └── Remaining unflagged mines
```

## Scoring

No built-in scoring system. Victory is binary:
- **Win**: All safe tiles revealed
- **Loss**: Mine detonated

For competitive play, race against the timer.

## Common Mistakes to Avoid

1. **Clicking too fast**: Take time to analyze patterns
2. **Ignoring flags**: Track mines visually
3. **Forgetting chord**: Speed up by using number chords
4. **Guessing**: Only guess when no logical moves remain

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| R | Restart game |
| ESC | Main menu |
| F | Toggle fullscreen (if implemented) |

## Tips for Beginners

1. **Start Easy**: Learn patterns on 9×9 before upgrading
2. **Take Your Time**: Speed comes with pattern recognition
3. **Use Both Hands**: Left for clicking, right for flagging
4. **Review Losses**: Analyze what went wrong
5. **Practice Daily**: Pattern recognition improves with repetition

## Advanced Techniques

### Edge Counting
```
On an edge tile touching 3 unknown tiles:
If the number is 2, and you can identify 2 mines elsewhere,
the remaining adjacent tiles must be safe.
```

### Box Solving
Identify complete patterns to mark entire sections:

```
┌───────┬───────┐
│ 1 1 0 │ 0 1 1 │  ← All zeros = no mines around them
│ 1 M 0 │ 0 M 1 │  ← Zero can reveal everything around it
└───────┴───────┘
```

### Probability Assessment
When uncertain, calculate probabilities:
- Fewer unknown neighbors = higher certainty
- Corner tiles have maximum 3 potential neighbors
- Edge tiles have maximum 5 potential neighbors
