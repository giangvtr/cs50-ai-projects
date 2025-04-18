"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None

class InvalidAction(Exception):
    pass


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] != EMPTY : 
                count = count + 1

    if count%2 == 0 : 
        return X
    else : return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_cells = set()
    for row in range(len(board)):
        for col in range(len(board[row])):
            cell = board[row][col]
            if cell == EMPTY :
                possible_cells.add((row,col))
    
    return possible_cells

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    current_player = player(board)
    row, col = action
            
    if board[row][col] != EMPTY :
        raise InvalidAction("Cell is already occupied.")
    
    if row < 0 or col < 0 or row > 2 or col > 2:
        raise InvalidAction("Cell coordinations are out of bound")
    
    else : 
        # Function should not modify the input board
        new_board = deepcopy(board)
        new_board[row][col] = current_player
        return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winning_cases = [
        # Rows
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        # Columns
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        # Diagonals
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]]
    ]

    for case in winning_cases : 
        if case[0] == case[1] == case[2] and case[0] != EMPTY : 
            return case[0]

    
def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None : 
        return True
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == EMPTY : 
                return False
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X : 
        return 1
    elif winner(board) == O :
        return -1
    else : 
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board) == True : 
        return None
    
    if player(board) == X : 
        best_action, _ = max_value(board)
        return best_action
    
    if player(board) == O :
        best_action, _ = min_value(board)
        return best_action
            
def max_value(board):
    if terminal(board) :
        return (None, utility(board))
    max_found = float('-inf')
    best_action = (0,0)
    for action in actions(board):
        _, min_found = min_value(result(board,action))
        new_max = max(max_found, min_found)

        if new_max > max_found:
            max_found = new_max
            best_action = action

    return (best_action,max_found)

def min_value(board):
    if terminal(board):
        return (None, utility(board))
    min_found = float('inf')
    best_action = (0,0)
    for action in actions(board):
        _, max_found = max_value(result(board,action))
        new_min = min(min_found, max_found)

        if new_min < min_found:
            min_found = new_min
            best_action = action
    return (best_action,min_found)