# -*- coding: utf-8 -*-

"""
    Graph
    ~~~~~

    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""

import sys

from pyglet.gl import *
from pyglet.event import EventDispatcher

from .base import Rect, Point, Element, Active
from .box import Box
from .handle import Handle

class Intersection(object):
    def __init__(self, u1, l1, u2, l2):
        self.u1 = u1
        self.l1 = l1
        self.u2 = u2
        self.l2 = l2
        self.p1 = l1.p1 + (l1.p2 - l1.p1) * u1
        self.p2 = l2.p1 + (l2.p2 - l2.p1) * u2

class Line(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def intersect(self, other):
        x1 = self.p1.x
        x2 = self.p2.x
        x3 = other.p1.x
        x4 = other.p2.x
        
        y1 = self.p1.y
        y2 = self.p2.y
        y3 = other.p1.y
        y4 = other.p2.y

        denominator = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)

        if not denominator:
            return False

        u1 = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denominator
        u2 = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denominator

        return Intersection(u1, self, u2, other)

def boundary_intersect(width, height, a, b):
    b *= width

    intersections = []
    p = Point(0, (0*a) + b)
    if p.y <= height and p.y >= 0.0:
        intersections.append(p)
    p = Point(width, (width*a) + b)
    if p.y <= height and p.y >= 0.0:
        intersections.append(p)

    p = Point((0-b) / a, 0)
    if p.x <= width and p.x >= 0.0:
        intersections.append(p)
    p = Point((height-b) / a, height)
    if p.x <= width and p.x >= 0.0:
        intersections.append(p)
    
    distances = []
    for a in intersections:
        for b in intersections:
            distances.append((len(a - b), a, b))
    distances = sorted(distances)

    return distances[-1][1:]

class Graph(Element, EventDispatcher):
    def __init__(self, width, height, a, b):
        Element.__init__(self)
        self.width = width + 10
        self.height = height + 10
    
        if a and b:
            a, b = float(a), float(b)
            start_point, stop_point = boundary_intersect(width, height, a, b)
        else:
            start_point = Point(0, 0)
            stop_point = Point(width,height)
        self.start = Handle(start=start_point, bbox=Rect(0,0,width,height))
        self.start.layout()
        self.start.push_handlers(on_handle_move=self.update)
        self.start.on_handle_move = self.start_move

        self.stop = Handle(start=stop_point, bbox=Rect(0,0,width,height))
        self.stop.layout()
        self.stop.push_handlers(on_handle_move=self.update)
        self.stop.on_handle_move = self.stop_move

        self.line = Line(self.start.pos, self.stop.pos)
        self.boundary = [
            Line(Point(0,0), Point(width, 0)),
            Line(Point(0, height), Point(width, height)),
            Line(Point(0, 0), Point(0, height)),
            Line(Point(width, 0), Point(width, height)),
        ]

        self.children = [self.start, self.stop]
        self.update(None)

        self.indicator = Point()

    def start_move(self, pos):
        vec = self.start.pos - self.stop.pos
        distance = len(vec)
        if distance < 20:
            target = (vec/distance) * 20.0
            self.start.pos = self.stop.pos + target

    def stop_move(self, pos):
        vec = self.stop.pos - self.start.pos
        distance = len(vec)
        if distance < 20:
            target = (vec/distance) * 20.0
            self.stop.pos = self.start.pos + target

    def do_update(self):
        line = Line(self.start.pos, self.stop.pos)
        intersections = []
        for b in self.boundary:
            intersection = b.intersect(line)
            if intersection:
                if intersection.u1 >= 0.0 and intersection.u1 <= 1.0:
                    intersections.append(intersection)

        distances = []
        for a in intersections:
            for b in intersections:
                distances.append((len(a.p1 - b.p1), a.p1, b.p1))
        distances = sorted(distances)
        self.p1, self.p2 = distances[-1][1:]

    def update(self, pos):
        self.do_update()
        self.dispatch_event('on_graph_change')

    def do_draw(self):
        glColor3f(0.0, 0.0, 0.0)
        width = self.width - 10
        height = self.height - 10
        glPushMatrix()
        glTranslatef(5.0, 5.0, 0.0)

        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_QUADS)
        glVertex3f(0, 0, 0.0)
        glVertex3f(width, 0, 0.0)
        glVertex3f(width, height, 0.0)
        glVertex3f(0, height, 0.0)
        glEnd()

        glBegin(GL_LINES)
        glColor4f(0.2, 0.2, 0.2, 1.0)
        x = 0.0
        while x < width:
            x += width/4.0
            glVertex3f(x, 0.0, 0.0)
            glVertex3f(x, height, 0.0)
        y = 0.0
        while y < height:
            y += height/4.0
            glVertex3f(0.0, y, 0.0)
            glVertex3f(height, y, 0.0)

        glColor4f(1.0, 1.0, 1.0, 1.0)
        glVertex3f(self.p1.x, self.p1.y, 0.0)
        glVertex3f(self.p2.x, self.p2.y, 0.0)
        glEnd()

        glPointSize(5)
        glColor4f(1.0, 0.0, 0.0, 0.8)
        glBegin(GL_POINTS)
        glVertex3f(self.indicator.x, self.indicator.y, 0)
        glEnd()

        glColor4f(1.0, 0.0, 0.0, 0.4)
        glBegin(GL_LINES)
        glVertex3f(self.indicator.x, self.indicator.y, 0)
        glVertex3f(self.indicator.x, 0, 0)
        glVertex3f(self.indicator.x, self.indicator.y, 0)
        glVertex3f(0, self.indicator.y, 0)
        glEnd()
        
        glPopMatrix()
        self.start.draw()
        self.stop.draw()

    def linear_equation(self):
        x1, y1 = self.p1.x, self.p1.y
        x2, y2 = self.p2.x, self.p2.y

        denominator = x2 - x1
        if denominator == 0.0:
            denominator = 0.000000000000000000001
        a = (y2 - y1) / denominator
        b = (x2*y1 - x1*y2) / denominator
        if a == 0.0:
            a = 0.000000000000000000001
        return a, b

Graph.register_event_type('on_graph_change')
