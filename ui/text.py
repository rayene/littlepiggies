# -*- coding: utf-8 -*-

"""
    text
    ~~~~

    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""

import pyglet
from pyglet.gl import *
from base import Element

class Text(Element):
    def __init__(self, text='', **kwargs):
        Element.__init__(self)
        self.kwargs = kwargs
        self.set_text(text)

    def set_text(self, text, **kwargs):
        self.text = text
        self.kwargs.update(kwargs)
        kwargs = self.kwargs
        if 'anchor_y' not in kwargs:
            kwargs['anchor_y'] = 'bottom'
        if 'width' in kwargs:
            kwargs['multiline'] = True
        self.label = pyglet.text.Label(text, **kwargs)
        self.width = kwargs.get('width') or self.label.content_width
        self.height = self.label.content_height

    def do_draw(self):
        self.label.draw()

    def __repr__(self):
        return '<Text %i %s>' % (id(self), self.text)
       
