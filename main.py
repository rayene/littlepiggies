import pyglet
from ui import Layer
from window import Window
from dialog import Dialog

class Application(object):
    def __init__(self):
        self.window = Window(self)
        self.window.push_handlers(self)
        self.layer = Layer(self.window)

        dialog = Dialog(self.window)
        self.layer.add(dialog)
        dialog.push_handlers(self)
        self.layer.enable()
        
    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.event.key.ESCAPE:
            quit()

    def draw(self):
        self.layer.draw()

if __name__ == '__main__':
    app = Application()
    pyglet.app.run()
