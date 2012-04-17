from __future__ import division

import pygrafix

class SpriteFont(object):
    def __init__(self, bold=False):
        if bold:
            self.texture = pygrafix.image.load('sprites/fontbold.png')
            self.cw = 9
            self.ch = 13
        else:
            self.texture = pygrafix.image.load('sprites/font.png')
            self.cw = 7
            self.ch = 13
        self.chars = list([self.texture.get_region((char % 16) * self.cw, (char // 16) * self.ch, self.cw, self.ch) for char in range(256)])
            
    def stringSize(self, string):
        return (len(string) * self.cw, self.ch)
            
    def renderString(self, string, x, y):
        sprites = []
        for i, char in enumerate(string):
            char = ord(char)
            if char > 255: # too big to be in font
                char = ord(' ')
            sprite = pygrafix.sprite.Sprite(
                self.chars[char]
            )
            sprite.x = x + i*self.cw
            sprite.y = y
            sprites.append(sprite)
        pygrafix.sprite.draw_batch(sprites, scale_smoothing = False, blending = 'add')