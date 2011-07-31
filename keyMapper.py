#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import wx

from define import Def

class KeyDef():
    """ Key定義。
        KeyCode（ord("a")とか）とModifier定義（MOD_KEY_XXXX）からなる
    """
    MOD_KEY_ALT     =(1<<0)
    MOD_KEY_CMD     =(1<<1)
    MOD_KEY_CTRL    =(1<<2)
    MOD_KEY_SHIFT   =(1<<3)

    def __init__( self, keycode, modKey=0 ):
        self.keycode = keycode
        self.modKey = modKey

    def getKey( self ):
        """ KeyHashを取得
            Command辞書のKeyとなる
        """
        return "m_%d_c_%d" %(self.modKey, self.keycode)

    @classmethod
    def getKeyFromEvent( cls, event ):
        """ KeyHashを取得
            KeyDownイベントオブジェクトから作って返す
        """
        keycode = event.GetKeyCode()
        modKey = 0
        if event.AltDown():    modKey |= cls.MOD_KEY_ALT
        if event.CmdDown():    modKey |= cls.MOD_KEY_CMD
        if event.ControlDown():modKey |= cls.MOD_KEY_CTRL
        if event.ShiftDown():  modKey |= cls.MOD_KEY_SHIFT
        return cls( keycode, modKey ).getKey()

class CommandDef():
    """ Command定義。KeyDefとCommand関数からなる
    """
    def __init__( self, keyDef, cmdFunc ):
        self.keyDef = keyDef
        self.cmdFunc = cmdFunc
    def getKey( self ):
        return self.keyDef.getKey()
    def getCmd( self ):
        return self.cmdFunc


class KeyMapper():
    vfiler = None
    cmdDict = {}    # KeyはKeyDefのKeyHash。ValueはCommand関数
    cancelKeyDefs = [
            KeyDef( ord("["), KeyDef.MOD_KEY_CTRL ).getKey(),
            KeyDef( wx.WXK_ESCAPE ).getKey(),
            ]
    decideKeyDefs = [
            KeyDef( wx.WXK_RETURN ).getKey(),
            ]

    @classmethod
    def add( cls, cmdDef ):
        """ KeyMappingの追加
        """
        cls.cmdDict[ cmdDef.getKey() ] = cmdDef.getCmd()

    @classmethod
    def get( cls, key ):
        """ KeyHashからCommandの取得
        """
        if cls.cmdDict.has_key( key ):
            return cls.cmdDict[ key ]
        return None

    @classmethod
    def execute( cls, event ):
        """ KeyにMappingされたCommandの実行
        """
        key = KeyDef.getKeyFromEvent( event )
        cmd = cls.get( key )
        if cmd:
            cmd( cls.vfiler, event )

    @classmethod
    def isCancel( cls, event ):
        key = KeyDef.getKeyFromEvent( event )
        for cancelKeyDef in cls.cancelKeyDefs:
            if key==cancelKeyDef:
                return True
        return False

    @classmethod
    def isDecide( cls, event ):
        key = KeyDef.getKeyFromEvent( event )
        for decideKeyDef in cls.decideKeyDefs:
            if key==decideKeyDef:
                return True
        return False

    @classmethod
    def setup( cls, vfiler ):
        cls.vfiler = vfiler



class KeyMapper_ListCtrl( KeyMapper ):
    """ ListCtrlのKeyMapper
    """
    @classmethod
    def setup( cls, vfiler ):
        cls.vfiler = vfiler

        from cmd_defs import *
        cls.add( CommandDef( KeyDef( ord("K") ), Cmd_CursorUp ) )
        cls.add( CommandDef( KeyDef( ord("J") ), Cmd_CursorDown ) )
        cls.add( CommandDef( KeyDef( ord("H") ), Cmd_CursorLeft ) )
        cls.add( CommandDef( KeyDef( ord("L") ), Cmd_CursorRight ) )

        cls.add( CommandDef( KeyDef( ord("U") ), Cmd_MoveDirUp ) )
        cls.add( CommandDef( KeyDef( ord("D") ), Cmd_MoveDirDown ) )

        cls.add( CommandDef( KeyDef( ord("E") ), Cmd_FileEdit ) )
        cls.add( CommandDef( KeyDef( ord("Q") ), Cmd_Quit ) )
        cls.add( CommandDef( KeyDef( ord("C") ), Cmd_Copy ) )
        cls.add( CommandDef( KeyDef( ord("M") ), Cmd_Move ) )
        #cls.add( CommandDef( KeyDef( ord("D") ), Cmd_Delete ) )
        cls.add( CommandDef( KeyDef( ord("/") ), Cmd_Search ) )
        cls.add( CommandDef( KeyDef( ord("G") ), Cmd_Grep ) )
        cls.add( CommandDef( KeyDef( ord("O") ), Cmd_SameDir ) )
        cls.add( CommandDef( KeyDef( wx.WXK_RETURN, KeyDef.MOD_KEY_CTRL ), Cmd_Open ) )


class KeyMapper_TextCtrl( KeyMapper ):
    """ TextCtrlのKeyMapper
    """
    pass


