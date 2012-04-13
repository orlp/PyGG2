from __future__ import division, print_function

import math
import pygrafix

import function

class ClassRenderer(object):
    def __init__(self):
        pass

    def render(self, renderer, game, state, character):
        anim_frame = int(character.animoffset)

        if not character.onground(game, state):
            anim_frame = 1

        if character.intel:
            anim_frame += 2

        sprite = pygrafix.sprite.Sprite(self.sprites[anim_frame])

        if character.flip:
            sprite.flip_x = True
            sprite.anchor_x = self.spriteoffset_flipped[0]
            sprite.anchor_y = self.spriteoffset_flipped[1]
        else:
            sprite.anchor_x = self.spriteoffset[0]
            sprite.anchor_y = self.spriteoffset[1]

        sprite.position = renderer.get_screen_coords(character.x, character.y)

        renderer.world_sprites.append(sprite)


class ScoutRenderer(ClassRenderer):
    def __init__(self):
        self.depth = 0
        self.sprites = [pygrafix.image.load("characters/scoutreds/%s.png" % i) for i in range(4)]

        self.spriteoffset = (24, 30)
        self.spriteoffset_flipped = (28, 30)

class PyroRenderer(ClassRenderer):
    def __init__(self):
        self.depth = 0
        self.sprites = [pygrafix.image.load("characters/pyroreds/%s.png" % i) for i in range(4)]

        self.spriteoffset = (24, 30)
        self.spriteoffset_flipped = (28, 30)

class SoldierRenderer(ClassRenderer):
    def __init__(self):
        self.depth = 0
        self.sprites = [pygrafix.image.load("characters/soldierreds/%s.png" % i) for i in range(4)]

        self.spriteoffset = (24, 30)
        self.spriteoffset_flipped = (28, 30)

class HeavyRenderer(ClassRenderer):
    def __init__(self):
        self.depth = 0
        self.sprites = [pygrafix.image.load("characters/heavyreds/%s.png" % i) for i in range(4)]

        self.spriteoffset = (14, 30)
        self.spriteoffset_flipped = (36, 30)

class EngineerRenderer(ClassRenderer):
    def __init__(self):
        self.depth = 0
        self.sprites = [pygrafix.image.load("characters/engineerreds/%s.png" % i) for i in range(4)]

        self.spriteoffset = (26, 30)
        self.spriteoffset_flipped = (26, 30)

class SpyRenderer(ClassRenderer):
    def __init__(self):
        self.depth = 0
        self.sprites = [pygrafix.image.load("characters/spyreds/%s.png" % i) for i in range(4)]

        self.spriteoffset = (22, 30)
        self.spriteoffset_flipped = (30, 30)

    def render(self, renderer, game, state, character):
        if not character.cloaking:
            ClassRenderer.render(self, renderer, game, state, character)
            # FIXME: Why is the character still getting drawn on the screen if cloaked?
