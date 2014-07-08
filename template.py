#!/usr/bin/env python3

#
# Recursive depth first search
#
def solve(b):
    if b is None or solved(b): return b

    s = empty_square(b)
    for d in possible_digits(b, s):
        solution = solve(assign(b, s, d))
        if solution: return solution

    return None

def board(text):
    """Given text consisting of digits (1-9) and periods ('.') and
    possibly other characters return whatever representation of a
    board you want to use."""
    raise "Not yet implemented"

def to_list(b):
    """Return a list representing of the cells of the board (from top
    left to bottom right in reading order) with either a digit or
    None."""
    raise "Not yet implemented"

def solved(b):
    """Returns true if the given board is already solved."""
    raise "Not yet implemented"


def empty_square(b):
    """Return an empty square to try to fill."""
    raise "Not yet implemented"

def possible_digits(b, s):
    """Return a list of digits that we want to try putting in square s"""
    raise "Not yet implemented"

def assign(b, s, d):
    """Return a new board the same as the given board b but with digit d
    in square s."""
    raise "Not yet implemented"


sudoku.main(board, solve)
