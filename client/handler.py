import pygrafix
import json
import os.path

# manages client, switches handlers
class ClientManager(object):
    def __init__(self, handler):
        # set display mode
        self.window = pygrafix.window.Window(800, 600, title = "PyGG2 - 0 FPS", fullscreen = False, vsync = False)

        self.load_config()

        self.quitting = False
        self.newhandler = None

        self.handler = handler(self.window, self)

    def load_config(self):
        if os.path.exists('client_cfg.json'):
            with open('client_cfg.json', 'r') as fp:
                self.config = json.load(fp)
        else:
            self.config = {}

    def save_config(self):
        with open('client_cfg.json', 'w') as fp:
            json.dump(self.config, fp, indent=4)

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
        self.save_config()

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