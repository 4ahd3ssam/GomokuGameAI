import tkinter as tk
from tkinter import messagebox
from functools import partial
import math

BOARD_SIZE = 15
EMPTY_CELL = '.'


class MiniMax:
    def __init__(self, board, maximizer, minimizer, maxDepth = 1):
        self.board = board # Instance of the current board state
        self.maximizer = maximizer # Player 'O', trie to maximize their score
        self.minimizer = minimizer # Opponent 'X', trie to minimze the maximizer score
        self.maxDepth = maxDepth # Maximum number of moves to explore

    def getBestMove(self):
        bestScore = -math.inf # MIN_INT
        bestMove = None

        for row, col in self.board.get_empty_cells(): # Iterate over all empty cells
            self.board.make_move(row, col, self.maximizer.symbol) # Make move
            score = self.minimax(self.maxDepth - 1, False) # Get the best
            self.board.grid[row][col] = EMPTY_CELL  # Undo move

            if score > bestScore: # If this is the maximum score 
                bestScore = score
                bestMove = (row, col) # Get its cell

        return bestMove # return the best move for the maximizer

    # Algorithm to determine the best move of a player
    # Maximize the player score
    # Minimze the opponent score
    # Based on DFS "try all possible future moves", but limited to the depth 
    def minimax(self, depth, isMaximizing):
        # Base cases
        if self.board.check_winner(self.maximizer.symbol): # If maximizer wins
            return 1
        elif self.board.check_winner(self.minimizer.symbol): # If minimizer wins
            return -1
        elif depth == 0 or not self.board.get_empty_cells(): # If no more depth or the game is over
            return 0  # Draw or depth limit

        if isMaximizing: # Maximizer turn
            bestScore = -math.inf # MIN_INT
            for row, col in self.board.get_empty_cells(): # Iterate over all possible moves
                self.board.make_move(row, col, self.maximizer.symbol) # Make a move
                score = self.minimax(depth - 1, False) # Switch to the opponent turn
                self.board.grid[row][col] = EMPTY_CELL # Backtrack to make the cell empty again
                bestScore = max(score, bestScore) # Track the max score 
            return bestScore
        else: # Minimizer turn
            bestScore = math.inf # MAX_INT
            for row, col in self.board.get_empty_cells(): # Iterate over all possible moves
                self.board.make_move(row, col, self.minimizer.symbol) # Make a move
                score = self.minimax(depth - 1, True) # Switch to the player turn
                self.board.grid[row][col] = EMPTY_CELL # Backtrack to make the cell empty again
                bestScore = min(score, bestScore) # Track the min score 
            return bestScore

class AlphaBeta:
    def __init__(self, board, maximizer, minimizer, maxDepth=2):
        self.board = board
        self.maximizer = maximizer
        self.minimizer = minimizer
        self.maxDepth = maxDepth

    def getBestMove(self):
        bestScore = -math.inf
        bestMove = None

        for row, col in self.board.get_candidate_moves():
            self.board.make_move(row, col, self.maximizer.symbol)
            score = self.alphabeta(self.maxDepth - 1, -math.inf, math.inf, False)
            self.board.grid[row][col] = EMPTY_CELL

            if score > bestScore:
                bestScore = score
                bestMove = (row, col)

        return bestMove

    def alphabeta(self, depth, alpha, beta, isMaximizing):
        if self.board.check_winner(self.maximizer.symbol):
            return 1
        elif self.board.check_winner(self.minimizer.symbol):
            return -1
        elif depth == 0 or not self.board.get_empty_cells():
            return self.board.evaluate(self.maximizer.symbol)

        if isMaximizing:
            value = -math.inf
            for row, col in self.board.get_candidate_moves():
                self.board.make_move(row, col, self.maximizer.symbol)
                value = max(value, self.alphabeta(depth - 1, alpha, beta, False))
                self.board.grid[row][col] = EMPTY_CELL
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return value
        else:
            value = math.inf
            for row, col in self.board.get_candidate_moves():
                self.board.make_move(row, col, self.minimizer.symbol)
                value = min(value, self.alphabeta(depth - 1, alpha, beta, True))
                self.board.grid[row][col] = EMPTY_CELL
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value


class Board:
    def __init__(self, board_size=BOARD_SIZE):
        self.board_size = board_size
        self.grid = [[EMPTY_CELL for _ in range(self.board_size)] for _ in range(self.board_size)]

    def display(self):
        print("\n------------------- Current Board -------------------\n")
        print("   " + "  ".join(f"{i:2}" for i in range(BOARD_SIZE)))
        for idx, row in enumerate(self.grid):
            print(f"{idx:2}  " + "   ".join(row))
        print("\n-----------------------------------------------------\n")

    def is_valid_move(self, row, col):
        return 0 <= row < self.board_size and 0 <= col < self.board_size and self.grid[row][col] == EMPTY_CELL

    def make_move(self, row, col, symbol):
        if self.is_valid_move(row, col):
            self.grid[row][col] = symbol
            return True
        return False

    def check_winner(self, symbol):
        for row in range(self.board_size):
            for col in range(self.board_size):
                # Check horizontal (left to right)
                if col + 4 < self.board_size and all(self.grid[row][col + i] == symbol for i in range(5)):
                    return True
                # Check vertical (top to bottom)
                if row + 4 < self.board_size and all(self.grid[row + i][col] == symbol for i in range(5)):
                    return True
                # Check diagonal (top-left to bottom-right)
                if row + 4 < self.board_size and col + 4 < self.board_size and all(
                        self.grid[row + i][col + i] == symbol for i in range(5)):
                    return True
                # Check diagonal (top-right to bottom-left)
                if row + 4 < self.board_size and col - 4 >= 0 and all(
                        self.grid[row + i][col - i] == symbol for i in range(5)):
                    return True
        return False

    def get_empty_cells(self):
        return [(r, c) for r in range(self.board_size) for c in range(self.board_size) if self.grid[r][c] == EMPTY_CELL]

    def get_candidate_moves(self, distance=2):
        candidates = set()

        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.grid[r][c] != EMPTY_CELL:
                    for dr in range(-distance, distance + 1):
                        for dc in range(-distance, distance + 1):
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < self.board_size and 0 <= nc < self.board_size:
                                if self.grid[nr][nc] == EMPTY_CELL:
                                    candidates.add((nr, nc))

        # Fallback to full board if no moves are near existing stones (e.g., empty board)
        return list(candidates) if candidates else self.get_empty_cells()

    def evaluate_direction(self, r, c, player, opponent, dr, dc):
        max_len = 5
        if not (0 <= r + (max_len - 1) * dr < self.board_size) or not (0 <= c + (max_len - 1) * dc < self.board_size):
            return 0

        line = [self.grid[r + i * dr][c + i * dc] for i in range(max_len)]

        if opponent not in line:
            player_count = line.count(player)
            if player_count == 2:
                return 10
            elif player_count == 3:
                return 50
            elif player_count == 4:
                return 200
        if player not in line:
            opp_count = line.count(opponent)
            if opp_count == 2:
                return -10
            elif opp_count == 3:
                return -50
            elif opp_count == 4:
                return -200
        return 0

    def evaluate(self, symbol):
        opponent = 'O' if symbol == 'X' else 'X'
        score = 0

        for r in range(self.board_size):
            for c in range(self.board_size):
                score += self.evaluate_direction(r, c, symbol, opponent, 0, 1)   # horizontal
                score += self.evaluate_direction(r, c, symbol, opponent, 1, 0)   # vertical
                score += self.evaluate_direction(r, c, symbol, opponent, 1, 1)   # diag ↘
                score += self.evaluate_direction(r, c, symbol, opponent, 1, -1)  # diag ↙

        return score

class Player:
    def __init__(self, symbol, is_ai=False, ai_name=None):
        self.symbol = symbol
        self.is_ai = is_ai
        self.ai_name = ai_name  # minimax or alphabeta


class GomokuGame:
    def __init__(self, player1, player2):
        self.board = Board()
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1

    def switch_turn(self):
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def play(self):
        while True:
            self.board.display()
            print(f"Player {self.current_player.symbol}'s turn.")

            if self.current_player.is_ai:
                print(f"Current player is AI ({self.current_player.ai_name})")
                if self.current_player.ai_name == "minimax":
                    minimax = MiniMax(self.board, self.player1, self.player2)
                    bestMove = minimax.getBestMove()
                    print(f"AI ({self.current_player.symbol}) chooses move: {bestMove}")
                    self.board.make_move(bestMove[0], bestMove[1], self.current_player.symbol)

                elif self.current_player.ai_name == "alphabeta":
                    alphabeta = AlphaBeta(self.board, self.player2, self.player1)
                    bestMove = alphabeta.getBestMove()
                    print(f"AI ({self.current_player.symbol}) chooses move: {bestMove}")
                    self.board.make_move(bestMove[0], bestMove[1], self.current_player.symbol)
                    pass

            else:
                try:
                    row_col = input("Enter your move (row col) or 'exit': ").strip()
                    if row_col.lower() == 'exit':
                        print("Game exited.")
                        break
                    row, col = map(int, row_col.split())
                except ValueError:
                    print("Invalid input. Please enter two numbers separated by space like  1 1.")
                    continue

                if not self.board.make_move(row, col, self.current_player.symbol):
                    print("Invalid move. Try again.")
                    continue

            if self.board.check_winner(self.current_player.symbol):
                self.board.display()
                print(f"🏆 Player {self.current_player.symbol} wins!")
                break

            self.switch_turn()


# Test Without GUI
# if __name__ == "__main__":
#     while True:
#         print("====== Gomoku Game ======")
#         print("1. Human vs AI (Minimax)")
#         print("2. AI (Minimax) vs AI (Alpha-Beta)")
#         print("3. Exit")
#         choice = input("Select mode (1-3): ").strip()
#
#         if choice == '1':
#             player1 = Player('X')
#             player2 = Player('O', is_ai=True, ai_name="minimax")
#             game = GomokuGame(player1, player2)
#             game.play()
#
#         elif choice == '2':
#             player1 = Player('X', is_ai=True, ai_name="minimax")
#             player2 = Player('O', is_ai=True, ai_name="alphabeta")
#             game = GomokuGame(player1, player2)
#             game.play()
#
#         elif choice == '3':
#             print("Thanks for playing Gomoku!")
#             break
#
#         else:
#             print(" Please Only  choose 1, 2, or 3.")


# ---------------------------------<<        GUI       >> -----------------------------

class Menu:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Gomoku Game")
        self.root.configure(bg="#F0F4F8")

        window_width = root.winfo_screenwidth()
        window_height = root.winfo_screenheight()
        root.geometry(f"{window_width}x{window_height}+0+0")

        top_frame = tk.Frame(root, bg="#F0F4F8")
        top_frame.pack(side="top", anchor="n", ipady=100)  # Stick to top with padding

        self.label = tk.Label(top_frame,
                              text="🎮 Choose Game Mode",
                              font=("Segoe UI", 32, "bold"),
                              bg="#F0F4F8",
                              fg="#333333")
        self.label.pack(pady=(30, 50))

        button_style = {
            "width": 30,
            "height": 2,
            "font": ("Segoe UI", 16, "bold"),
            "bg": "#1E88E5",
            "fg": "white",
            "activebackground": "#1565C0",
            "activeforeground": "white",
            "bd": 0,
            "highlightthickness": 2,
            "highlightbackground": "#FFD54F",
            "highlightcolor": "#FFD54F",
            "cursor": "hand2"
        }

        self.button1 = tk.Button(top_frame, text="👤  Human vs AI (Minimax)",
                                 command=lambda: self.get_board_size("human_vs_ai"),
                                 **button_style)
        self.button1.pack(pady=10)

        self.button2 = tk.Button(top_frame, text="🤖  AI (Minimax) vs AI (Alpha-Beta)",
                                 command=lambda: self.get_board_size("ai_vs_ai"),
                                 **button_style)
        self.button2.pack(pady=10)

        self.button3 = tk.Button(top_frame, text="❌  Exit", command=root.quit, **button_style)
        self.button3.pack(pady=10)

    def get_board_size(self, mode):
        self.selected_mode = mode
        self.board_size_window = tk.Toplevel(self.root)
        self.board_size_window.title("Enter Board Size")

        window_width = 400
        window_height = 250
        screen_width = self.root.winfo_screenwidth()
        x_coordinate = (screen_width - window_width) // 2

        self.board_size_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+100")
        self.board_size_window.configure(bg="#1E88E5")

        label = tk.Label(self.board_size_window, text="Enter Board Size :", font=("Segoe UI", 14, "bold"), fg="white",
                         bg="#1E88E5")
        label.pack(pady=10)

        self.board_size_entry = tk.Entry(self.board_size_window, font=("Segoe UI", 14))
        self.board_size_entry.pack(pady=5)

        if self.selected_mode == "human_vs_ai":
            self.ai_choice = tk.StringVar(value="minimax")

            tk.Label(self.board_size_window, text="Choose AI Strategy:", font=("Segoe UI", 12, "bold"),
                     fg="white", bg="#1E88E5").pack(pady=(10, 0))

            tk.Radiobutton(self.board_size_window, text="Minimax", variable=self.ai_choice, value="minimax",
                           font=("Segoe UI", 12), bg="#1E88E5", fg="white", selectcolor="#1565C0").pack()

            tk.Radiobutton(self.board_size_window, text="Alpha-Beta", variable=self.ai_choice, value="alphabeta",
                           font=("Segoe UI", 12), bg="#1E88E5", fg="white", selectcolor="#1565C0").pack()


        button = tk.Button(self.board_size_window, text=" Start Game ", font=("Segoe UI", 14, "bold"),
                           command=self.start_game, bg="white")
        button.pack(pady=15)

    def start_game(self):
        try:
            board_size = int(self.board_size_entry.get())
            if 5 <= board_size <= 20:
                self.board_size_window.destroy()  # Close  board size window
                self.root.destroy()  # Close  menu window
                new_root = tk.Tk()
                ai_mode = self.ai_choice.get() if self.selected_mode == "human_vs_ai" else None
                GomokuGUI(new_root, board_size, self.selected_mode, ai_mode)
                new_root.mainloop()
            else:
                messagebox.showerror("Invalid Size", "Please enter a size between 5 and 20.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the board size.")


class GomokuGUI:
    def __init__(self, root, board_size, mode, ai_mode=None):
        self.root = root
        self.board_size = board_size
        self.root.title("Gomoku Game")
        self.board = Board(self.board_size)
        self.mode = mode
        self.ai_mode = ai_mode
        self.set_players(mode)
        self.buttons = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        window_width = root.winfo_screenwidth()
        window_height = root.winfo_screenheight()
        root.geometry(f"{window_width}x{window_height}+0+0")
        self.status_label = tk.Label(self.root, text="Welcome to Gomoku!", font=("Arial", 20, "bold"), bg="#1E88E5",
                                     fg="white")
        self.status_label.pack(pady=(10, 0))

        self.root.configure(bg="#1E88E5")
        self.create_widgets()

        # To start AI vs AI
        if self.player1.is_ai and self.player2.is_ai:
            self.root.after(500, self.minMax_move)

    def set_players(self, mode):
        if mode == "human_vs_ai":
            self.player1 = Player('X')  # human
            self.player2 = Player('O', is_ai=True, ai_name=self.ai_mode or "minimax")
        elif mode == "ai_vs_ai":
            self.player1 = Player('X', is_ai=True, ai_name="minimax")
            self.player2 = Player('O', is_ai=True, ai_name="alphabeta")
        self.current_player = self.player1

    def create_widgets(self):

        self.board_frame = tk.Frame(self.root, bg="#1E88E5")
        self.board_frame.pack(expand=True)  # frame is centered in the window

        for r in range(self.board_size):
            for c in range(self.board_size):
                btn = tk.Button(self.board_frame, text=EMPTY_CELL, width=4, height=1,
                                font=("Arial", 13, "bold"), bg="white", fg="black",
                                relief="raised", bd=0,
                                command=partial(self.cell_clicked, r, c),
                                activebackground="lightblue", activeforeground="white")
                btn.grid(row=r, column=c, padx=2, pady=2)
                self.buttons[r][c] = btn

    def cell_clicked(self, row, col):
        if not self.board.is_valid_move(row, col) or self.current_player.is_ai:
            return

        self.board.make_move(row, col, self.current_player.symbol)
        self.buttons[row][col]['text'] = self.current_player.symbol
        if self.current_player.symbol == 'X':
            self.buttons[row][col]['fg'] = 'red'
        elif self.current_player.symbol == 'O':
            self.buttons[row][col]['fg'] = 'green'

        if self.check_game_end():
            return

        self.switch_turn()
        self.root.after(500, self.minMax_move)

    def minMax_move(self):
        if self.current_player.is_ai:
            if self.current_player.ai_name == "minimax":
                ai = MiniMax(self.board, self.player1, self.player2)
            elif self.current_player.ai_name == "alphabeta":
                ai = AlphaBeta(self.board, self.player2, self.player1)
            else:
                return

            bestMove = ai.getBestMove()

            self.board.make_move(bestMove[0], bestMove[1], self.current_player.symbol)
            self.buttons[bestMove[0]][bestMove[1]]['text'] = self.current_player.symbol

            if self.current_player.symbol == 'X':
                self.buttons[bestMove[0]][bestMove[1]]['fg'] = 'red'
            elif self.current_player.symbol == 'O':
                self.buttons[bestMove[0]][bestMove[1]]['fg'] = 'green'

            if self.check_game_end():
                return

            self.switch_turn()

            self.root.after(500, self.minMax_move)  # AI takes the next turn after a delay

    def switch_turn(self):
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def check_game_end(self):
        if self.board.check_winner(self.current_player.symbol):
            messagebox.showinfo("Game Over", f"🏆 Player {self.current_player.symbol} wins!")
            self.root.quit()
            return True
        elif not self.board.get_empty_cells():
            messagebox.showinfo("Game Over", "It's a draw!")
            self.root.quit()
            return True
        return False


if __name__ == "__main__":
    root = tk.Tk()
    Menu(root)
    root.mainloop()
