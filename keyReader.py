#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import wx

from define import Def


IS_DPRINT_KEYDOWN_DETAIL = False
IS_KEYDOWN_IGNORE = False

class KeyReader( object ):
    """ OnKeyDownのeventオブジェクトから何が押されたのかを判定する関数を提供する
    """
    MOD_KEY_ALT     =(1<<0)
    MOD_KEY_CMD     =(1<<1)
    MOD_KEY_CTRL    =(1<<2)
    MOD_KEY_SHIFT   =(1<<3)

    def __init__( self, event ):
        self.event = event
        self.keycode = event.GetKeyCode()
        self.modKey = 0
        if self.event.AltDown():    self.modKey |= self.MOD_KEY_ALT
        if self.event.CmdDown():    self.modKey |= self.MOD_KEY_CMD
        if self.event.ControlDown():self.modKey |= self.MOD_KEY_CTRL
        if self.event.ShiftDown():  self.modKey |= self.MOD_KEY_SHIFT

        if IS_DPRINT_KEYDOWN_DETAIL:
            print "keycode " + str(self.keycode)
            print "- alt " + "true" if self.event.AltDown() else "false"
            print "- cmd " + "true" if self.event.CmdDown() else "false"
            print "- ctrl " + "true" if self.event.ControlDown() else "false"
            print "- shift " + "true" if self.event.ShiftDown() else "false"

        if IS_KEYDOWN_IGNORE:
            self.keycode = 0

    def getKeyCode(self):
        return self.keycode

    def pressEnter( self ):
        return True if self.keycode==wx.WXK_RETURN else False


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

    def grep( self ):
        return True if self.keycode==Def.GREP_KEYCODE else False

    def cancel( self ):
        if self.event.HasModifiers() and self.event.GetModifiers()==wx.MOD_CONTROL and self.keycode==ord("["):
            return True
        if self.keycode==wx.WXK_ESCAPE:
            return True
        return False

    def sameDir( self ):
        return True if self.keycode==Def.SAME_DIR_KEYCODE else False


