from __future__ import division, print_function

import sys
import time

if sys.platform == "win32":
    # on Windows, the best timer is time.clock()
    timerfunc = time.clock
else:
    # on most other platforms, the best timer is time.time()
    timerfunc = time.time

class Clock(object):
    def __init__(self):
        self.lasttime = timerfunc()
        self.curtime = timerfunc()
        self.frametime = 0

    def tick(self):
        self.lasttime = self.curtime
        self.curtime = timerfunc()
        dt = self.curtime - self.lasttime

        self.frametime = 0.9 * self.frametime + 0.1 * dt
        
        return dt

    def getfps(self):
        if self.frametime == 0: return 0
        return 1 / self.frametime
