from pyglet.gl import *
from .base import Element
from .text import Text

class Dial(Element):
    def __init__(self, width, label=''):
        Element.__init__(self)
        self.width = width
        self.height = 15
        self.value = 0
        self.label = Text(label, font_size=10, bold=True, color=[0, 0, 0, 178])
        self.label.y = -2
        self.label.x = (width - self.label.width) / 2

    def do_draw(self):
        glColor3f(0.4, 0.4, 0.4)
        glBegin(GL_QUADS)
        glVertex3f(0, 0, 0.0)
        glVertex3f(self.width, 0, 0.0)
        glVertex3f(self.width, self.height, 0.0)
        glVertex3f(0, self.height, 0.0)
        glEnd()
        
        glColor3f(0.8, 0.3, 0.1)
        glBegin(GL_QUADS)
        glVertex3f(0, 0, 0.0)
        glVertex3f(self.width * self.value, 0, 0.0)
        glVertex3f(self.width * self.value, self.height, 0.0)
        glVertex3f(0, self.height, 0.0)
        glEnd()

        self.label.draw()


class VDial(Element):
    def __init__(self, height):
        Element.__init__(self)
        self.width = 15
        self.height = height
        self.value = 0
        
    def do_draw(self):
        glColor3f(0.4, 0.4, 0.4)
        glBegin(GL_QUADS)
        glVertex3f(0, 0, 0.0)
        glVertex3f(self.width, 0, 0.0)
        glVertex3f(self.width, self.height, 0.0)
        glVertex3f(0, self.height, 0.0)
        glEnd()
        
        glColor3f(0.8, 0.3, 0.1)
        glBegin(GL_QUADS)
        glVertex3f(0, 0, 0.0)
        glVertex3f(self.width, 0, 0.0)
        glVertex3f(self.width, self.height*self.value, 0.0)
        glVertex3f(0, self.height*self.value, 0.0)
        glEnd()
