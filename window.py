# -*- coding: utf-8 -*-

"""
    window
    ~~~~~~

    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""

import pyglet
from pyglet.gl import *

class Window(pyglet.window.Window):
    def __init__(self, app):
        pyglet.window.Window.__init__(self, 800, 600, resizable=True, vsync=False)
        self.app = app

        glEnable(GL_ALPHA_TEST)
        glEnable(GL_CULL_FACE)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_POLYGON_SMOOTH)
        glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glClearColor(0.5, 0.5, 0.5, 0)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60., width / float(height), .1, 1000.)
        return pyglet.event.EVENT_HANDLED

    def draw_gui(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0.0, 1.0 * self.width, 0.0, 1.0 * self.height)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)
        self.app.draw()
        
    def set_mouse_position(self, x, y):
        pass
    def on_draw(self):
        self.clear()
        self.draw_gui()

