# -*- coding: utf-8 -*-

"""
    primitives
    ~~~~~~~~~~

    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""

import math
from pyglet.gl import *

def fourth_circle(radius):
    segments = 15.0 if radius > 15 else float(radius)
    step = math.pi / (segments*2)

    i = 0.0
    while i < math.pi / 2:
        yield math.cos(i) * radius, math.sin(i) * radius
        i += step
    if abs(i-radius) > 0.00001:
        yield 0.0, radius

def box_strip(width, height, corner_radius=0):
    if corner_radius > 0:
        radius = min(width, height) / 2.0 if min(width, height) < corner_radius*2 else corner_radius
        edge = list(fourth_circle(radius))
        for x, y in edge:
            yield x+width-radius, y+height-radius
        for x, y in edge:
            yield radius-y, x+height-radius
        for x, y in edge:
            yield radius-x, radius-y
        for x, y in edge:
            yield y+width-radius, radius-x
        yield width, height-radius
            
    else:
        yield 0.0, 0.0
        yield width, 0.0
        yield width, height,
        yield 0.0, height
        yield 0.0, 0.0

