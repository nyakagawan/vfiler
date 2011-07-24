#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import threading

from util import Util

class IntervalTimer( threading.Thread ):
    """ 一定間隔でCallbackを呼び出すTimer
    """
    def __init__( self, interval, callback ):
        threading.Thread.__init__( self )
        self.setDaemon( True )
        self.interval = interval
        self.callback = callback

    def run( self ):
        while True:
            time.sleep( self.interval )
            self.callback()



