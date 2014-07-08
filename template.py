#!/usr/bin/env python3

## If you copy this file and then replace all the 'pass' statements
## with an implementation of the function, you should have a working
## Sudoku solver.

import sudoku

#
# Recursive depth first search
#
def search(b):
    if b is None or solved(b): return b

    s = empty_square(b)
    for d in possible_digits(b, s):
        solution = solve(assign(b, s, d))
        if solution: return solution

    return None

def solved(b):
    "Returns true if the given board is already solved."
    pass

def empty_square(b):
    "Return an empty square to try to fill."
    pass

def possible_digits(b, s):
    "Return list of digits to try putting in square s."
    pass

def assign(b, s, d):
    "Return new board with digit d in square s."
    pass

def solve(givens):
    "Given a list of givens, return a solution in the form of a list of digits."
    pass

sudoku.main(solve)
