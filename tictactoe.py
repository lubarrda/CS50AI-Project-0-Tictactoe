"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy


X = "X"
O = "O"
EMPTY = None


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
    X_count = sum(row.count(X) for row in board)
    O_count = sum(row.count(O) for row in board)
    
    return X if X_count == O_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    all_possible_actions = set()
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                all_possible_actions.add((i, j))
    
    return all_possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Check if the action is valid
    if action not in actions(board):
        raise Exception("Invalid action.")
    
    new_board = deepcopy(board)
    
    new_board[action[0]][action[1]] = player(board)
    
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    for i in range(3):
        
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != EMPTY:
            return board[i][0]
        
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != EMPTY:
            return board[0][i]
    
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    
    # Check if all cells are filled (no EMPTY cells)
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False  # Game on
    
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0  # Tie or no winner


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    def max_value(state, alfa, beta):
        if terminal(state):
            return utility(state)
        v = float("-inf")
        for action in actions(state):
            v = max(v, min_value(result(state, action), alfa, beta))
            if v >= beta:
                return v
            alfa = max(alfa, v)
        return v

    def min_value(state, alfa, beta):
        if terminal(state):
            return utility(state)
        v = float("inf")
        for action in actions(state):
            v = min(v, max_value(result(state, action), alfa, beta))
            if v <= alfa:
                return v
            beta = min(beta, v)
        return v

    # Check if board is terminal
    if terminal(board):
        return None

    alfa = float("-inf")
    beta = float("inf")

    if player(board) == X:
        # For X player (maximizing player)
        best_value = float("-inf")
        best_move = None
        for action in actions(board):
            move_value = min_value(result(board, action), alfa, beta)
            alfa = max(alfa, move_value)
            if move_value > best_value:
                best_value = move_value
                best_move = action
        return best_move

    else:
        # For O player (minimizing player)
        best_value = float("inf")
        best_move = None
        for action in actions(board):
            move_value = max_value(result(board, action), alfa, beta)
            beta = min(beta, move_value)
            if move_value < best_value:
                best_value = move_value
                best_move = action
        return best_move
