#!/usr/bin/env python3

from sudoku import digits, main

rows  = [ [ r*9 + c for c in range(9) ] for r in range(9) ]
cols  = [ [ r*9 + c for r in range(9) ] for c in range(9) ]
boxes = [ [ r*9 + c for r in range(rs, rs + 3) for c in range(cs, cs + 3) ]
          for rs in (0, 3, 6) for cs in (0, 3, 6) ]

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

def solved(b): return all(len(s) == 1 for s in b)

def empty_square(b):
    def size(s): return len(b[s])
    return min((s for s in squares if size(s) > 1), key=size)

def possible_digits(b, s):
    return b[s]

def assign(b, s, d):
    new_board = [ s.copy() for s in b ]
    return new_board if set_digit(new_board, s, d) else None

# Note, this mutates the passed in board because eliminate does.
def set_digit(b, s, d):
    return all(eliminate_digit(b, s, d2) for d2 in b[s] - {d})

# Note, this mutates the passed in board.
def eliminate_digit(b, s, d):
    if d in b[s]:
        b[s].remove(d) # The mutation
        if not propagate_assignment(b, s): return False
        if not propagate_to_unit(b, s, d): return False
    return True

def propagate_assignment(b, s):
    # If s is down to one choice, eliminate from peers.
    if len(b[s]) == 1:
        d2 = list(b[s])[0]
        for p in peers[s]:
            if not eliminate_digit(b, p, d2): return False
    return True

def propagate_to_unit(b, s, d):
    # Now see if it's apparent where d must go if not in s.
    for u in units[s]:
        places = [ s2 for s2 in u if d in b[s2] ]
        if len(places) == 0:
            # Ooops, we just eliminated the last possible place.
            return False
        elif len(places) == 1:
            if not set_digit(b, places[0], d): return False
    return True

def solve(givens):
    b = search(board(givens))
    if b is not None:
        return [ None if len(b[s]) > 1 else list(b[s])[0] for s in squares ]
    else:
        return None

def board(givens):
    b = [ set(digits) for _ in squares ]
    for s, d in enumerate(givens):
        if d and not set_digit(b, s, d): return None
    return b

main(solve)
