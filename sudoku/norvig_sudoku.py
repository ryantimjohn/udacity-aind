from utils import display, peers

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    return [i+j for i in a for j in b]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(r, c) for r in ('ABC', 'DEF', 'GHI')
                            for c in ('123', '456', '789')]

unitlist = row_units + column_units + square_units

def grid_values(grid):
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))

grid = grid_values('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..')


def eliminate(values):
    for k,v in values.items():
        if len(v) == 1:
            for peer in peers[k]:
                values[peer] = values[peer].replace(v,"")

eliminate(grid)

display(grid)
