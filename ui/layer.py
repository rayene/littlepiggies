# -*- coding: utf-8 -*-

"""
    Layer
    ~~~~~

    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""

from .base import Point

class Layer(object):
    def __init__(self, window):
        self.enabled = False
        self.x = 0
        self.y = 0
        self.width = window.width
        self.height = window.height
        self.window = window
        self.children = []
        self.window_pos = Point(0, 0)
        self.viewport_pos = Point(0, 0)
        window.push_handlers(on_resize=self.on_resize)

    def draw(self):
        if self.enabled:
            for child in self.children:
                child.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        abs = Point(x, y)
        rel = Point(x, y)
        if self.children:
            return self.children[-1]._on_press(abs, rel)
    
    def on_mouse_release(self, x, y, button, modifiers):
        abs = Point(x, y)
        rel = Point(x, y)
        if self.children:
            return self.children[-1].on_release(abs, rel)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        delta = Point(dx, dy)
        if self.children:
            return self.children[-1].on_drag(delta)
    
    def on_mouse_motion(self, x, y, dx, dy):
        p2 = Point(x, y)
        delta = Point(dx, dy)
        if self.children:
            return self.children[-1].on_motion(p2, delta)

    def on_mouse_scroll(self, x, y, dx, dy):
        point = Point(x, y)
        delta = Point(dx, dy)
        if self.children:
            return self.children[-1].on_mouse_scroll(point, delta)

    def on_key_press(self, symbol, modifiers):
        if self.children:
            return self.children[-1].on_key_press(symbol, modifiers)

    def add(self, child):
        child.push_handlers(self)
        self.children.append(child)
        child.parent = self
        child.x = (self.window.width - child.width) / 2
        child.y = (self.window.height - child.height) / 2
        self.adjust_colors()
        return child

    def on_widget_open(self, widget):
        self.add(widget)

    def on_widget_close(self, widget):
        self.remove(widget)

    def remove(self, child):
        child.remove_handlers(self)
        self.children.remove(child)
        self.adjust_colors()

    def adjust_colors(self):
        for child in self.children[:-1]:
            child.color = [0.5, 0.5, 0.5, 0.3]

        if self.children:
            self.children[-1].color = [1.0, 1.0, 1.0, 1.0]

    def on_resize(self, width, height):
        self.width = width
        self.height = height
        self._layout()

    def _layout(self):
        for child in self.children:
            child.x = (self.width - child.width) / 2
            child.y = (self.height - child.height) / 2

    def enable(self):
        if not self.enabled:
            self.enabled = True
            self.window.push_handlers(self)

    def disable(self):
        if self.enabled:
            self.enabled = False
            self.window.remove_handlers(self)
