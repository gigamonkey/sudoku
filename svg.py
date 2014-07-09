#!/usr/bin/env python3

from sys import argv

padding = 10
size = 40

def coord(n): return padding + (n * size) + .5

print("""<?xml version="1.0"?>
<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg">
 <g>
  <title>Sudoku</title>
""".format((padding * 2) + (size * 9), (padding * 2) + (size * 9)))

rect = """  <rect height="{}" width="{}" y="{}" x="{}" stroke-width=".5" stroke="#777" fill="#fff"/>"""
bigrect = """  <rect height="{}" width="{}" y="{}" x="{}" stroke-width="3" stroke="#777" fill="#fff" fill-opacity="0.0"/>"""
text = """  <text font-family="sans-serif" fill="#333" text-anchor="middle" x="{}" y="{}">{}</text>"""

for y in range(9):
    for x in range(9):
        print(rect.format(size, size, coord(y), coord(x)))

for y in range(3):
    for x in range(3):
        print(bigrect.format(size * 3, size * 3, coord(y * 3), coord(x * 3)))

if argv[1] == "blank":
    pass
elif argv[1] == "numbers":
    for r in range(9):
        for c in range(9):
            print(text.format(coord(c) + size/2, coord(r) + size*.6, (r*9 + c)))
elif argv[1] == "pairs":
    for r in range(9):
        for c in range(9):
            print(text.format(coord(c) + size/2, coord(r) + size*.6, "{}, {}".format(r, c)))
elif argv[1] == "labels":
    letters = 'abcdefghi'
    for r in range(9):
        for c in range(9):
            print(text.format(coord(c) + size/2, coord(r) + size*.6, "{}{}".format(letters[r], c+1)))
else:
    from sudoku import givens
    with open(argv[1] + ".txt") as f:
        for i, g in enumerate(givens(f.read())):
            if g is not None:
               print(text.format(coord(i % 9) + size/2, coord(i // 9) + size * .6, g))



print(""" </g>
</svg>
""")
