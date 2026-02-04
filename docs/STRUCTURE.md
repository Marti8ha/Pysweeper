📁 Project structure
minesweeper/
│
├── main.py
├── settings.py
├── requirements.txt
│
├── assets/
│   ├── fonts/
│   ├── images/
│   │   ├── tiles/
│   │   └── ui/
│   └── sounds/
│
├── core/
│   ├── game.py
│   ├── board.py
│   ├── tile.py
│   └── state.py
│
├── ui/
│   ├── button.py
│   ├── hud.py
│   └── menu.py
│
└── utils/
    ├── loader.py
    └── helpers.py


This is very close to how a professional Pygame project would be organized.

🧠 What each part does
main.py → only starts the game
from core.game import Game

if __name__ == "__main__":
    game = Game()
    game.run()


Nothing else. Ever.

settings.py → all constants live here
WIDTH = 800
HEIGHT = 800
FPS = 60

ROWS = 16
COLS = 16
MINES = 40

TILE_SIZE = 40


You will touch this file a LOT.

🧩 core/ → the real game logic

This is the heart.

game.py → main loop + state handling

Handles:

pygame init

event loop

switching between menu / playing / game over

It does not know how mines work.

board.py → the minesweeper brain 🧠

Handles:

placing mines

counting neighbors

flood fill reveal

checking win

This file contains zero pygame code.
Pure logic = easy to debug.

tile.py → single cell object

Each tile knows:

is_mine

is_revealed

is_flagged

neighbor_count

This makes the board super clean.

state.py → game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
WIN = 3


So you don’t do weird booleans everywhere.

🎨 ui/ → everything visual but not logic
button.py

Reusable button class (restart, difficulty, etc.)

hud.py

Top bar with:

mines left

timer

smiley face

menu.py

Start screen.

🧰 utils/
loader.py

Loads images/fonts/sounds once.

helpers.py

Small functions like:

def get_tile_from_mouse(pos):

🎯 Why this structure is powerful

Because responsibilities are separated:

Folder	Responsibility
core	game rules
ui	drawing things
assets	files
utils	helpers
main	start program
settings	configuration

You could literally swap Pygame for another engine and core/ would not change.

That’s professional architecture.

🪄 How the flow works
main.py
   ↓
Game (game.py)
   ↓
Board (board.py)
   ↓
Tile (tile.py)


UI talks to Game.
Game talks to Board.
Board talks to Tiles.

Never the opposite direction.

💡 Hidden benefit

When you later add:

difficulty selector

animations

sound

timer

high score saving

themes

You don’t refactor anything. You just add files.

📦 Example: where does “reveal tile” happen?

Mouse click → game.py

Game calls → board.reveal(row, col)

Board updates tiles

Game asks board what changed

UI draws it

Perfect separation.

🧱 This is the difference between:

“school project”
vs
“small indie game architecture”

🧭 If you want ultra-clean code

Make board.py completely Pygame-free.
You can literally test it with pure Python.

That’s chef’s kiss design.