# -*- coding: utf-8 -*-

"""
    checkbox
    ~~~~~~~~

    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""

from pyglet.gl import *
from pyglet.event import EventDispatcher
from pyglet.window import mouse

from .base import Active
from .box import Box
from .text import Text

class Checkbox(Active, EventDispatcher):
    def __init__(self, on, off, checked=False):
        Active.__init__(self)
        self.checked = checked

        if isinstance(on, (str, unicode)):
            on = Text(on)
        self.on = on
        
        if isinstance(off, (str, unicode)):
            off = Text(off)
        self.off = off

        width = max(self.on.width, self.off.width)
        height = max(self.on.height, self.off.height)
        self.width = width + 10
        self.height = height + 10
        on.x = (self.width - on.width) / 2
        on.y = (self.height - on.height) / 2
        off.x = (self.width - off.width) / 2
        off.y = (self.height - off.height) / 2
        
        self.box = Box([0.3, 0.3, 0.3, 1.0], corner_radius=7)
        self.box.width = self.width
        self.box.height = self.height
        self.box.layout()
       
        if self.checked:
            self.children = self.box, self.on
        else:
            self.children = self.box, self.off

    def __nonzero__(self):
        return self.checked

    def on_press(self, abs, rel):
        if rel in self:
            if self.checked:
                self.checked = False
                self.children = self.box, self.off
            else:
                self.checked = True
                self.children = self.box, self.on
            self.dispatch_event('on_change', self.checked)
    
    def __repr__(self):
        return '<Checkbox %i %s>' % (id(self), self.content)

Checkbox.register_event_type('on_change')
