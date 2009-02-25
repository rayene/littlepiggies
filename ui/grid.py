# -*- coding: utf-8 -*-

"""
    grid
    ~~~~

    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""

from .base import Element

class Grid(Element):
    def __init__(self, spacing=10, rows=None, cols=None):
        Element.__init__(self)
        self.rows = dict()
        self.spacing = spacing
        self.style = dict(rows=rows, cols=cols)
        self.row_index = set()
        self.col_index = set()

    def __setitem__(self, (col, row), child):
        self.row_index.add(row)
        self.col_index.add(col)
        row = self.rows.setdefault(row, dict())
        row[col] = child
        self._layout()

    def defaults(self):
        widths = dict()
        heights = dict()
        rows = self.style['rows']
        if isinstance(rows, int):
            for row_index in self.row_index:
                heights[row_index] = rows
        elif isinstance(rows, dict):
            for row_index, height in rows.items():
                heights[row_index] = height

        cols = self.style['cols']
        if isinstance(cols, int):
            for col_index in self.col_index:
                widths[col_index] = cols
        elif isinstance(cols, dict):
            for col_index, width in cols.items():
                widths[col_index] = width
        return widths, heights

    def layout(self):
        children = list()
        widths, heights = self.defaults()
        for row_index, row in reversed(sorted(self.rows.items())):
            for col_index, cell in sorted(row.items()):
                width = widths.get(col_index, 0)
                widths[col_index] = max(cell.width, width)
                height = heights.get(row_index, 0)
                heights[row_index] = max(cell.height, height)
                children.append(cell)

        yoff = 0
        for row_index, row in reversed(sorted(self.rows.items())):
            row_height = heights[row_index]
            for col_index, cell in sorted(row.items()):
                xoff = 0
                for width in widths.values()[:col_index]:
                    xoff += width + self.spacing
                cell.x = xoff
                cell.y = yoff + (row_height - cell.height) / 2
            yoff += row_height + self.spacing

        self.width = sum(widths.values()) + (len(widths)-1) * self.spacing
        self.height = sum(heights.values()) + (len(heights)-1) * self.spacing
        self.children = children
