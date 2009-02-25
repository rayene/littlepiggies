# -*- coding: utf-8 -*-

"""
    Element
    ~~~~~~~

    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""

from pyglet.gl import *
import ctypes
import math

class Point(object):
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __div__(self, val):
        if isinstance(val, Point):
            return Point(self.x / val.x, self.y / val.y)
        else:
            return Point(self.x / val, self.y / val)

    def __mul__(self, val):
        if isinstance(val, Point):
            return Point(self.x * val.x, self.y * val.y)
        else:
            return Point(self.x * val, self.y * val)

    def __repr__(self):
        return 'Point(%s, %s)' % (self.x, self.y)

    def __imod__(self, rect):
        if self.x < rect.x:
            self.x = rect.x
        elif self.x > rect.x2:
            self.x = rect.x2
        if self.y < rect.y:
            self.y = rect.y
        elif self.y > rect.y2:
            self.y = rect.y2
        return self

    def get_x(self):
        return self._x
    def set_x(self, value):
        self._x = float(value)
    x = property(get_x, set_x)
    
    def get_y(self):
        return self._y
    def set_y(self, value):
        self._y = float(value)
    y = property(get_y, set_y)

    def __len__(self):
        return math.sqrt((self.x ** 2) + (self.y ** 2))

class Rect(object):
    def __init__(self, x=0, y=0, width=0, height=0):
        self.pos = Point(x, y)
        self.dim = Point(width, height)
        
    def get_x(self):
        return self.pos.x
    def set_x(self, value):
        self.pos.x = value
    x = property(get_x, set_x)

    def get_y(self):
        return self.pos.y
    def set_y(self, value):
        self.pos.y = value
    y = property(get_y, set_y)

    @property
    def x2(self):
        return self.pos.x + self.dim.x

    @property
    def y2(self):
        return self.pos.y + self.dim.y

    def get_width(self):
        return self.dim.x
    def set_width(self, value):
        self.dim.x = value
    width = property(get_width, set_width)
    
    def get_height(self):
        return self.dim.y
    def set_height(self, value):
        self.dim.y = value
    height = property(get_height, set_height)

    def __contains__(self, point):
        if point.x > self.x and point.y > self.y:
            if point.x < self.x2 and point.y < self.y2:
                return True
        return False

class Element(Rect):
    parent = None
    _window = None
    def __init__(self):
        Rect.__init__(self)
        self._children = []
    
    def __repr__(self):
        return '<%s %i %s>' % (self.__class__.__name__, id(self), ', '.join(repr(child) for child in self.children))

    def layout(self):
        pass

    def get_children(self):
        return self._children
    def set_children(self, children):
        for child in self._children:
            child._on_remove()
        self._children = children
        for child in children:
            child.parent = self

    children = property(get_children, set_children)

    def get_window(self):
        return self._window or self.parent.window

    def set_window(self, window):
        self._window = window

    window = property(get_window, set_window)

    def do_draw(self):
        for child in self.children:
            child.draw()

    @property
    def window_pos(self):
        return self.parent.window_pos + self.pos
    
    @property
    def viewport_pos(self):
        return self.parent.viewport_pos + self.pos

    def draw(self):
        glPushMatrix()
        if self.parent is not None:
            glTranslatef(self.x, self.y, 0)
            self.do_draw()
        else:
            glTranslatef(self.x, self.y, 0)
            self.do_draw()
        glPopMatrix()

    def _layout(self):
        self.layout()
        if self.parent:
            self.parent._layout()

    def _on_press(self, abs, rel):
        if rel in self:
            new_rel = rel - self.pos
            for child in self.children:
                if child._on_press(abs, new_rel):
                    return True
            return self.on_press(abs, rel)

    def on_press(self, abs, rel):
        pass

    def on_mouse_scroll(self, pos, delta):
        if pos in self:
            rel = pos - self.pos
            for child in self.children:
                child.on_mouse_scroll(rel, delta)
    
    def on_release(self, abs, rel):
        rel = rel - self.pos
        for child in self.children:
            child.on_release(abs, rel)

    def on_drag(self, delta):
        for child in self.children:
            if child.on_drag(delta):
                return True

    def on_motion(self, p2, delta):
        p1 = p2 - delta
        in1 = p1 in self
        in2 = p2 in self

        if in1 or in2:
            p2 = p2 - self.pos
            for child in self.children:
                child.on_motion(p2, delta)
            if in1 != in2:
                if in2:
                    self.on_enter()
                else:
                    self.on_leave()

    def on_enter(self):
        pass

    def on_leave(self):
        pass

    def on_key_press(self, symbol, modifiers):
        for child in self.children:
            if child.on_key_press(symbol, modifiers):
                return True

    def on_remove(self):
        pass

    def _on_remove(self):
        for child in self.children:
            child._on_remove()
        self.on_remove() 

class Active(Element):
    hl_color = 0.5, 0.5, 0.5, 1.0
    normal_color = 0.3, 0.3, 0.3, 1.0
    def on_enter(self):
        self.color = self.hl_color
        cursor = self.window.get_system_mouse_cursor(self.window.CURSOR_HAND)
        self.window.set_mouse_cursor(cursor)

    def on_leave(self):
        self.color = self.normal_color
        cursor = self.window.get_system_mouse_cursor(self.window.CURSOR_DEFAULT)
        self.window.set_mouse_cursor(cursor)

    def set_color(self, color):
        self.box.color = color
    color = property(None, set_color)

class Texture(Element):
    fbo = None
    def __init__(self):
        Element.__init__(self)
        self.color = [1.0, 1.0, 1.0, 0.8]
    
    def layout(self): 
        fbo = GLuint()
        glGenFramebuffersEXT(1, ctypes.byref(fbo))
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, fbo)

        self.texture = pyglet.image.Texture.create(int(self.width), int(self.height), GL_RGBA)
        glBindTexture(GL_TEXTURE_2D, self.texture.id)
        glFramebufferTexture2DEXT(GL_FRAMEBUFFER_EXT,
            GL_COLOR_ATTACHMENT0_EXT, GL_TEXTURE_2D, self.texture.id, 0)

        status = glCheckFramebufferStatusEXT(GL_FRAMEBUFFER_EXT)
        assert status == GL_FRAMEBUFFER_COMPLETE_EXT
        
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, 0)

        self.fbo = fbo
    
    def __del__(self):
        if self.fbo:
            glDeleteFramebuffersEXT(1, ctypes.byref(self.fbo)) 
    
    @property
    def viewport_pos(self):
        return Point(0, 0)

    def draw(self):
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, self.fbo)
        for child in self.children:
            child.draw()
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, 0)
        glColor4f(*self.color)
        self.texture.blit(self.x, self.y)
