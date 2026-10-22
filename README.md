# Tic Tac Toe

A cute, pastel-themed two-player Tic-Tac-Toe game built with **Python** and **Tkinter**. Two players take turns on the same computer, with a live scoreboard that keeps track of wins and draws.

## 🎮 Game Preview

Here is a preview of my Tic-Tac-Toe game!

![Tic-Tac-Toe Game Screenshot](Screenshots/game.png)

## Features

- Two players (X and O) taking turns on the same computer
- Shows whose turn it is
- Blocks moves on squares that are already taken
- Detects all 8 winning combinations (3 rows, 3 columns, 2 diagonals)
- Highlights the winning line and shows a winner message
- Detects a draw when all 9 squares are filled
- Scoreboard for Player X wins, Player O wins and draws
- **Play Again** button starts a new round and keeps the scores
- **Reset Score** button clears the scores and starts fresh
- Pastel design in lavender, pink, baby blue and white

## Requirements

- Python 3.8 or newer
- Tkinter (included with the Python installer from [python.org](https://www.python.org/downloads/))

No other libraries are needed.

## How to Run

1. Download or clone this repository:
   ```
   git clone https://github.com/YOUR-USERNAME/tic-tac-toe.git
   cd tic-tac-toe
   ```
2. Run the game:
   ```
   python3 tic_tac_toe.py
   ```

On macOS, if you see `No module named '_tkinter'`, install Python from [python.org](https://www.python.org/downloads/) or run `brew install python-tk`.

## How to Play

1. Player **X** goes first. Click any empty square to place your symbol.
2. Players take turns. The banner above the board shows whose turn it is.
3. Get three of your symbols in a row, column or diagonal to win the round.
4. If all nine squares fill up with no winner, the round is a draw.
5. Click **Play Again** for a new round (scores are kept) or **Reset Score** to start completely fresh.

## How It Works

The code is split into three parts:

1. **Constants:** colours and fonts at the top of the file, so the look is easy to change.
2. **Game logic:** plain functions with no GUI code.
   - The board is a list of 9 items (`""`, `"X"` or `"O"`) numbered 0 to 8.
   - `WINNING_LINES` lists the 8 ways to win.
   - `check_winner(board)` finds a winner and the winning line.
   - `is_draw(board)` checks for a full board with no winner.
3. **`TicTacToeApp` class:** builds the Tkinter window and connects clicks to the logic.
   - `handle_click(index)` is the core of the game. It ignores clicks after the round ends, rejects taken squares, places the symbol, checks for a win or draw, and otherwise switches players.
   - `start_new_round()` clears the board without touching the scores.
   - `reset_scores()` zeroes the scores and starts a new round.

## Project Structure

```
tic-tac-toe/
├── tic_tac_toe.py   # the complete game
├── screenshot.png   # image shown in this README
└── README.md
```

## Built With

- [Python](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html), Python's standard GUI library

## Author

Made by Aishwarya Mishra for a college assignment.