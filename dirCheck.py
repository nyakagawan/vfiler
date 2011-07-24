#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import threading
from FSEvents import *

from util import Util

class DirCheck( threading.Thread ):
    """ ディレクトリの更新をチェックするクラス
    """
    def __init__( self, path ):
        threading.Thread.__init__( self )
        # http://techno-st.net/2010/02/06/python-3.html
        self.setDaemon( True )

        if path[-1] == '/':
            path = path[:-1]
        self._path = os.path.abspath( path )
        self._isChanged = False

        self.start()

    def isChanged( self ):
        return self._isChanged

    def offChangeFlag( self ):
        self._isChanged = False

    def run( self ):
        path = self._path
        self._streamRef = FSEventStreamCreate(
                kCFAllocatorDefault,
                self.eventsCallback,
                path,
                [path],
                kFSEventStreamEventIdSinceNow,# sinceWhen
                1.0,# latency
                0
                )

        if self._streamRef is None:
            Util.trace( "FSEventStreamCreate is failed" )
            return

        if False:
            FSEventStreamShow( self._streamRef )

        FSEventStreamScheduleWithRunLoop(self._streamRef, CFRunLoopGetCurrent(), kCFRunLoopDefaultMode)
        startedOK = FSEventStreamStart(self._streamRef)
        if not startedOK:
            Util.trace("failed to start the FSEventStream")
            return

#        if True:
#            timer = CFRunLoopTimerCreate(
#                    FSEventStreamGetSinceWhen(streamRef), 
#                    CFAbsoluteTimeGetCurrent() + settings.flush_seconds, 
#                    settings.flush_seconds,
#                    0, 0, timer_callback, streamRef)
#            CFRunLoopAddTimer(CFRunLoopGetCurrent(), timer, kCFRunLoopDefaultMode)

        CFRunLoopRun()

    def __del__( self ):
        Util.trace( "destroy DirCheck instance" )
        streamRef = self._streamRef
        #Stop / Invalidate / Release
        FSEventStreamStop(streamRef)
        FSEventStreamInvalidate(streamRef)
        FSEventStreamRelease(streamRef)

    def eventsCallback(self, streamRef, clientInfo, numEvents, eventPaths, eventMarsks, eventIDs):
        fullPath = clientInfo
        print ("callback: clientInfo[%s]" %(clientInfo) )

        for i in range(numEvents):
            path = eventPaths[i]
            if path[-1] == '/':
                path = path[:-1]

            print "eventPath => %s" %(path)
            if path==self._path:
                self._isChanged = True

            eventMarsk = eventMarsks[i]
            if eventMarsk & kFSEventStreamEventFlagMustScanSubDirs:
                Util.trace( "kFSEventStreamEventFlagMustScanSubDirs" )
                recursive = True

            elif eventMarsk & kFSEventStreamEventFlagUserDropped:
                Util.trace( "kFSEventStreamEventFlagUserDropped" )
                recursive = True
                path = fullPath

            elif eventMarsk & kFSEventStreamEventFlagKernelDropped:
                Util.trace( "kFSEventStreamEventFlagKernelDropped" )
                recursive = 1
                path = fullPath

            else:
                Util.trace( "recive FSEvent callback" )
                recursive = False



# for test
def main():
    argv = sys.argv
    argc = len( argv )
    checkPath = "./"
    if argc>1:
        checkPath = argv[1]
    print "checkDir => " + checkPath

    dirCheck = DirCheck( checkPath )
    print "afetr create"

    import time
    while True:
        time.sleep( 5 )

if __name__=="__main__":
    main()

