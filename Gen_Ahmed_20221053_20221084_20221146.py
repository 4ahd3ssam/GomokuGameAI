# ------------------------  Board basic info --------------------- 

BOARD_SIZE = 15
EMPTY_CELL = '.'    
PLAYER_X = 'X'  
PLAYER_O = 'O'    




def create_board():
    return [[EMPTY_CELL for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def print_board(board):
    for i, row in enumerate(board):
        print( " ".join(row))

def is_valid_move(board, row, col):
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and board[row][col] == EMPTY_CELL

def move(board, x, y, player):
    if is_valid_move(board, x, y):
        board[x][y] = player
        return True  
    return False  


def check_is_winner(board, player):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            # horizontal  5  
            if row + 4 < BOARD_SIZE and all(board[row + i][col] == player for i in range(5)):
                return True
            #   vertical
            if col + 4 < BOARD_SIZE and all(board[row][col + i] == player for i in range(5)):
                return True
            # ↘
            if row + 4 < BOARD_SIZE and col + 4 < BOARD_SIZE and all(board[row + i][col + i] == player for i in range(5)):
                return True
            #  ↙
            if row + 4 < BOARD_SIZE and col - 4 >= 0 and all(board[row + i][col - i] == player for i in range(5)):
                return True
    return False 




#  test board 
board = create_board()

print_board(board)

  print("\nBoard after play in  7 7 ")

move(board, 7, 7, PLAYER_X)
print_board(board)