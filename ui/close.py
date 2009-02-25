# -*- coding: utf-8 -*-

"""
    close
    ~~~~~

    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""

from pyglet.gl import *
from pyglet.event import EventDispatcher
from pyglet.window import mouse

from .base import Active
from .util import Loader

loader = Loader(__file__, 'res')

class Close(Active, EventDispatcher):
    img = loader.image('close.png')
    hl_color = 0.7, 0.7, 0.7, 1.0
    normal_color = 1.0, 1.0, 1.0, 1.0

    def __init__(self):
        Active.__init__(self)

        self.width = self.img.width
        self.height = self.img.height
        self._color = [1.0, 1.0, 1.0, 1.0]

    def on_press(self, abs, rel):
        if rel in self:
            self.dispatch_event('on_click')
            return True

    def do_draw(self):
        glColor4f(*self._color)
        self.img.blit(0,0)

    def set_color(self, color):
        self._color = color
    color = property(None, set_color)

Close.register_event_type('on_click')
