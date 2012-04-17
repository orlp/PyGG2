import pygrafix
import webbrowser
import socket
import uuid
import struct
import random
from pygrafix.window import key, mouse

import constants
from .handler import Handler
from .spritefont import SpriteFont
from .main import GameClientHandler

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