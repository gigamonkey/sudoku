#!/usr/bin/env python3

#
# Make a board out a textual representation. The text can be anything
# as long as there are exactly 81 characters that are either digits or
# '.'. All other characters are ignored.
#
def givens(text):
    return [ given(c) for c in text if is_square_char(c) ]

def grid(b):
    return divider.join(band(b, i) for i in range(3))

def oneline(b): return ''.join(sq(x) for x in b)

def side_by_side(b1, b2, space=10):
    for l1, l2 in zip(grid(b1).split('\n'), grid(b2).split('\n')):
        print(l1 + (' ' * space) + l2)

########################################################################
# Private methods

digits  = set('123456789')
rows    = [ [ r*9 + c for c in range(9) ] for r in range(9) ]
divider = '\n------+-------+------\n'

def is_square_char(c): return c in digits or c == '.'

def given(c): return c if c in digits else None


def sq(x): return '.' if x is None else x

def row_chunk(b, r, c): return (sq(b[s]) for s in rows[r][c:c+3])

def row(b, r):
    return ' | '.join(' '.join(row_chunk(b, r, c)) for c in (0, 3, 6))

def band(b, i):
    return '\n'.join(row(b, r) for r in range(i * 3, (i+1) * 3))


def main(board, solve, to_list):
    import fileinput
    puzzle = givens(''.join(fileinput.input()))
    side_by_side(to_list(board(puzzle)), to_list(solve(board(puzzle))))
