# -*- coding: utf-8 -*-

"""
    row
    ~~~

    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""

from .base import Element

class Row(Element):
    def __init__(self, rows, spacing=10):
        Element.__init__(self)
        self.spacing = spacing
        self.children = rows
        self._layout()

    def layout(self):
        xoff = 0
        height = 0
        for child in self.children:
            child.x = xoff
            xoff += child.width + self.spacing
            height = max(child.height, height)

        for child in self.children:
            child.y = (height - child.height) / 2

        self.width = xoff - self.spacing
        self.height = height

    def append(self, child):
        child.parent = self
        self.children.append(child)
        self._layout()
        return child
