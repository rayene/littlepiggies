# -*- coding: utf-8 -*-

"""
    widget
    ~~~~~~

    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""

from .base import Element
from .box import Box
from .outline import Outline
from .text import Text
import pyglet
from pyglet.event import EventDispatcher

class Widget(Element, EventDispatcher):
    _content = None
    def __init__(self, title, content):
        Element.__init__(self)
        self.label = Text(title,
            font_size   = 18,
            bold        = True,
            anchor_y    = 'top',
            color       = (150, 150, 150, 255),
            width       = content.width - 25,
        )
        self.box = Box((0.1, 0.1, 0.1, 0.8))
        
        self.dragging = False

        self.content = content
        self.children = self.box, self.label, self.content
        self._layout()

    def layout(self):
        content = self.content
        self.content.x = 15
        self.content.y = 10
        content_width = content.width
        content_height = content.height

        self.width = width = max(self.label.width, content_width) + 30
        self.height = height = self.label.height + content_height + 30
        self.label.y = height - 10
        self.label.x = 15
        
        self.box.width = width
        self.box.height = height
        self.box.layout()
            
Widget.register_event_type('on_widget_close')
