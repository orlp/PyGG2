#!/usr/bin/env python

from __future__ import division, print_function

import pygrafix
from pygrafix.window import key
from pygrafix.window import mouse

import precision_timer
import client.spectator
import engine.game
import engine.player
import engine.character
import client.rendering
import client.networker
from client.spritefont import SpriteFont
import networking.event_serialize
import constants
import function
import random
import webbrowser
import socket
import uuid
import struct
import collections

# DEBUG ONLY
import cProfile
import pstats
import os

def get_input(window):
    return {
        "up": window.is_key_pressed(key.W),
        "down": window.is_key_pressed(key.S),
        "left": window.is_key_pressed(key.A),
        "right": window.is_key_pressed(key.D),
        "space": window.is_key_pressed(key.SPACE)
    }

# add resource locations
if os.path.isdir("sprites"):
    pygrafix.resource.add_location("sprites")
if os.path.isfile("sprites.zip"):
    pygrafix.resource.add_location("sprites.zip")

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

# generic menu handler
class MenuHandler(Handler):
    menuitems = []
    offsetx = 30
    offsety = 30
    spacing = 30

    def __init__(self, window, manager):
        self.manager = manager
        self.window = window

        self.font = SpriteFont(bold=True)
        self.prevleft = None

    def draw(self, hoveritem=None):
        x = self.offsetx
        y = self.offsety
        for item in self.menuitems:
            if item is hoveritem:
                width, height = self.font.stringSize(item[0])
                pygrafix.draw.rectangle((x, y), (width, height), (1, 0.5, 0))
            self.font.renderString(item[0], x, y)
            y += self.spacing

        self.window.flip()

    def step(self):
        self.window.poll_events()

        # check if user exited the game
        if not self.window.is_open() or self.window.is_key_pressed(key.ESCAPE):
            return False

        # handle input
        self.keys = get_input(self.window)
        leftmouse = self.window.is_mouse_button_pressed(mouse.LEFT)
        mouse_x, mouse_y = self.window.get_mouse_position()
        x = self.offsetx
        y = self.offsety
        hoveritem = None
        for item in self.menuitems:
            width, height = self.font.stringSize(item[0])
            # are we hovering over this item?
            if x <= mouse_x <= x+width and y <= mouse_y <= y+height:
                hoveritem = item
                if leftmouse and not self.prevleft and item[1]:
                    item[1](self)
            y += self.spacing
        self.prevleft = leftmouse

        # draw stuff
        self.draw(hoveritem)

        # troll
        self.window.title = u"PyGG2 - \u221e FPS".encode('utf8')

        return True

# handler for main menu
class MainMenuHandler(MenuHandler):
    def item_start_game(self):
        self.manager.switch_handler(GameClientHandler)

    def item_go_github(self):
        webbrowser.open('http://github.com/nightcracker/PyGG2')

    def item_go_lobby(self):
        self.manager.switch_handler(LobbyHandler)

    def item_quit(self):
        self.manager.quit()

    menuitems = [
        ('Start test client', item_start_game),
        ('Lobby', item_go_lobby),
        ('Go to GitHub', item_go_github),
        ('Quit', item_quit)
    ]

    offsetx = 10
    offsety = 120
    spacing = 30

    def __init__(self, window, manager):
        super(MainMenuHandler, self).__init__(window, manager)

        self.menubg = pygrafix.sprite.Sprite(
            pygrafix.image.load(
                "sprites/gameelements/menubackgrounds/%s.png" % random.randint(0,2)
            )
        )
        self.menubg.x = 200

    def draw(self, hoveritem):
        self.menubg.draw(scale_smoothing = False)
        pygrafix.draw.rectangle((0, 0), (200, 600), (0.7, 0.25, 0))

        super(MainMenuHandler, self).draw(hoveritem)

# handler for lobby
class LobbyHandler(MenuHandler):
    def go_back(self):
        self.manager.switch_handler(MainMenuHandler)

    offsetx = 210
    offsety = 120
    spacing = 30

    def __init__(self, window, manager):
        super(LobbyHandler, self).__init__(window, manager)

        self.menuitems = [
            ('Back to Main Menu', LobbyHandler.go_back),
            ('', None)
        ]

        self.menubg = pygrafix.sprite.Sprite(
            pygrafix.image.load("sprites/gameelements/menubackgrounds/0.png")
        )
        self.menubg.x = 200

        self.sendbuf = b''

        self.lobbysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.num_servers = -1
        self.servers_read = 0

        self.lobbysocket.connect((constants.LOBBY_HOST, constants.LOBBY_PORT))
        lobbyuuid = uuid.UUID(constants.LOBBY_MESSAGE_TYPE_LIST).get_bytes()
        self.protocoluuid = uuid.UUID(constants.GG2_LOBBY_UUID).get_bytes()
        self.send_all(lobbyuuid+self.protocoluuid)

    def send_all(self, buf):
        while len(buf) > 0:
            sent = self.lobbysocket.send(buf)
            buf = buf[sent:]

    def recv_all(self, size):
        buf = b''
        while len(buf) < size:
            buf += self.lobbysocket.recv(size - len(buf))
        return buf
        #return self.lobbysocket.recv(size)

    def step(self):
        if self.num_servers == -1:
            num = self.recv_all(4)
            num = struct.unpack('>I', num)[0]
            self.num_servers = num
        elif self.servers_read < self.num_servers:
            length = self.recv_all(4)
            length = struct.unpack('>I', length)[0]
            if length > 100000:
                print('Server data block from lobby is too large')
                sys.exit(0)
            datablock = self.recv_all(length)
            server = {}
            items = struct.unpack('>BHBBBB18xHHHHH', datablock[:1+2+1+1+1+1+18+2+2+2+2+2])
            datablock = datablock[1+2+1+1+1+1+18+2+2+2+2+2:]
            server['protocol'], server['port'] = items[:2]
            server['ip'] = '.'.join([str(octet) for octet in items[2:6]])
            server['slots'], server['players'], server['bots'] = items[6:9]
            server['private'] = bool(items[9] & 1)
            infolen = items[10]
            server['infos'] = {}
            for i in range(infolen):
                keylen = struct.unpack('>B', datablock[0])[0]
                datablock = datablock[1:]
                key = datablock[:keylen]
                datablock = datablock[keylen:]
                datalen = struct.unpack('>H', datablock[:2])[0]
                datablock = datablock[2:]
                data = datablock[:datalen]
                datablock = datablock[datalen:]
                if key == 'protocol_id':
                    same_protocol_id = data == (self.protocoluuid)
                else:
                    server['infos'][key] = data
            server['compatible'] = (server['protocol'] == 0 and server['port'] > 0 and same_protocol_id)
            if server['bots']:
                playercount = '%s+%s' % (server['players'], server['bots'])
            else:
                playercount = str(server['players'])
            server['playerstring'] = '%s/%s' % (playercount, server['slots'])
            server['name'] = server['infos']['name']
            self.servers_read += 1

            self.menuitems.append( ('%s - [%s]' % (server['name'], server['playerstring']), None) )
        return super(LobbyHandler, self).step()

    def draw(self, hoveritem):
        self.menubg.draw(scale_smoothing = False)
        pygrafix.draw.rectangle((0, 0), (200, 600), (0.7, 0.25, 0))

        super(LobbyHandler, self).draw(hoveritem)

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
        self.networker = client.networker.Networker(('127.0.0.1', 8190), self) # FIXME: Remove these values, and replace with something easier.
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
            key.SPACE
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
        self.spectator = client.spectator.Spectator(self.our_player_id)

        # create renderer object
        self.renderer = client.rendering.GameRenderer(self)

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
                        if keypress == key.LEFT:
                            self.game.horizontal -= 1
                            self.pressed_dict[keypress] = True
                        if keypress == key.RIGHT:
                            self.game.horizontal += 1
                            self.pressed_right = True
                            self.pressed_dict[keypress] = True
                        if keypress == key.UP:
                            self.game.vertical -= 1
                            self.pressed_dict[keypress] = True
                        if keypress == key.DOWN:
                            self.game.vertical += 1
                            self.pressed_dict[keypress] = True
                        if keypress == key.SPACE:
                            print("HORIZONTAL OFFSET = " + str(self.game.horizontal))
                            print("VERTICAL OFFSET = " + str(self.game.vertical))
                            self.pressed_space = True
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

def profileGG2():
    cProfile.run("GG2main()", sort="time")

def GG2main(skipmenu=False):
    if skipmenu:
        cm = ClientManager(GameClientHandler)
    else:
        cm = ClientManager(MainMenuHandler)
    cm.run()

if __name__ == "__main__":
    # when profiling:
    profileGG2()
    # GG2main()
