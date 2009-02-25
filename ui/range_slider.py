# -*- coding: utf-8 -*-

"""
    RangeSlider
    ~~~~~~~~~~~

    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""

from pyglet.gl import *
from .base import Rect, Point, Element, Active
from .box import Box
from .handle import Handle

class RangeSlider(Element):
    def __init__(self, min, max, width):
        Element.__init__(self)
        self.width = width + 10
        self.height = 25
        self.min = min
        self.max = max
        self.start = Handle(start=Point(0, 15), bbox=Rect(0,15,width,0))
        self.start.layout()
        self.stop = Handle(start=Point(width,0), bbox=Rect(0,0,width,0))
        self.stop.layout()

        self.children = [self.start, self.stop]

    def do_draw(self):
        glColor3f(0.4, 0.4, 0.4)
        glBegin(GL_QUADS)
        glVertex3f(5, 5, 0.0)
        glVertex3f(self.width-5, 5, 0.0)
        glVertex3f(self.width-5, self.height-5, 0.0)
        glVertex3f(5, self.height-5, 0.0)
        glEnd()
        self.start.draw()
        self.stop.draw()
