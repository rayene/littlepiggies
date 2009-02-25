# -*- coding: utf-8 -*-

"""
    button
    ~~~~~~

    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""

from pyglet.gl import *
from pyglet.event import EventDispatcher
from pyglet.window import mouse

from .base import Active
from .box import Box
from .text import Text

class Button(Active, EventDispatcher):
    def __init__(self, content, args=[], kwargs={}):
        Active.__init__(self)

        if isinstance(content, (str, unicode)):
            self.content = Text(content)
        else:
            self.content = content

        self.args = args
        self.kwargs = kwargs
        self.width = self.content.width + 10
        self.height = self.content.height + 10
        self.box = Box([0.3, 0.3, 0.3, 1.0], corner_radius=7)
        self.box.width = self.width
        self.box.height = self.height
        self.box.layout()
        self.content.x = (self.width - self.content.width) / 2
        self.content.y = (self.height - self.content.height) / 2
        self.children = self.box, self.content

    def on_press(self, abs, rel):
        if rel in self:
            self.dispatch_event('on_click', *self.args, **self.kwargs)
    
    def __repr__(self):
        return '<Button %i %s>' % (id(self), self.content)

Button.register_event_type('on_click')
