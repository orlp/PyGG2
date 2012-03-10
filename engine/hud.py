#!/usr/bin/env python

from __future__ import division, print_function

import math
import random

import entity
import character
import function
import mask

class HealthHUD(entity.HudObject):

    def __init__(self):
    
        self.x = 50
        self.y = 50