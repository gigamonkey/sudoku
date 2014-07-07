#!/usr/bin/env python3

#
# Loosely based on code from Peter Norvig's "Solving Every Sudoku Puzzle" (http://norvig.com/sudoku.html)
#

digits  = set('123456789')
squares = range(81)

# If we use a 81-element list as our board, these give us lists of
# lists of indices of various groupings of squares.
rows  = [ [ r*9 + c for c in range(9) ] for r in range(9) ]
cols  = [ [ r*9 + c for r in range(9) ] for c in range(9) ]
boxes = [ [ r*9 + c for r in range(x, x+3) for c in range(y, y+3) ]
          for x in range(0, 9, 3) for y in range(0, 9, 3) ]
units = [ [ u for u in (rows + cols + boxes) if s in u ]
          for s in squares ]
peers = [ set(sum(units[s], [])) - {s} for s in squares ]

########################################################################
# Parsing and display

#
# Make a board out a textual representation. The text can be anything
# as long as there are exactly 81 characters that are either digits or
# '.'. All other characters are ignored.
#

def is_square_char(c): return c in digits or c == '.'

def given(c): return c if c in digits else None

def givens(text):
    return [ given(c) for c in text if is_square_char(c) ]

def board(text):
    b = [ set(digits) for _ in squares ]
    for s, d in enumerate(givens(text)):
        if d and not set_digit(b, s, d): return None
    return b

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

#
# Helpers for printing a board.
#

divider = '\n------+-------+------\n'

def sq(x):
    return '.' if x is None or len(x) > 1 else list(x)[0]

def row_chunk(b, r, c): return (sq(b[s]) for s in rows[r][c:c+3])

def row(b, r):
    return ' | '.join(' '.join(row_chunk(b, r, c)) for c in (0, 3, 6))

def band(b, i):
    return '\n'.join(row(b, r) for r in range(i * 3, (i+1) * 3))

#
# Return a string representation of the board as a grid.
#
def grid(b):
    return divider.join(band(b, i) for i in range(3))

#
# Return a single line representation of the board.
#
def oneline(b): return ''.join(sq(x) for x in b)

#
# Given a board with some squares filled in, return a board completely
# filled in or None if there is no solution.
#
def solve(b):
    if b is None or solved(b): return b

    s = empty_square(b)
    for d in possible_digits(b, s):
        solution = solve(assign(b, s, d))
        if solution: return solution

    return None

def solved(b): return all(len(s) == 1 for s in b)

def empty_square(b):
    def size(s): return len(b[s])
    return min((s for s in squares if size(s) > 1), key=size)

def possible_digits(b, s): return b[s]

def assign(b, s, d):
    new_board = [ s.copy() for s in b ]
    return new_board if set_digit(new_board, s, d) else None

if __name__ == '__main__':

    def side_by_side(g1, g2, space=10):
        for l1, l2 in zip(g1.split('\n'), g2.split('\n')):
            print(l1 + (' ' * space) + l2)

    import fileinput
    puzzle = ''.join(fileinput.input())
    side_by_side(grid(givens(puzzle)), grid(solve(board(puzzle))))

    exit()

    easy          = '.5...1479..27....8....462...46..9537....6....8935..64...961....1....23..3274...1.'
    easy_solution = '658231479432795168971846253246189537715364892893527641589613724164972385327458916'

    hard          = '85...24..72......9..4.........1.7..23.5...9...4...........8..7..17..........36.4.'
    hard_solution = '859612437723854169164379528986147352375268914241593786432981675617425893598736241'


    b = board(easy)

    # Some test cases.
    assert solve(None) == None
    assert b == board(grid(b))
    assert b == board(oneline(b))
    # assert(easy == oneline(b)) # Not true any more since just loading the puzzle may partically (or completely) solve it.
    assert easy == oneline(givens(easy))

    def check(puzzle, solution):
        print(grid(givens(puzzle)))
        print()
        s = solve(board(puzzle))
        assert s == board(solution)
        print(grid(s))
        print()
        print(oneline(givens(puzzle)))
        print(oneline(s))
        print()

    check(easy, easy_solution)
    check(hard, hard_solution)
