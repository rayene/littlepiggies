# -*- coding: utf-8 -*-

"""
    Flow
    ~~~~

    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""

from .base import Element

class Flow(Element):
    def __init__(self, width, children=[], spacing=10):
        Element.__init__(self)
        self.spacing = spacing
        self.children = list(children)
        self.width = width
        self._layout()

    def layout(self):
        x = 0
        y = 0
        height = 0
        for child in self.children:
            if x + self.spacing + child.width > self.width:
                y += height + self.spacing
                x = 0
            height = max(height, child.height)
            child.x = x
            child.y = y
            x += child.width + self.spacing
        
        self.height = y + height
        for child in self.children:
            child.y = self.height - child.y - child.height

    def append(self, child):
        child.parent = self
        self.children.append(child)
        self._layout()
        return child

    def remove(self, child):
        index = self.children.index(child)
        self.children.remove(child)
        child.on_remove()
        self._layout()
        return index

    def insert(self, index, child):
        child.parent = self
        self.children.insert(index, child)
        self._layout()
        return child

    def __len__(self):
        return len(self.children)
