import precision_timer
from pygrafix.window import key, mouse

from .handler import Handler
from . import networker, rendering, spectator
import function
import engine.game, engine.player
import constants
import networking

def get_input(window):
    return {
        "up": window.is_key_pressed(key.W),
        "down": window.is_key_pressed(key.S),
        "left": window.is_key_pressed(key.A),
        "right": window.is_key_pressed(key.D),
        "space": window.is_key_pressed(key.SPACE)
    }

# handler for when client is in game
class GameClientHandler(Handler):
    def __init__(self, window, manager):
        self.manager = manager
        self.window = window

        # create game engine object
        self.game = engine.game.Game()

        self.server_password = ""# FIXME: Remove and replace with something more flexible
        self.player_name = ""

        # Create the networking-handler
        self.networker = networker.Networker(('127.0.0.1', 8190), self) # FIXME: Remove these values, and replace with something easier.
        self.network_update_timer = 0

        # Gets set to true when we're disconnecting, for the networker
        self.destroy = False
        
        #These are used for when we want to detect when certain keys are pressed; append to this list which keys you want tracked
        #(don't forget to remember to add the handle to the step loop below!)
        #DEBUGTOOL
        self.pressed_list = [
            key.DOWN,
            key.UP,
            key.LEFT,
            key.RIGHT,
            key.LEFT_SHIFT,
            ]
        #Generate Dictionary
        self.pressed_dict = {}
        
        for pressedlistkey in self.pressed_list:
            self.pressed_dict[pressedlistkey] = False

    
    def start_game(self, player_id):
        # Only start the game once the networker has confirmed a connection with the server

        # keep state of keys stored for one frame so we can detect down/up events
        self.keys = get_input(self.window)
        self.oldkeys = self.keys

        # TODO REMOVE THIS
        # create player
        self.our_player_id = engine.player.Player(self.game, self.game.current_state, player_id).id
        self.spectator = spectator.Spectator(self.our_player_id)

        # create renderer object
        self.renderer = rendering.GameRenderer(self)

        # pygame time tracking
        self.clock = precision_timer.Clock()
        self.inputsender_accumulator = 0.0 # this counter will accumulate time to send input at a constant rate
        self.fpscounter_accumulator = 0.0 # this counter will tell us when to update the fps info in the title

    def step(self):
        #game loop
        while True:
            self.networker.recieve(self.game, self)
            if self.networker.has_connected:
                self.window.poll_events()
    
                # check if user exited the game
                if not self.window.is_open() or self.window.is_key_pressed(key.ESCAPE):
                    event = networking.event_serialize.ClientEventDisconnect()
                    self.networker.sendbuffer.append(event)
                    break
    
                # handle input
                self.oldkeys = self.keys
                self.keys = get_input(self.window)
                leftmouse = self.window.is_mouse_button_pressed(mouse.LEFT)
                middlemouse = self.window.is_mouse_button_pressed(mouse.MIDDLE)
                rightmouse = self.window.is_mouse_button_pressed(mouse.RIGHT)
    
                mouse_x, mouse_y = self.window.get_mouse_position()
                our_player = self.game.current_state.players[self.our_player_id]
                our_player.up = self.keys["up"]
                our_player.down = self.keys["down"]
                our_player.left = self.keys["left"]
                our_player.right = self.keys["right"]
                our_player.leftmouse = leftmouse
                our_player.middlemouse = middlemouse
                our_player.rightmouse = rightmouse
                our_player.aimdirection = function.point_direction(self.window.width / 2, self.window.height / 2, mouse_x, mouse_y)
    
                if self.window.is_key_pressed(key._1):
                    event = networking.event_serialize.ClientEventChangeclass(constants.CLASS_SCOUT)
                    self.networker.events.append((self.networker.sequence, event))
                elif self.window.is_key_pressed(key._2):
                    event = networking.event_serialize.ClientEventChangeclass(constants.CLASS_PYRO)
                    self.networker.events.append((self.networker.sequence, event))
                elif self.window.is_key_pressed(key._3):
                    event = networking.event_serialize.ClientEventChangeclass(constants.CLASS_SOLDIER)
                    self.networker.events.append((self.networker.sequence, event))
                elif self.window.is_key_pressed(key._4):
                    event = networking.event_serialize.ClientEventChangeclass(constants.CLASS_HEAVY)
                    self.networker.events.append((self.networker.sequence, event))
                elif self.window.is_key_pressed(key._6):
                    event = networking.event_serialize.ClientEventChangeclass(constants.CLASS_MEDIC)
                    self.networker.events.append((self.networker.sequence, event))
                elif self.window.is_key_pressed(key._7):
                    event = networking.event_serialize.ClientEventChangeclass(constants.CLASS_ENGINEER)
                    self.networker.events.append((self.networker.sequence, event))
                elif self.window.is_key_pressed(key._8):
                    event = networking.event_serialize.ClientEventChangeclass(constants.CLASS_SPY)
                    self.networker.events.append((self.networker.sequence, event))
                    

                #This for loop detects to see if a key has been pressed. Currently useful for precision offsets
                #DEBUGTOOL
                for keypress in self.pressed_list:
                    if self.window.is_key_pressed(keypress) == True and self.pressed_dict[keypress] == False:
                        self.pressed_dict[keypress] = True
                        if keypress == key.LEFT:
                            self.game.horizontal -= 1
                        if keypress == key.RIGHT:
                            self.game.horizontal += 1
                            self.pressed_right = True
                        if keypress == key.UP:
                            self.game.vertical -= 1
                        if keypress == key.DOWN:
                            self.game.vertical += 1
                        if keypress == key.LEFT_SHIFT:
                            print("HORIZONTAL OFFSET = " + str(self.game.horizontal))
                            print("VERTICAL OFFSET = " + str(self.game.vertical))
                    elif self.window.is_key_pressed(keypress) == False:
                            self.pressed_dict[keypress] = False
                # did we just release the F11 button? if yes, go fullscreen
                if self.window.is_key_pressed(key.F11):
                    self.window.fullscreen = not self.window.fullscreen
    
                # update the game and render
                frame_time = self.clock.tick()
                frame_time = min(0.25, frame_time) # a limit of 0.25 seconds to prevent complete breakdown
    
                self.fpscounter_accumulator += frame_time
    
                self.networker.recieve(self.game, self)
                self.game.update(self.networker, frame_time)
                self.renderer.render(self, self.game, frame_time)
    
                if self.network_update_timer >= constants.INPUT_SEND_FPS:
                    self.networker.update(self)
                    self.network_update_timer = 0
                else:
                    self.network_update_timer += frame_time
    
                if self.fpscounter_accumulator > 0.5:
                    self.window.title = "PyGG2 - %d FPS" % self.window.get_fps()
                    self.fpscounter_accumulator = 0.0
    
                self.window.flip()
        self.cleanup()

    def cleanup(self):
        #clear buffer, send disconnect, and kiss and fly
        self.destroy = True
        self.networker.update(self)