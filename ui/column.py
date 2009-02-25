# -*- coding: utf-8 -*-

"""
    Column
    ~~~~~~

    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""

from .base import Element

class Column(Element):
    def __init__(self, rows=[], spacing=10):
        Element.__init__(self)
        self.spacing = spacing
        self.children = rows
        self._layout()

    def layout(self):
        yoff = 0
        width = 0
        for child in reversed(self.children):
            child.y = yoff
            yoff += child.height + self.spacing
            width = max(child.width, width)

        self.height = yoff - self.spacing
        self.width = width

    def append(self, child):
        child.parent = self
        self.children.append(child)
        self._layout()
        return child
