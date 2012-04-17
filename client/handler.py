import pygrafix

# manages client, switches handlers
class ClientManager(object):
    def __init__(self, handler):
        # set display mode
        self.window = pygrafix.window.Window(800, 600, title = "PyGG2 - 0 FPS", fullscreen = False, vsync = False)

        self.handler = handler(self.window, self)

        self.quitting = False
        self.newhandler = None

    def run(self):
        while self.handler.step() and not self.quitting:
            if self.newhandler:
                self.handler.clearup()
                self.handler = self.newhandler(self.window, self)
                self.newhandler = None
        self.clearup()

    def switch_handler(self, handler):
        self.newhandler = handler

    def quit(self):
        self.quitting = True

    def clearup(self):
        self.window.close()

# handler base class, implements dummy handler
class Handler(object):
    def __init__(self, window, manager):
        self.manager = manager
        self.window = window

    # if the handler returns a non-true value, the game exits
    def step(self):
        return True

    # run when handler is about to be destroyed
    def clearup(self):
        pass