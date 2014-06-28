#!/usr/bin/env python3

digits = set('123456789')

# If we use a 81-element list as our board, these give us lists of
# lists of indices of various groupings of squares.
rows  = [ list(range(r*9, (r+1)*9)) for r in range(9) ]
cols  = [ list(range(c, 81, 9)) for c in range(9) ]
boxes = [ [ r*9 + c for r in range(x, x+3) for c in range(y, y+3) ] for x in (0, 3, 6) for y in (0, 3, 6) ]
units = rows + cols + boxes
peers = [ set(sum([u for u in units if s in u], [])) - {s} for s in range(81) ]

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
def grid(b):
    divider = '\n' + ('-+-'.join(['-' * 5] * 3)) + '\n'
    def sq(i): return b[i] if b[i] in digits else '.'
    def row(r): return ' | '.join([ ' '.join(sq(s) for s in rows[r][c:c+3]) for c in (0, 3, 6) ])
    def band(i): return '\n'.join(row(r) for r in range(i*3, (i+1)*3))
    return divider.join(band(i) for i in range(3))

#
# Return a single line representation of the board.
#
def oneline(b): return ''.join(c if c in digits else '.' for c in b)

#
# Given a board with some squares filled in, return a board completely
# filled in or None if there is no solution.
#
def solve(b):
    if b:
        s = empty_square(b)
        if s is None:
            return b
        else:
            for d in possible_digits(b, s):
                solution = solve(assign(b, s, d))
                if solution: return solution
    else:
        return None

def empty_square(b):
    try:
        return b.index(None)
    except:
        return None

def possible_digits(b, s):
    return filter(lambda d: legal_digit(b, s, d), digits)

def legal_digit(b, s, d):
    return not any(b[p] == d for p in peers[s])

def assign(b, s, d):
    new_board = b.copy()
    new_board[s] = d
    return new_board if legal(new_board) else None

def legal(b):
    return all(legal_square(b, s) for s in range(81))

def legal_square(b, s):
    return all(b[p] is None or b[s] != b[p] for p in peers[s])

if __name__ == '__main__':

    easy          = '.5...1479..27....8....462...46..9537....6....8935..64...961....1....23..3274...1.'
    easy_solution = '658231479432795168971846253246189537715364892893527641589613724164972385327458916'

    hard          = '85...24..72......9..4.........1.7..23.5...9...4...........8..7..17..........36.4.'
    hard_solution = '859612437723854169164379528986147352375268914241593786432981675617425893598736241'

    b = board(easy)

    # Some test cases.
    assert(b == board(grid(b)))
    assert(b == board(oneline(b)))
    assert(easy == oneline(b))

    def check(puzzle, solution):
        b = board(puzzle)
        print(grid(b))
        print()
        s = solve(b)
        assert(s == board(solution))
        print(grid(s))
        print()
        print(oneline(b))
        print(oneline(s))
        print()

    check(easy, easy_solution)
    check(hard, hard_solution) # Too slow with current code.
