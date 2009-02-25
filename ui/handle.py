# -*- coding: utf-8 -*-

"""
    handle
    ~~~~~~

    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""

from pyglet.gl import *
from pyglet.event import EventDispatcher
from pyglet.window import mouse

from .base import Active, Point, Rect
from .box import Box

class Handle(Active, EventDispatcher):
    def __init__(self, start=None, size=None, bbox=None):
        Active.__init__(self)
        self.bbox = bbox or Rect()
        self.pos = start or Point()
        self.dim = size or Point(10, 10)

        self.dragging = False
        self.box = Box([0.3, 0.3, 0.3, 1.0], 4)

    def layout(self):
        self.box.dim = self.dim
        self.box.layout()

    def do_draw(self):
        self.box.draw()
    
    def on_press(self, abs, rel):
        if rel in self:
            self.window.set_mouse_visible(False)
            self.dragging = True
            self.on_enter()
    
    def on_release(self, abs, rel):
        if self.dragging:
            abs = self.window_pos
            pos = abs + self.dim/2
            self.window.set_mouse_position(int(pos.x), int(pos.y))
            self.window.set_mouse_visible(True)
            self.dragging = False
            self.on_enter()

    def update(self, pos):
        self.pos = self.bbox.pos + self.bbox.dim * pos
    
    def on_drag(self, delta):
        if self.dragging:
            self.pos += delta
            self.pos %= self.bbox

            pos = self.pos - self.bbox.pos
            if self.bbox.dim.x:
                pos.x /= float(self.bbox.dim.x)
            if self.bbox.dim.y:
                pos.y /= float(self.bbox.dim.y)
            self.dispatch_event('on_handle_move', pos)
            return True

Handle.register_event_type('on_handle_move')
