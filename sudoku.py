#!/usr/bin/env python3

digits = set('123456789')

# If we use a 81-element list as our board, these give us lists of
# lists of indices of various groupings of squares.
rows  = [ list(range(r*9, (r+1)*9)) for r in range(9) ]
cols  = [ list(range(c, 81, 9)) for c in range(9) ]
boxes = [ [ r*9 + c for r in range(x, x+3) for c in range(y, y+3) ] for x in (0, 3, 6) for y in (0, 3, 6) ]

########################################################################
# Parsing and display

#
# Make a board out a textual representation. The text can be anything
# as long as there are exactly 81 characters that are either digits or
# '.'. All other characters are ignored.
#
def board(text):
    return [ None if c == '.' else c for c in text if c in digits or c == '.' ]

#
# Return a string representation of the board as a grid.
#
def grid(board):
    divider = '\n' + ('-+-'.join(['-' * 5] * 3)) + '\n'
    def sq(i): return b[i] if b[i] in digits else '.'
    def row(r): return ' | '.join([ ' '.join(sq(s) for s in rows[r][c:c+3]) for c in (0, 3, 6) ])
    def band(i): return '\n'.join(row(r) for r in range(i*3, (i+1)*3))
    return divider.join(band(i) for i in range(3))

#
# Return a single line representation of the board.
#
def oneline(board): return ''.join(c if c in digits else '.' for c in b)

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

if __name__ == '__main__':

    text = '9.........5.............................................................4.......1'

    b = board(text)

    # Some test cases.
    assert(b == board(grid(b)))
    assert(b == board(oneline(b)))
    assert(text == oneline(b))

    print(grid(b))
