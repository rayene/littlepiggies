# -*- coding: utf-8 -*-

"""
    scrollable
    ~~~~~~

    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""

from pyglet.gl import *
from .base import Element, Point
from .handle import Handle

class Scrollable(Element):
    def __init__(self, content, height):
        Element.__init__(self)
        self.handle = Handle()
        self.handle.push_handlers(self)
        self.height = height
        self.content = content
        self.children = self.handle, self.content
        self._layout()

    def layout(self):
        self.width = self.content.width + 15
        self.handle.bbox.x = self.width-10
        self.handle.x = self.width-10
        if self.content.height > self.height:
            self.children = self.handle, self.content
            self.room = self.content.height - self.height
            self.content.y = -self.room
            relation = float(self.height)/float(self.content.height)
            handle_height = relation * self.height
            handle_height = max(10, handle_height)
            handle_height = min(self.height, handle_height)

            self.handle.y = self.height - handle_height
            self.handle.bbox.height = self.height - handle_height
            self.handle.height = handle_height
        else:
            self.content.y = self.height - self.content.height
            self.children = [self.content]
            self.handle.y = 0
            self.handle.bbox.height = 0
            self.handle.height = self.height
        self.handle.layout()

    def on_handle_move(self, pos):
        offset = self.room * pos.y 
        self.content.y = -offset

    def on_mouse_scroll(self, pos, delta):
        if pos in self:
            if self.content.height > self.height:
                new_y = self.content.y - delta.y * 10

                if new_y > 0:
                    new_y = 0
                elif new_y < -self.room:
                    new_y = -self.room

                delta_y = self.content.y - new_y
                self.content.y = new_y

                point_delta = Point(0, delta_y)
                
                rel = pos - self.pos
                self.on_motion(rel, point_delta)
                
                if self.content.y > 0:
                    self.content.y = 0
                elif self.content.y < -self.room:
                    self.content.y = -self.room
                value = float(self.content.y) / float(self.room)
                self.handle.update(Point(0, -value))

    def do_draw(self):
        abs = self.viewport_pos
        self.handle.draw()
        glEnable(GL_SCISSOR_TEST)
        glScissor(int(abs.x), int(abs.y), int(self.width-15), int(self.height)) 
        self.content.draw()
        glDisable(GL_SCISSOR_TEST)
