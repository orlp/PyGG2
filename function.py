#!/usr/bin/env python

from __future__ import division, print_function

import math
import mask

# make pygrafix an optional import
# if we are running the server without pygrafix everything will work fine
# as long as we don't call functions in the file that use pygame
try:
    import pygrafix
except: pass

import zipfile
import cStringIO
import os.path

spritesfolder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sprites/")

def sign(x):
    # Returns the sign of the number given
    return cmp(x, 0)

def point_direction(x1, y1, x2, y2):
    angle = -math.degrees(math.atan2(y2 - y1, x2 - x1))
    if angle < 0: angle += 360
    return angle

# from http://www.nanobit.net/doxy/quake3/q__math_8c-source.html LerpAngle
def interpolate_angle(a, b, alpha):
    a, b = a % 360, b % 360

    if b - a > 180: b -= 360
    if b - a < -180: b += 360

    return (a + alpha * (b - a)) % 360

# prevent double-loading, only load a filename once
images = {}
def load_image(filename):
    if filename in images:
        return images[filename].copy()

    # first try to load the sprite from the sprite folder, fall back to our zipped sprites
    # this allows users to override sprites, and makes testing/developing easier
    try:
        image = pygrafix.image.load(spritesfolder + filename + ".png")
    except:
        sprites = zipfile.ZipFile("sprites.zip", "r")
        spritefile = cStringIO.StringIO(sprites.open("sprites/" + filename + ".png", "r").read())
        image = pygrafix.image.load(spritefile, filename + ".png")
        spritefile.close()

    images[filename] = image

    return image

masks = {}
def load_mask(filename, give_orig=False):
    if filename in masks:
        if give_orig: return masks[filename]
        else: return masks[filename].copy()

    # first try to load the sprite from the sprite folder, fall back to our zipped sprites
    # this allows users to override sprites, and makes testing/developing easier
    try:
        bitmask = mask.from_image(spritesfolder + filename + ".png")
    except:
        sprites = zipfile.ZipFile("sprites.zip", "r")
        spritefile = cStringIO.StringIO(sprites.open(filename + ".png", "r").read())
        bitmask = mask.from_image(spritefile)
        spritefile.close()

    masks[filename] = bitmask

    if give_orig: return bitmask
    else: return bitmask.copy()
