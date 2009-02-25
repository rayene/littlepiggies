# -*- coding: utf-8 -*-

"""
    dialog
    ~~~~~~

    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""

import pyglet
from ui import (Widget, Grid, Text, Column, Checkbox, Button, Element,
                    Texture, Flow, Scrollable, Row, Dial, VDial, Close, Graph)



class Dialog(Texture, pyglet.event.EventDispatcher):
    mapping_width = 400
    def __init__(self, window):
        Texture.__init__(self)
        pyglet.event.EventDispatcher.__init__(self)
        self.window = window
        self.dragging = False
        self.grid = grid = Grid(cols={1:self.mapping_width}, rows=40)
        
        
        text1 = Text('Hi')
        text2 = Text('World')
        checkbox = Checkbox('Toggle', 'non')
        
        g = Graph(100, 100, 0, 0)
        
        dial = Dial(100, '30%')
        dial.value = 0.30
        vdial = VDial(100)
        vdial.value = 0.30
        r1 = Row([text1, text2, checkbox, dial, g, vdial])

        self.col = Column()
        self.col.append(r1)
        for i in range(3):
            for j in range(3):
                pass
                self.grid[i,j] = Button('Grid Button'+str(i+j))
        r2 = Row([self.grid])
        self.col.append(r2)
        self.col.x = 20
        self.col.width = 400
        self.col.height = 300
        self.scrollable = Scrollable(self.col, 300)
        self.scrollable = Column()
        self.widget = Widget('My Dialog', self.scrollable)
        close = Close()
        close.x = self.widget.width - close.width - 15
        close.y = self.widget.height - close.height - 15
        close.on_click = self.on_close
        
        self.children = [self.widget, close]#, self.resizer]
        
        self.width = self.widget.width
        self.height = self.widget.height
        self._layout()

    def on_press(self, abs, rel):
        if rel in self:
            self.dragging = True

    def on_release(self, abs, rel):
        if self.dragging:
            abs = self.window_pos
            pos = abs + self.dim/2
            self.window.set_mouse_position(int(pos.x), int(pos.y))
            self.window.set_mouse_visible(True)
            self.dragging = False
            self.on_enter()
        self.widget.on_release(abs, rel)
            
    def on_drag(self, delta):
        if not self.widget.on_drag(delta) and self.dragging:
            self.pos += delta
            return True
    
    def resize(self, delta):
        self.widget.width += delta.x
        self.widget.height += delta.y
        self.scrollable.layout
        self._layout()

    def write_something(self):
        print 'Something'
        
    def on_close(self):
        self.write_something()
        self.dispatch_event('on_widget_close', self)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            self.on_close()
            return True

Dialog.register_event_type('on_widget_open')
Dialog.register_event_type('on_widget_close')
