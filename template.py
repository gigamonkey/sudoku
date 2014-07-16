#!/usr/bin/env python3

## If you copy this file and then replace all the 'pass' statements
## with an implementation of the function, you should have a working
## Sudoku solver.

from sudoku import digits, main

#
# Recursive depth first search
#
def search(board):
    if board is None or solved(board): return board

    square = empty_square(board)
    for digit in possible_digits(board, square):
        solution = search(assign(board, square, digit))
        if solution: return solution

    return None

def solved(board):
    "Returns true if the given board is already solved."
    pass

def empty_square(board):
    "Return an empty square to try to fill."
    pass

def possible_digits(board, square):
    "Return list of digits to try putting in square s."
    pass

def assign(board, square, digit):
    "Return new board with digit d in square s."
    pass

def solve(givens):
    "Given a list of givens, return a solution in the form of a list of digits."
    pass

main(solve)
