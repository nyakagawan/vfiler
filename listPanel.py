#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import wx

from listCtrl import ListCtrl
from define import Def
from idManager import IdManager

class ListPanel( wx.Panel ):
    """ ファイルリスト、リストの上のパス表示エリアが乗るPanelコントロール
    """
    def __init__( self, parent, guid, paneKind, frame ):
        wx.Panel.__init__( self, parent, guid )
        self.frame = frame
        self.paneKind = paneKind
        self.staticText = None
        self.listCtrl = None

    def initGui( self ):
        vbox = wx.BoxSizer( wx.VERTICAL )
        self.staticText = wx.StaticText( self, -1, "Static " + str(self.paneKind) )
        vbox.Add( self.staticText, 0, wx.EXPAND, 10 )
        self.listCtrl = ListCtrl( self, IdManager.listCtrl( self.paneKind ), self.paneKind, self.frame )
        vbox.Add( self.listCtrl, 1, wx.EXPAND )
        self.SetSizer( vbox )

    def getListCtrl( self ):
        return self.listCtrl

    def setPathText( self, text ):
        self.staticText.SetLabel( text )



