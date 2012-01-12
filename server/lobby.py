from __future__ import division, print_function

import socket, random, struct
import constants

class Lobbyconnector(object):
    def __init__(self, server):
        self.server = server
        self.server_id = random.randint(0, 60000)# FIXME: A more reliable system without duplicates
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def update(self, server):
        packet = ""
        # TODO: Make a lobby reg packet and bug medo to add compatibility for UDP in the gg2 lobby, because faking is stupid.
