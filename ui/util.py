# -*- coding: utf-8 -*-

"""
    util
    ~~~~

    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""

import os
import pyglet

class Loader(object):
    def __init__(self, module, subdir):
        path = os.path.dirname(module)
        self.path = os.path.join(path, subdir)

    def image(self, name):
        path = os.path.join(self.path, name)
        return pyglet.image.load(path)
