#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import wx
import time

from util import Util
from element import *
from define import Def
from keyReader import KeyReader

class TextCtrl( wx.TextCtrl ):
    """ ファイルリストGUI
    """
    def __init__( self, parent, id, frame ):
        wx.TextCtrl.__init__( self, parent, id )
        self.frame = frame
        self.Bind( wx.EVT_KEY_DOWN, self.OnKeyDown )
        self.Bind( wx.EVT_SET_FOCUS, self.OnFocus )

    def getFrame( self ):
        return self.frame

    def OnKeyDown( self, event ):
        """ キーダウンイベントハンドラ
        """
        kr = KeyReader( event )
        if kr.cancel():
            # ESC押されたらListCtrlにフォーカスを戻す
            self.getFrame().setFocusedPane( self.getFrame().getFocusedPane() )
        event.Skip()

    def OnFocus( self, event ):
        self.Clear()

