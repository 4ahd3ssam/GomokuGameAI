import math
import copy


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


class Board:
    def __init__(self):
        self.grid = [[EMPTY_CELL for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def display(self):
        print("\n------------------- Current Board -------------------\n")
        print("   " + "  ".join(f"{i:2}" for i in range(BOARD_SIZE)))
        for idx, row in enumerate(self.grid):
            print(f"{idx:2}  " + "   ".join(row))
        print("\n-----------------------------------------------------\n")

    def is_valid_move(self, row, col):
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.grid[row][col] == EMPTY_CELL

    def make_move(self, row, col, symbol):
        if self.is_valid_move(row, col):
            self.grid[row][col] = symbol
            return True
        return False

    def check_winner(self, symbol):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (
                    row + 4 < BOARD_SIZE and all(self.grid[row + i][col] == symbol for i in range(5)) or
                    col + 4 < BOARD_SIZE and all(self.grid[row][col + i] == symbol for i in range(5)) or
                    row + 4 < BOARD_SIZE and col + 4 < BOARD_SIZE and all(self.grid[row + i][col + i] == symbol for i in range(5)) or
                    row + 4 < BOARD_SIZE and col - 4 >= 0 and all(self.grid[row + i][col - i] == symbol for i in range(5))
                ):
                    return True
        return False
   
    def get_empty_cells(self):
        return [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if self.grid[r][c] == EMPTY_CELL]

class Player:
    def __init__(self, symbol, is_ai=False, ai_name=None):
        self.symbol = symbol
        self.is_ai = is_ai
        self.ai_name = ai_name  #  minimax or alphabeta 


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
                    bestMove = minimax.getBestMove()  # Get the best move for the AI (minimax)
                    print(f"AI ({self.current_player.symbol}) chooses move: {bestMove}")
                    self.board.make_move(bestMove[0], bestMove[1], self.current_player.symbol)  # Make AI's move

                elif self.current_player.ai_name == "alphabeta":
                    # Implement Alpha-Beta logic here
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


if __name__ == "__main__":
    while True:
        print("====== Gomoku Game ======")
        print("1. Human vs AI (Minimax)")
        print("2. AI (Minimax) vs AI (Alpha-Beta)")
        print("3. Exit")
        choice = input("Select mode (1-3): ").strip()

        if choice == '1':
            player1 = Player('X')  
            player2 = Player('O', is_ai=True, ai_name="minimax")
            game = GomokuGame(player1, player2)
            game.play()

        elif choice == '2':
            player1 = Player('X', is_ai=True, ai_name="minimax")
            player2 = Player('O', is_ai=True, ai_name="alphabeta")
            game = GomokuGame(player1, player2)
            game.play()

        elif choice == '3':
            print("Thanks for playing Gomoku!")
            break

        else:
            print(" Please Only  choose 1, 2, or 3.")


