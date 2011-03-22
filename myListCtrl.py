#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import wx
import time

from util import Util
from element import *

class MyListCtrl( wx.ListCtrl ):
    """ ファイルリストGUI
    """
    def __init__( self, parent, id ):
        wx.ListCtrl.__init__( self, parent, id, style=wx.LC_REPORT )
        self.initGui()
        self.curDir_ = os.path.abspath( os.getcwd() )
        self.updateFileList( self.curDir_ )

    def initGui( self ):
        self.InsertColumn( 0, 'Name' )
        self.InsertColumn( 1, 'Ext' )
        self.InsertColumn( 2, 'Size', wx.LIST_FORMAT_RIGHT )
        self.InsertColumn( 3, 'Modified' )

        self.SetColumnWidth( 0, 220 )
        self.SetColumnWidth( 1, 70 )
        self.SetColumnWidth( 2, 100 )
        self.SetColumnWidth( 3, 420 )

        self.SetBackgroundColour( BG_COLOR )

        self.Bind( wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected )
        self.Bind( wx.EVT_LIST_KEY_DOWN, self.OnKeyDown )

    def OnItemSelected( self, event ):
        print "OnItemSelected !!!"
    def OnKeyDown( self, event ):
        print "OnKeyDown !!!!" + str( event.GetKeyCode() )

    def changeDir( self, path ):
        """ カレントディレクトリを移動
        """
#        path = os.path.abspath( path )
#        if not self.curDir_:
#            self.curDir_ = ElemDir( -1, self, path )
  
    def updateFileList( self, curDir ):
        Util.trace( "curDir [%s]. updateFileList" %(curDir) )
        elems = os.listdir( curDir )
        iFile = 0
        for e in elems:
            if os.path.isdir( e ):
                Util.trace( "adddir " + e )
                elem = ElemDir( iFile, self, e )
            else:
                Util.trace( "addfile " + e )
                elem = ElemFile( iFile, self, e )
            elem.update()
            iFile += 1




