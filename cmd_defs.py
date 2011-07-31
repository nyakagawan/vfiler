#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import wx

from define import Def
from util import Util
from commander import Commander, CommandDef
from listCtrl import ListCtrl
from textCtrl import TextCtrl

def Cmd_CursorUp( vfiler, event ):
    listCtrl = vfiler.getFocusedListCtrl()
    listCtrl.moveCursor( ListCtrl.MOVE_CURSOR_UP )

def Cmd_CursorDown( vfiler, event ):
    listCtrl = vfiler.getFocusedListCtrl()
    listCtrl.moveCursor( ListCtrl.MOVE_CURSOR_DOWN )

def Cmd_CursorLeft( vfiler, event ):
    listCtrl = vfiler.getFocusedListCtrl()
    listCtrl.changeFocus( Def.PANE_KIND_LEFT )

def Cmd_CursorRight( vfiler, event ):
    listCtrl = vfiler.getFocusedListCtrl()
    listCtrl.changeFocus( Def.PANE_KIND_RIGHT )

def Cmd_MoveDirUp( vfiler, event ):
    listCtrl = vfiler.getFocusedListCtrl()
    listCtrl.moveDir( ListCtrl.MOVE_DIR_UP )

def Cmd_MoveDirDown( vfiler, event ):
    listCtrl = vfiler.getFocusedListCtrl()
    listCtrl.moveDir( ListCtrl.MOVE_DIR_DOWN )

def Cmd_FileEdit( vfiler, event ):
    listCtrl = vfiler.getFocusedListCtrl()
    focusedItemIndex = listCtrl.GetFocusedItem()
    cmd = "mvim --remote-silent %s" %( listCtrl.getItemAbsPath( focusedItemIndex ) )
    Util.trace("file edit command( %s )" %(cmd) )
    os.system( cmd )

def Cmd_Quit( vfiler, event ):
    vfiler.Close()

def Cmd_Copy( vfiler, event ):
    """ 選択中エレメントを非フォーカスペインのディレクトリへコピーする
    """
    listCtrl = vfiler.getFocusedListCtrl()
    focusedItemIndex = listCtrl.GetFocusedItem()
    if listCtrl.getElemCount() and focusedItemIndex>=0:
        forcusedElem = listCtrl.getElem( focusedItemIndex )
        srcPath = forcusedElem.getAbsPath()
        destPath = None
        unfocusedPane = vfiler.getUnFocusedPane()
        if unfocusedPane:
            destPath = unfocusedPane.getCurDir()
        if destPath and destPath!=os.path.dirname( srcPath ):
            cmd = "cp -rf %s %s" %( srcPath, destPath )
            Util.trace( cmd )
            os.system( cmd )

def Cmd_Move( vfiler, event ):
    Util.trace( "NOT IMPLEMENT!" )

def Cmd_Delete( vfiler, event ):
    """ 選択中エレメントをファイルリストから削除する
    """
    listCtrl = vfiler.getFocusedListCtrl()
    focusedItemIndex = listCtrl.GetFocusedItem()
    if listCtrl.getElemCount() and focusedItemIndex>=0:
        forcusedElem = listCtrl.getElem( focusedItemIndex )
        # elemListから削除
        listCtrl.elemList.remove( forcusedElem )
        # GUIから削除
        listCtrl.DeleteItem( focusedItemIndex )
        # FileSystemから削除
        cmd = "rm -rf %s" %( forcusedElem.getAbsPath() )
        Util.trace( cmd )
        os.system( cmd )

def Cmd_Search( vfiler, event ):
    """ インクリメンタルサーチ
    """
    vfiler.focusSearchTextCtrl()

def Cmd_Grep( vfiler, event ):
    """ Grep
    """
    vfiler.focusGrepTextCtrl()

def Cmd_SameDir( vfiler, event ):
    """ フォーカスのないリストのディレクトリを、フォーカスのあるリストと一緒にする
    """
    listCtrl = vfiler.getFocusedListCtrl()
    dirToChange = listCtrl.getCurDir()
    vfiler.getUnFocusedPane().changeDir( dirToChange )

def Cmd_Open( vfiler, event ):
    """ 関連づけられたプログラムでファイルを開く
    """
    listCtrl = vfiler.getFocusedListCtrl()
    focusedItemIndex = listCtrl.GetFocusedItem()
    cmd = "open %s" %( listCtrl.getItemAbsPath( focusedItemIndex ) )
    Util.trace( cmd )
    os.system( cmd )




