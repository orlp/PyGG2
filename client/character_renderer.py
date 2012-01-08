from __future__ import division, print_function

import math, pygrafix

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

        #if character.flip: image = pygame.transform.flip(image, 1, 0)
        # FIXME PYGRAFIX FLIPPING

        sprite.anchor_x = self.spriteoffset[0]
        sprite.anchor_y = self.spriteoffset[1]

        sprite.position = renderer.get_screen_coords(character.x, character.y)

        renderer.world_sprites.add_sprite(sprite)


class ScoutRenderer(ClassRenderer):
    def __init__(self):
        self.sprites = [function.load_image("characters/scoutreds/%s" % i) for i in range(4)]

        self.spriteoffset = (24, 30)

class SoldierRenderer(ClassRenderer):
    def __init__(self):
        self.sprites = [function.load_image("characters/soldierreds/%s" % i) for i in range(4)]

        self.spriteoffset = (-24, 30)

class EngineerRenderer(ClassRenderer):
    def __init__(self):
        self.sprites = [function.load_image("characters/engineerreds/%s" % i) for i in range(4)]

        self.spriteoffset = (-24, 30)

class SpyRenderer(ClassRenderer):
    def __init__(self):
        self.sprites = [function.load_image("characters/spyreds/%s" % i) for i in range(4)]

        self.spriteoffset = (-24, 30)

    def render(self, renderer, game, state, character):
        if not character.cloaking:
            ClassRenderer.render(self, renderer, game, state, character)
            # Why is the character still getting drawn on the screen?
