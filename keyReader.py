#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import wx

from define import Def

class KeyReader( object ):
    """ OnKeyDownのeventオブジェクトから何が押されたのかを判定する関数を提供する
    """
    def __init__( self, event ):
        self.keycode = event.GetKeyCode()
        self.event = event


    def cursorUp( self ):
        return True if self.keycode==Def.CORSOR_UP_KEYCODE else False

    def cursorDown( self ):
        return True if self.keycode==Def.CORSOR_DOWN_KEYCODE else False

    def cursorLeft( self ):
        return True if self.keycode==Def.CORSOR_LEFT_KEYCODE else False

    def cursorRight( self ):
        return True if self.keycode==Def.CORSOR_RIGHT_KEYCODE else False


    def moveDirUp( self ):
        return True if self.keycode==Def.MOVE_DIR_UP_KEYCODE else False

    def moveDirDown( self ):
        return True if self.keycode==Def.MOVE_DIR_DOWN_KEYCODE else False


    def fileEdit( self ):
        return True if self.keycode==Def.FILE_EDIT_KEYCODE else False

    def quit( self ):
        return True if self.keycode==Def.QUIT_KEYCODE else False

    def copy( self ):
        return True if self.keycode==Def.COPY_KEYCODE else False

    def move( self ):
        return True if self.keycode==Def.MOVE_KEYCODE else False

    def delete( self ):
        return True if self.keycode==Def.DELETE_KEYCODE else False

    def search( self ):
        return True if self.keycode==Def.SEARCH_KEYCODE else False

    def cancel( self ):
        if self.event.GetModifiers()==wx.MOD_CONTROL and self.keycode==ord("["):
            return True
        if self.keycode==wx.WXK_ESCAPE:
            return True
        return False


