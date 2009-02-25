# -*- coding: utf-8 -*-

from pyglet.gl import *
from pyglet.event import EventDispatcher
from pyglet.window import mouse

from .base import Active
from .util import Loader

loader = Loader(__file__, 'res')

class Resizer(Active, EventDispatcher):
    img = loader.image('resize.png')
    hl_color = 0.7, 0.7, 0.7, 1.0
    normal_color = 1.0, 1.0, 1.0, 1.0

    def __init__(self, dialog):
        Active.__init__(self)
        self.dialog = dialog
        self.width = self.img.width
        self.height = self.img.height
        self._color = [1.0, 1.0, 1.0, 1.0]
        self.dragging = False

    def on_press(self, abs, rel):
        if rel in self:
            self.dragging = True
            
            #self.dispatch_event('on_click')
            return True
    def on_release(self, abs, rel):
        self.dragging = False
        return True
    
    def on_drag(self, delta):
        print 'dragging'
        if self.dragging:
            self.dialog.resize(delta)
            return True

    def do_draw(self):
        glColor4f(*self._color)
        self.img.blit(0,0)

    def set_color(self, color):
        self._color = color
    color = property(None, set_color)

Resizer.register_event_type('on_resize2')
