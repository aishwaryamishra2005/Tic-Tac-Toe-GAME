"""
Cute Pastel Tic-Tac-Toe
-----------------------
A two-player Tic-Tac-Toe game made with Python and Tkinter.

How the code is organised:
  1. Colours / fonts      -> constants at the top (easy to change the look)
  2. Game logic           -> plain functions that know nothing about the GUI
  3. TicTacToeApp class   -> builds the window and connects clicks to the logic
"""

import tkinter as tk

# ---------------------------------------------------------------------------
# 1. LOOK AND FEEL  (change these to restyle the whole app)
# ---------------------------------------------------------------------------
BG_COLOR = "#EDE7FF"        # soft lavender (window background)
CARD_COLOR = "#FFFFFF"      # white (cards and empty squares)
BOARD_COLOR = "#D9CCFF"     # deeper lavender (frame behind the board)
HOVER_COLOR = "#F6F0FF"     # very light lavender (square under the mouse)
WIN_COLOR = "#FFF1B8"       # soft butter yellow (winning squares)

X_COLOR = "#FF7EB6"         # pink  -> Player X
O_COLOR = "#6EB5FF"         # baby blue -> Player O
DRAW_COLOR = "#9B7EDE"      # purple -> draws
TEXT_COLOR = "#5A4A8A"      # dark lavender, easy to read

PLAYER_COLORS = {"X": X_COLOR, "O": O_COLOR}

# Fonts: Tkinter quietly falls back to a default if a font is missing.
TITLE_FONT = ("Arial Rounded MT Bold", 30)
SUBTITLE_FONT = ("Arial Rounded MT Bold", 13)
STATUS_FONT = ("Arial Rounded MT Bold", 18)
SCORE_LABEL_FONT = ("Arial Rounded MT Bold", 12)
SCORE_NUMBER_FONT = ("Arial Rounded MT Bold", 28)
BUTTON_FONT = ("Arial Rounded MT Bold", 14)
SYMBOL_FONT = ("Arial Rounded MT Bold", 64)

CELL_SIZE = 110             # width and height of each square, in pixels


# ---------------------------------------------------------------------------
# 2. GAME LOGIC  (no GUI code here, so it is easy to test and explain)
# ---------------------------------------------------------------------------
# The board is a list of 9 items. Index positions look like this:
#       0 | 1 | 2
#       3 | 4 | 5
#       6 | 7 | 8
# Each item is "" (empty), "X" or "O".

# All 8 ways to win: 3 rows, 3 columns, 2 diagonals.
WINNING_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),    # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),    # columns
    (0, 4, 8), (2, 4, 6),               # diagonals
]


def check_winner(board):
    """Return (winner, winning_line). If nobody has won, return (None, None)."""
    for a, b, c in WINNING_LINES:
        # A line wins if its first square is not empty and all 3 squares match.
        if board[a] != "" and board[a] == board[b] == board[c]:
            return board[a], (a, b, c)
    return None, None


def is_draw(board):
    """A draw means every square is filled and nobody has won."""
    winner, _ = check_winner(board)
    return winner is None and "" not in board


def other_player(player):
    """Return the player whose turn comes next."""
    return "O" if player == "X" else "X"


# ---------------------------------------------------------------------------
# 3. THE APP  (builds the window and reacts to clicks)
# ---------------------------------------------------------------------------
class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)
        self.root.minsize(460, 0)               # a little extra side space

        # --- Game state (everything the game needs to remember) ---
        self.board = [""] * 9                       # the 9 squares
        self.current_player = "X"                   # X always starts a round
        self.game_over = False                      # True once someone wins / draw
        self.scores = {"X": 0, "O": 0, "Draw": 0}   # the scoreboard numbers

        # --- Widgets we need to update later ---
        self.cells = []             # the 9 square widgets (Canvas)
        self.score_labels = {}      # the 3 score number labels
        self.status_label = None    # "Player X's turn" banner

        self.build_header()
        self.build_scoreboard()
        self.build_status()
        self.build_board()
        self.build_buttons()

        self.start_new_round()

    # ------------------------- building the screen -------------------------
    def build_header(self):
        """Playful title at the top."""
        tk.Label(self.root, text="\u273F Tic Tac Toe \u273F", font=TITLE_FONT,
                 bg=BG_COLOR, fg=X_COLOR).pack(pady=(22, 0))
        tk.Label(self.root, text="two players  \u2022  one board  \u2022  lots of fun",
                 font=SUBTITLE_FONT, bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=(0, 14))

    def build_scoreboard(self):
        """Three little cards: Player X wins, Draws, Player O wins."""
        row = tk.Frame(self.root, bg=BG_COLOR)
        row.pack(pady=(0, 12))

        # (key in self.scores, caption, colour)
        cards = [("X", "Player X", X_COLOR),
                 ("Draw", "Draws", DRAW_COLOR),
                 ("O", "Player O", O_COLOR)]

        for key, caption, color in cards:
            card = tk.Frame(row, bg=CARD_COLOR, width=110, height=90)
            card.pack(side="left", padx=8)
            card.pack_propagate(False)      # keep the fixed card size

            tk.Label(card, text=caption, font=SCORE_LABEL_FONT,
                     bg=CARD_COLOR, fg=color).pack(pady=(10, 0))
            number = tk.Label(card, text="0", font=SCORE_NUMBER_FONT,
                              bg=CARD_COLOR, fg=color)
            number.pack()
            self.score_labels[key] = number

    def build_status(self):
        """The banner that says whose turn it is (or who won)."""
        self.status_label = tk.Label(self.root, text="", font=STATUS_FONT,
                                     bg=BG_COLOR, fg=TEXT_COLOR)
        self.status_label.pack(pady=(4, 10))

    def build_board(self):
        """Create the 3x3 grid of clickable squares."""
        frame = tk.Frame(self.root, bg=BOARD_COLOR, padx=8, pady=8)
        frame.pack()

        for index in range(9):
            row, col = divmod(index, 3)     # turn 0-8 into a row and column
            cell = tk.Canvas(frame, width=CELL_SIZE, height=CELL_SIZE,
                             bg=CARD_COLOR, highlightthickness=0, cursor="hand2")
            cell.grid(row=row, column=col, padx=5, pady=5)

            # "i=index" makes each square remember its own number.
            cell.bind("<Button-1>", lambda event, i=index: self.handle_click(i))
            cell.bind("<Enter>", lambda event, i=index: self.on_hover(i, True))
            cell.bind("<Leave>", lambda event, i=index: self.on_hover(i, False))
            self.cells.append(cell)

    def build_buttons(self):
        """Play Again and Reset Score buttons."""
        row = tk.Frame(self.root, bg=BG_COLOR)
        row.pack(pady=(18, 24))

        self.make_button(row, "Play Again", self.start_new_round,
                         "#FFB6D5", "#FF9CC5").pack(side="left", padx=8)
        self.make_button(row, "Reset Score", self.reset_scores,
                         "#B5D8FF", "#9CCBFF").pack(side="left", padx=8)

    def make_button(self, parent, text, command, color, hover_color):
        """
        Make a rounded-looking button.
        (We use a Label instead of tk.Button because macOS ignores the
        background colour of normal Tkinter buttons.)
        """
        button = tk.Label(parent, text=text, font=BUTTON_FONT, bg=color,
                          fg="white", padx=22, pady=10, cursor="hand2")
        button.bind("<Button-1>", lambda event: command())
        button.bind("<Enter>", lambda event: button.config(bg=hover_color))
        button.bind("<Leave>", lambda event: button.config(bg=color))
        return button

    # ----------------------------- game actions ----------------------------
    def start_new_round(self):
        """Clear the board for a new round. Scores are NOT touched."""
        self.board = [""] * 9
        self.current_player = "X"
        self.game_over = False

        for cell in self.cells:
            cell.delete("all")                  # remove any X or O drawing
            cell.config(bg=CARD_COLOR)

        self.show_turn()

    def reset_scores(self):
        """Set all scores to 0 and start a fresh round."""
        self.scores = {"X": 0, "O": 0, "Draw": 0}
        self.update_scoreboard()
        self.start_new_round()

    def handle_click(self, index):
        """Called whenever a square is clicked. This is the heart of the game."""
        # 1. Ignore clicks after the round has ended.
        if self.game_over:
            return

        # 2. Don't allow a square that is already taken.
        if self.board[index] != "":
            self.status_label.config(text="That square is taken! \u2639", fg=DRAW_COLOR)
            self.root.after(1200, self.show_turn_if_playing)
            return

        # 3. Place the current player's symbol.
        self.board[index] = self.current_player
        self.draw_symbol(index, self.current_player)

        # 4. Did this move win the game?
        winner, line = check_winner(self.board)
        if winner:
            self.end_round_with_win(winner, line)
        # 5. Or is the board full (a draw)?
        elif is_draw(self.board):
            self.end_round_with_draw()
        # 6. Otherwise, pass the turn to the other player.
        else:
            self.current_player = other_player(self.current_player)
            self.show_turn()

    def end_round_with_win(self, winner, line):
        """Show the winner, highlight the winning line and add a point."""
        self.game_over = True
        self.scores[winner] += 1
        self.update_scoreboard()

        for index in line:
            self.cells[index].config(bg=WIN_COLOR)
        self.status_label.config(text=f"\u2605 Player {winner} wins! \u2605",
                                 fg=PLAYER_COLORS[winner])

    def end_round_with_draw(self):
        """Nobody won: show a draw message and add a draw point."""
        self.game_over = True
        self.scores["Draw"] += 1
        self.update_scoreboard()
        self.status_label.config(text="It's a draw! \u2661", fg=DRAW_COLOR)

    # ------------------------------ drawing -------------------------------
    def draw_symbol(self, index, player):
        """Draw a big X or O in the middle of a square."""
        cell = self.cells[index]
        cell.delete("all")
        cell.create_text(CELL_SIZE // 2, CELL_SIZE // 2, text=player,
                         font=SYMBOL_FONT, fill=PLAYER_COLORS[player])
        cell.config(bg=CARD_COLOR)

    def on_hover(self, index, mouse_is_over):
        """Light highlight when the mouse is over an empty square."""
        if self.game_over or self.board[index] != "":
            return
        self.cells[index].config(bg=HOVER_COLOR if mouse_is_over else CARD_COLOR)

    def show_turn(self):
        """Update the banner to say whose turn it is."""
        self.status_label.config(text=f"Player {self.current_player}'s turn",
                                 fg=PLAYER_COLORS[self.current_player])

    def show_turn_if_playing(self):
        """Restore the turn message (used after the 'square taken' warning)."""
        if not self.game_over:
            self.show_turn()

    def update_scoreboard(self):
        """Copy the numbers in self.scores onto the screen."""
        for key, label in self.score_labels.items():
            label.config(text=str(self.scores[key]))


# ---------------------------------------------------------------------------
# Start the program
# ---------------------------------------------------------------------------
def main():
    root = tk.Tk()
    TicTacToeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
