# -*- coding: utf-8 -*-

"""
    Container
    ~~~~~~~~~

    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""

from .base import Element

class Container(Element):
    def __init__(self, width, height):
        Element.__init__(self)
        self.width = width
        self.height = height

    def layout(self):
        self._content.y = self.height - self._content.height
        self._content.x = (self.width - self._content.width) / 2

    def set_content(self, content):
        self._content = content
        if content:
            self.children = [content]
            self.layout()
        else:
            self.children = []
    content = property(None, set_content)
