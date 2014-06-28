#!/usr/bin/env python3

# If we use a 81-element list as our board, these give us lists of
# lists of indices of various groupings of squares.
rows  = [ list(range(r*9, (r+1)*9)) for r in range(9) ]
cols  = [ list(range(c, 81, 9)) for c in range(9) ]
boxes = [ [ r*9 + c for r in range(x, x+3) for c in range(y, y+3) ] for x in (0, 3, 6) for y in (0, 3, 6) ]

#
# Given a board with some squares filled in, return a board completely
# filled in or None if there is no solution.
#
def solve(board):
    if board:
        s = empty_square(board)
        if s is None:
            return board
        else:
            for d in possible_digits(board, s):
                solution = solve(assign(board, s, d))
                if solution: return solution
    else:
        return None

def empty_square(board): pass

def possible_digits(board, s): pass

def assign(board, s, d): pass
