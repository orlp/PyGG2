#!/usr/bin/env python

from __future__ import division, print_function

import math
import mask
import engine.character
import constants

# make pygrafix an optional import
# if we are running the server without pygrafix everything will work fine
# as long as we don't call functions in the file that use pygame
try:
    import pygrafix
except: pass

import zipfile
import cStringIO
import os.path
import sys

spritesfolder = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "sprites/")
spriteszip = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "sprites.zip")

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

masks = {}
def load_mask(filename, give_orig=False):
    if filename in masks:
        if give_orig: return masks[filename]
        else: return masks[filename].copy()

    # first try to load the sprite from the sprite folder, fall back to our zipped sprites
    # this allows users to override sprites, and makes testing/developing easier
    try:
        bitmask = mask.from_image(spritesfolder +  filename + ".png")
    except:
        sprites = zipfile.ZipFile(spriteszip, "r")
        spritefile = cStringIO.StringIO(sprites.open("sprites/" + filename + ".png", "r").read())
        bitmask = mask.from_image(spritefile)
        spritefile.close()

    masks[filename] = bitmask

    if give_orig: return bitmask
    else: return bitmask.copy()

def convert_class(class_object):
        # Try converting the class to it's constant first
        if class_object == engine.character.Scout:
            return constants.CLASS_SCOUT
        elif class_object == engine.character.Pyro:
            return constants.CLASS_PYRO
        elif class_object == engine.character.Soldier:
            return constants.CLASS_SOLDIER
        elif class_object == engine.character.Heavy:
            return constants.CLASS_HEAVY
        elif class_object == engine.character.Engineer:
            return constants.CLASS_ENGINEER
        elif class_object == engine.character.Spy:
            return constants.CLASS_SPY

        # Didn't work, try converting the constant to it's class
        if class_object == constants.CLASS_SCOUT:
            return engine.character.Scout
        elif class_object == constants.CLASS_PYRO:
            return engine.character.Pyro
        elif class_object == constants.CLASS_SOLDIER:
            return engine.character.Soldier
        elif class_object == constants.CLASS_HEAVY:
            return engine.character.Heavy
        elif class_object == constants.CLASS_ENGINEER:
            return engine.character.Engineer
        elif class_object == constants.CLASS_SPY:
            return engine.character.Spy
        else:
            print("ERROR: UNKNOWN CLASS ARGUMENT IN Functions.get_class().", class_object)
            return constants.CLASS_SCOUT
