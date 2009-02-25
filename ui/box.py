# -*- coding: utf-8 -*-

"""
    Box
    ~~~

    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""

from pyglet.gl import *

from .base import Element
from .primitives import box_strip

class Box(Element):
    def __init__(self, color, corner_radius=25):
        Element.__init__(self)
        self.color = color
        self.corner_radius = corner_radius

    def layout(self):
        self.strip = list(box_strip(self.width, self.height, self.corner_radius))

    def draw(self):
        glColor4f(*self.color)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(self.width/2, self.height/2)
        for x, y in self.strip:
            glVertex2f(x, y)
        glEnd()
