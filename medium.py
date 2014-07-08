#!/usr/bin/env python3

import sudoku

def row(r): return [ r*9 + c for c in range(9) ]
def col(c): return [ r*9 + c for r in range(9) ]
def box(b):
    rs, cs = [ range(n * 3, (n+1) * 3) for n in divmod(b, 3) ]
    return [ r*9 + c for r in rs for c in cs ]

squares = range(81)

rows  = [ row(r) for r in range(9) ]
cols  = [ col(c) for c in range(9) ]
boxes = [ box(b) for b in range(9) ]
units = [ [ u for u in (rows + cols + boxes) if s in u ] for s in squares ]
peers = [ set(sum(units[s], [])) - {s} for s in squares ]

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

def board(givens): return givens

def to_list(b): return b

def solved(b): return not any(s is None for s in b)

def empty_square(b):
    try:
        return b.index(None)
    except:
        return None

def possible_digits(b, s):
    return [ d for d in sudoku.digits if legal_digit(b, s, d) ]

def legal_digit(b, s, d):
    return not any(b[p] == d for p in peers[s])

def assign(b, s, d):
    new_board = b.copy()
    new_board[s] = d
    return new_board if not contradiction(new_board) else None

def contradiction(b):
    return not all(okay(b, s) for s in squares if b[s] is not None)

def okay(b, s):
    return not any(b[s] == b[p] for p in peers[s])


sudoku.main(board, solve, to_list)
