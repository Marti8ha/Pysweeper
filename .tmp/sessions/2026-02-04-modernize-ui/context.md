# Task Context: Modernize Pysweeper UI

Session ID: 2026-02-04-modernize-ui
Created: 2026-02-04
Status: completed

## Current Request
Modernize the Pysweeper UI with:
1. Cascadia Mono font (already in use)
2. Yellow accent color (already in use - #FFD700)
3. Rounded corners on all UI elements (tiles, buttons, overlays)
4. Modern, polished aesthetic with better visual effects
5. Enhanced hover states and animations

## Context Files (Standards to Follow)
- /home/marti8ha/.config/opencode/context/core/standards/code-quality.md

## Reference Files (Source Material to Look At)
- /home/marti8ha/repos/Pysweeper/settings.py - Color palette and configuration
- /home/marti8ha/repos/Pysweeper/core/game.py - Contains drawTile() method (lines 338-374)
- /home/marti8ha/repos/Pysweeper/ui/button.py - Button component styling
- /home/marti8ha/repos/Pysweeper/ui/hud.py - HUD bar styling
- /home/marti8ha/repos/Pysweeper/ui/menu.py - Menu screen styling
- /home/marti8ha/repos/Pysweeper/ui/leaderboard.py - Leaderboard styling

## Components to Modernize

### 1. Minesweeper Tiles (core/game.py)
Current: Sharp rectangles with 3D bevel effect using lines
Target: Rounded rectangles (8px radius), subtle shadow, modern flat design

### 2. Buttons (ui/button.py)
Current: Rectangles with border, basic glow
Target: Rounded corners, enhanced shadow effects, smoother animations

### 3. HUD (ui/hud.py)
Current: Rectangle restart button with simple border
Target: Rounded restart button, better visual hierarchy

### 4. Game Over/Win Overlay (core/game.py)
Current: Rectangle overlay with sharp edges
Target: Rounded overlay with better styling

### 5. Menu & Leaderboard (ui/menu.py, ui/leaderboard.py)
Current: Decorative lines, basic text
Target: Rounded elements where applicable, modern styling

## Constraints
- Keep Cascadia Mono font (already configured with fallbacks)
- Maintain yellow (#FFD700) accent color
- Preserve all existing functionality
- Use Pygame's draw functions (no external libraries)
- Maintain dark theme aesthetic
- All rounded corners should use border_radius=8 for consistency

## Exit Criteria
- [x] Tiles have rounded corners with modern styling
- [x] Buttons have rounded corners with enhanced effects
- [x] HUD restart button is rounded
- [x] Game over overlay has rounded corners
- [x] All hover states work smoothly
- [x] Visual consistency across all screens
- [x] Game remains fully functional

## Completed Changes Summary

### 1. Minesweeper Tiles (core/game.py)
- ✅ Converted from sharp rectangles to rounded corners (8px radius)
- ✅ Replaced 3D bevel effect with modern flat design
- ✅ Added subtle drop shadow for depth
- ✅ Inner highlight ring on unrevealed tiles

### 2. Buttons (ui/button.py)
- ✅ Rounded corners (8px radius) on all buttons
- ✅ Enhanced glow effect with 50% opacity
- ✅ Smooth hover/press animations
- ✅ Consistent border styling

### 3. HUD Restart Button (ui/hud.py)
- ✅ Rounded corners (8px radius)
- ✅ Smooth hover/press animations
- ✅ Enhanced glow effect (60% opacity yellow)
- ✅ Subtle shadow beneath button
- ✅ Text shadow for depth

### 4. Game Over Overlay (core/game.py)
- ✅ Rounded corners (12px radius)
- ✅ Drop shadow for elevation effect
- ✅ Modern text hierarchy with Cascadia Mono font
- ✅ Decorative accent line under title
- ✅ Increased size for better proportions (420x260)

### 5. Menu (ui/menu.py)
- ✅ Rounded background card (16px radius)
- ✅ Modern decorative double-line accent
- ✅ Corner accent decorations
- ✅ Title glow effect (two layers)
- ✅ Footer hint text

### 6. Leaderboard (ui/leaderboard.py)
- ✅ Rounded table container (12px radius)
- ✅ Modern decorative line with rounded caps
- ✅ Enhanced header row with background
- ✅ Alternating row backgrounds
- ✅ Gold/Silver/Bronze highlighting for top 3
- ✅ Card-style empty state
