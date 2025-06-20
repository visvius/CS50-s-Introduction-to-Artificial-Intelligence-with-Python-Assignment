"""
Tic Tac Toe Player
"""

import math
import copy

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
    countX = 0
    countO = 0
    for row in board:
        for block in row:
            if (block == X):
                countX += 1
            elif (block == O):
                countO += 1
    
    if countX <= countO:
        return X
    else:
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible.add((i,j))
    
    return possible


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # exception for movement outside the matrix
    if(action[0]<0 or action[1]<0 or action[0]>2 or action[1]>2):
        raise ValueError("Invalid action: You can't move there.")
    # exception for taking action on occupied cell
    if board[action[0]][action[1]] != EMPTY:
        raise ValueError("Invalid action: Cell is already occupied.")

    newBoard = copy.deepcopy(board)
    actor = player(board)
    newBoard[action[0]][action[1]] = actor
    return newBoard

# helper function that checks if the actor won the game
def winnerHelper(board, actor):
    # horizontal check
    for i in range(3):
        if (board[i][0]==actor and board[i][1]==actor and board[i][2]==actor):
            return True
    
    # vertical check
    for j in range(3):
        if(board[0][j]==actor and board[1][j]==actor and board[2][j]==actor):
            return True
        
    # diagonal check
    if (board[0][0]==actor and board[1][1]==actor and board[2][2]==actor):
        return True
    if (board[2][0]==actor and board[1][1]==actor and board[0][2]==actor):
        return True
    
    return False

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if(winnerHelper(board, X)):
        return X
    if(winnerHelper(board, O)):
        return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # did X or O win?
    win = winner(board)
    if(win != None):
        return True
    
    # is the board full?
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
            
    # default True since no empty space found
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if(win == X):
        return 1
    elif win == O:
        return -1
    return 0

# dfs is a recursive helper function for minimax implementing dfs
# minmax : 0 -> min (player O), 1 -> max (player X)
def dfs(board, minmax, alpha, beta):
    if terminal(board):
        return (utility(board), 0, 0)
    
    curPlayer = O if minmax==0 else X   #current player taking action
    finalVal = (100, 0, 0) if minmax==0 else (-100, 0, 0)  #stores final returning (utility, moveX, moveY)
    moves = actions(board)
    for move in moves:
        temp = board[move[0]][move[1]]
        board[move[0]][move[1]] = curPlayer

        # currently turn is of minimizing player O
        if(minmax == 0):
            val = dfs(board, 1, alpha, beta)
            beta = min(beta, val[0])
            if (val[0] < finalVal[0]):
                finalVal = (val[0], move[0], move[1])
            # found a smaller value which will be selected by current min fn and not be selected by the parent max fn?
            if(finalVal[0] <= alpha): 
                board[move[0]][move[1]] = temp
                break

        # current player is maximizing player X 
        else:
            val = dfs(board, 0, alpha, beta)
            alpha = max(alpha, val[0])
            if(val[0] > finalVal[0]):
                finalVal = (val[0], move[0], move[1])
            # found a bigger value which will be selected by current max fn and not be selected by the parent min?
            if(finalVal[0] >= beta):
                board[move[0]][move[1]] = temp
                break
        board[move[0]][move[1]] = temp

    return finalVal

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    currPlayer = player(board)
    if(currPlayer == X):
        rec = dfs(board, 1, -100, +100)
    else:
        rec = dfs(board, 0, -100, 100)
    return (rec[1],rec[2])
