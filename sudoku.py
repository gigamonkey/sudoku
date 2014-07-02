#!/usr/bin/env python3

#
# Loosely based on code from Peter Norvig's "Solving Every Sudoku Puzzle" (http://norvig.com/sudoku.html)
#

digits = set('123456789')

# If we use a 81-element list as our board, these give us lists of
# lists of indices of various groupings of squares.
rows  = [ list(range(r*9, (r+1)*9)) for r in range(9) ]
cols  = [ list(range(c, 81, 9)) for c in range(9) ]
boxes = [ [ r*9 + c for r in range(x, x+3) for c in range(y, y+3) ] for x in (0, 3, 6) for y in (0, 3, 6) ]
units = [ [ u for u in (rows + cols + boxes) if s in u ] for s in range(81) ]
peers = [ set(sum(units[s], [])) - {s} for s in range(81) ]

########################################################################
# Parsing and display

#
# Make a board out a textual representation. The text can be anything
# as long as there are exactly 81 characters that are either digits or
# '.'. All other characters are ignored.
#
def board(text):
    b = [ set(digits) for _ in range(81) ]
    for s, d in enumerate(givens(text)):
        if d and not set_digit(b, s, d): return None
    return b

def givens(text):
    return [ None if c == '.' else c for c in text if c in digits or c == '.' ]

# Note, this mutates the passed in board because eliminate does.
def set_digit(b, s, d):
    return all(eliminate_digit(b, s, d2) for d2 in b[s] - {d})

# Note, this mutates the passed in board.
def eliminate_digit(b, s, d):
    current = b[s]
    if d not in current:
        return True # Nothing to do
    else:
        current.remove(d)
        if len(current) == 1:
            # d is the only possible digit for this square so remove
            # it from all peers.
            d2 = list(current)[0]
            if not all(eliminate_digit(b, p, d2) for p in peers[s]): return False

        # Now see if it's apparent where d must go if not in s.
        for u in units[s]:
            places = [ s2 for s2 in u if d in b[s2] ]
            if len(places) == 0:
                # Ooops, we just eliminated the last possible place.
                return False
            elif len(places) == 1:
                # Only one place to put it. Eliminate any other digits
                # from that place.
                return set_digit(b, places[0], d)

        return True

#
# Return a string representation of the board or a givens list as a grid.
#
def grid(b):
    divider = '\n' + ('-+-'.join(['-' * 5] * 3)) + '\n'
    def row(r): return ' | '.join([ ' '.join(sq(b[s]) for s in rows[r][c:c+3]) for c in (0, 3, 6) ])
    def band(i): return '\n'.join(row(r) for r in range(i*3, (i+1)*3))
    return divider.join(band(i) for i in range(3))

#
# Return a single line representation of the board or a givens list.
#
def oneline(b): return ''.join(sq(s) for s in b)

#
# Shared implementation of sq for grid and oneline.
#
def sq(s):
    if s is None or len(s) > 1:
        return '.'
    else:
        return list(s)[0]

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

def solved(b): return not any(s for s in b if len(s) > 1)

def empty_square(b):
    p = min((p for p in enumerate(b) if len(p[1]) > 1), key=lambda p: len(p[1]), default=None)
    return p[0] if p else None

def possible_digits(b, s): return b[s]

def assign(b, s, d):
    new_board = [ s.copy() for s in b ]
    return new_board if set_digit(new_board, s, d) else None

if __name__ == '__main__':

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
