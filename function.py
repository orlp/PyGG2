#!/usr/bin/env python

from __future__ import division, print_function

import math
import pyglet
from pyglet.gl import *
import mask

import zipfile
import cStringIO
import os.path


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

# http://www.mail-archive.com/pyglet-users@googlegroups.com/msg04559.html
def disable_anti_aliasing(texture):
    glBindTexture(texture.target, texture.id)
    glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glBindTexture(texture.target, 0)

def enable_anti_aliasing(texture):
    glBindTexture(texture.target, texture.id)
    glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glBindTexture(texture.target, 0)
    
# prevent double-loading, only load a filename once
loaded_images = {}
def load_image(filename, anti_aliasing = False):
    image = None
    
    if filename in loaded_images:
        image = pyglet.image.ImageData(*loaded_images[filename])
    else:
        # first try to load the sprite from the sprite folder, fall back to our zipped sprites
        # this allows users to override sprites, and makes testing/developing easier
        try:
            image = pyglet.image.load("sprites/" + filename + ".png")
        except:
            # open zipfile and create file object from the data
            sprites = zipfile.ZipFile("sprites.zip", "r")
            spritefile = cStringIO.StringIO(sprites.open(filename + ".png", "rb").read())
            
            # load image and close file object
            image = pyglet.image.load(filename + ".png", spritefile)
            spritefile.close()
    
        imgdata_obj = image.get_image_data()
        loaded_images[filename] = (image.width, image.height, imgdata_obj.format, imgdata_obj.get_data(imgdata_obj.format, imgdata_obj.pitch), imgdata_obj.pitch)
    
    if not anti_aliasing:
        disable_anti_aliasing(image.get_texture())
    
    return image
    
    
masks = {}
def load_mask(filename, give_orig=False): 
    if filename in masks:
        if give_orig: return masks[filename]
        else: return masks[filename].copy()
    
    bitmask = None
    # first try to load the sprite from the sprite folder, fall back to our zipped sprites
    # this allows users to override sprites, and makes testing/developing easier
    try:
        bitmask = mask.from_image("sprites/" + filename + ".png")
    except:
        sprites = zipfile.ZipFile("sprites.zip", "r")
        spritefile = cStringIO.StringIO(sprites.open(filename + ".png", "r").read())
        bitmask = mask.from_image(spritefile)
        spritefile.close()
    
    masks[filename] = bitmask
    
    if give_orig: return bitmask
    else: return bitmask.copy()