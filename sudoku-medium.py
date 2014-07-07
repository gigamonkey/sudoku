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

def board(text):
    return [ given(c) for c in text if is_square_char(c) ]

#
# Helpers for printing a board.
#

divider = '\n------+-------+------\n'

def sq(x): return x if x is not None else '.'

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

def solved(b): return not any(s is None for s in b)

def empty_square(b):
    try:
        return b.index(None)
    except:
        return None

def possible_digits(b, s):
    return [ d for d in digits if legal_digit(b, s, d) ]

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

if __name__ == '__main__':

    def side_by_side(g1, g2, space=10):
        for l1, l2 in zip(g1.split('\n'), g2.split('\n')):
            print(l1 + (' ' * space) + l2)

    import fileinput
    puzzle = ''.join(fileinput.input())
    side_by_side(grid(board(puzzle)), grid(solve(board(puzzle))))
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
    assert easy == oneline(b)

    def check(puzzle, solution):
        print(grid(board(puzzle)))
        print()
        s = solve(board(puzzle))
        assert s == board(solution)
        print(grid(s))
        print()
        print(oneline(board(puzzle)))
        print(oneline(s))
        print()

    check(easy, easy_solution)
    #check(hard, hard_solution) # Too slow with current code.
