# Python Chess Engine & GUI

A fully playable chess game featuring an engine built from scratch in Python. No external chess libraries were used for move generation or evaluation. Just core algorithms and Pygame for the graphical interface.

## Features

* **Engine:** Minimax algorithm with Alpha-Beta pruning (default depth: 3).
* **Rule Enforcement:** Accurately validates legal moves, including checks, checkmates, and stalemates.
* **Interactive GUI:** An interactive board built with Pygame that prevents invalid moves.
* **Pawn Promotion:** Custom UI overlay for selecting the promoted piece.

## How to run

### Option 1: Play instantly
1. Go to the **Releases** section on the right side of this GitHub page.
2. Download the latest executable file (`.exe`).
3. Run the downloaded file.

### Option 2: Run from source
1. Clone this repository to your local machine.
2. Install the required dependencies: `pip install -r requirements.txt`
3. Run the main script to start the game: `python -m src.main`

## Tech Stack

* **Python**
* **Pygame**

## Known Limitations

* **Side Selection:** Currently, the user can only play as White (the engine automatically plays Black).
* **Missing Draw Rules:** Draws by **insufficient material** and the **50-move rule** are not yet detected.
* **Time Controls:** There are no chess clocks or time limits implemented.