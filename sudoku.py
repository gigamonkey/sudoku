#!/usr/bin/env python3

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
