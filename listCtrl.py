#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import wx
import time

from util import Util
from element import *
from define import Def

class ListCtrl( wx.ListCtrl ):
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
        #print "OnItemSelected !!!"
        pass

    def OnKeyDown( self, event ):
        #print "OnKeyDown !!!!" + str( event.GetKeyCode() )
        keycode = event.GetKeyCode()
        self.moveCursor( keycode )
        self.executeCommand( keycode )

    def moveCursor( self, keycode ):
        """ カーソル移動 """
        nowSel = self.GetFirstSelected()
        itemCount = self.GetItemCount()
        if keycode==Def.CORSOR_UP_KEYCODE:
            self.Select( nowSel, False )
            nowSel = (nowSel-1) if nowSel>0 else itemCount-1
        elif keycode==Def.CORSOR_DOWN_KEYCODE:
            self.Select( nowSel, False )
            nowSel = (nowSel+1) % itemCount
        self.Select( nowSel )
        self.Focus( nowSel )

    def executeCommand( self, keycode ):
        """ いろんなコマンドを実行 """
        focusedItemIndex = self.GetFocusedItem()
        if keycode==Def.FILE_EDIT_KEYCODE:
            cmd = "mvim --remote-silent %s" %( self.getItemAbsPath( focusedItemIndex ) )
            Util.trace("file edit command( %s )" %(cmd) )
            os.system( cmd )

    def getItemAbsPath( self, itemId ):
        """ Itemの絶対パスを取得 """
        itemName = self.GetItem( itemId, Def.LIST_COL_INDEX_NAME )
        name = itemName.GetText()
        itemExt = self.GetItem( itemId, Def.LIST_COL_INDEX_EXT )
        ext = itemExt.GetText()
        return "%s/%s.%s" %( self.curDir_, name, ext )

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




