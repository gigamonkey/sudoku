#!/usr/bin/env python3

from sudoku import digits, main

rows  = [ [ r*9 + c for c in range(9) ] for r in range(9) ]
cols  = [ [ r*9 + c for r in range(9) ] for c in range(9) ]
boxes = [ [ r*9 + c for r in range(rs*3, (rs+1)*3) for c in range(cs*3, (cs+1)*3) ]
          for rs, cs in (divmod(b, 3) for b in range(9)) ]

squares   = range(81)
all_units = rows + cols + boxes
units     = [ [ u for u in all_units if s in u ] for s in squares ]
peers     = [ set().union(*units[s]) - {s} for s in squares ]

#
# Recursive depth first search
#
def search(b):
    if b is None or solved(b): return b

    s = empty_square(b)
    for d in possible_digits(b, s):
        solution = search(assign(b, s, d))
        if solution: return solution

    return None

def solved(b): return not any(s is None for s in b)

def empty_square(b):
    try:
        return b.index(None)
    except:
        return None

def possible_digits(b, s):
    return digits

def assign(b, s, d):
    new_board = b.copy()
    new_board[s] = d
    return new_board if not contradiction(new_board) else None

def contradiction(b):
    return not all(okay(b, s) for s in squares if b[s] is not None)

def okay(b, s):
    return not any(b[s] == b[p] for p in peers[s])

def solve(givens):
    return search(givens)

main(solve)
