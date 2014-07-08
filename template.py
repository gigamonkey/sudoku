#!/usr/bin/env python3

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
    raise Exception("Not yet implemented")

def empty_square(b):
    "Return an empty square to try to fill."
    raise Exception("Not yet implemented")

def possible_digits(b, s):
    "Return list of digits to try putting in square s."
    raise Exception("Not yet implemented")

def assign(b, s, d):
    "Return new board with digit d in square s."
    raise Exception("Not yet implemented")o

def solve(givens):
    "Given a list of givens, return a solution."
    raise Exception("Not yet implemented")

sudoku.main(solve)
