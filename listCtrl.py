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
    def __init__( self, parent, id, paneKind, frame ):
        wx.ListCtrl.__init__( self, parent, id, style=wx.LC_REPORT )
        self.paneKind = paneKind
        self.elemList = []
        self.frame = frame

        self.initGui()
        self.changeDir( os.path.abspath( os.getcwd() ) )
        self.Bind( wx.EVT_CHILD_FOCUS, self.OnChildFocus )

    def getFrame( self ):
        """ Frameオブジェクトを得る
        """
        #return self.GetParent().GetParent()
        return self.frame

    def getCurDir( self ):
        return self.curDir

    def OnChildFocus( self, event ):
        """ http://d.hatena.ne.jp/h1mesuke/20090429/p1 この現象に対応するため
        """
        pass

    def getElemList( self ):
        return self.elemList
    def getElemCount( self ):
        return len( self.getElemList() )
    def getElem( self, index ):
        if index<self.getElemCount():
            return self.getElemList()[ index ]
        assert False, "elem list range over %d" %( index )

    def initGui( self ):
        self.InsertColumn( 0, 'Name' )
        self.InsertColumn( 1, 'Ext' )
        self.InsertColumn( 2, 'Size', wx.LIST_FORMAT_RIGHT )
        self.InsertColumn( 3, 'Modified' )

        self.SetColumnWidth( 0, 200 )
        self.SetColumnWidth( 1, 70 )
        self.SetColumnWidth( 2, 100 )
        self.SetColumnWidth( 3, 140 )

        self.SetBackgroundColour( BG_COLOR )

        self.Bind( wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected )
        self.Bind( wx.EVT_LIST_KEY_DOWN, self.OnKeyDown )

    def OnItemSelected( self, event ):
        #print "OnItemSelected !!!"
        pass

    def OnKeyDown( self, event ):
        """ キーダウンイベントハンドラ
        """
        #print "OnKeyDown !!!!" + str( event.GetKeyCode() )
        keycode = event.GetKeyCode()
        self.moveDir( keycode )
        self.moveCursor( keycode )
        self.changeFocus( keycode )
        self.executeCommand( keycode )

    def moveDir( self, keycode ):
        """ Key入力によってディレクトリを移動する
        """
        nextPath = ""
        if keycode==Def.MOVE_DIR_UP_KEYCODE:
            nextPath = self.curDir + "/.."
        if keycode==Def.MOVE_DIR_DOWN_KEYCODE:
            nextPath = self.getItemAbsPath( self.GetFocusedItem() )
        if os.path.isdir( nextPath ):
            Util.trace( "moveDir %s -> %s" %(self.getCurDir(), nextPath) )
            nextPath = os.path.normpath( nextPath )
            self.changeDir( nextPath )

    def moveCursor( self, keycode ):
        """ カーソル移動
        """
        nowSel = self.GetFirstSelected()
        itemCount = self.GetItemCount()
        if keycode==Def.CORSOR_UP_KEYCODE:
            self.Select( nowSel, False )
            nowSel = (nowSel-1) if nowSel>0 else itemCount-1
        elif keycode==Def.CORSOR_DOWN_KEYCODE:
            self.Select( nowSel, False )
            nowSel = (nowSel+1) % itemCount
        if nowSel!=-1:
            self.Select( nowSel )
            self.Focus( nowSel )

    def changeFocus( self, keycode ):
        """ Key入力によって、フォーカスしているペインをかえる
        """
        changePane = Def.PANE_KIND_INVALID
        if keycode==Def.CORSOR_LEFT_KEYCODE:
            changePane = Def.PANE_KIND_LEFT
        elif keycode==Def.CORSOR_RIGHT_KEYCODE:
            changePane = Def.PANE_KIND_RIGHT
        if changePane!=Def.PANE_KIND_INVALID and self.paneKind!=changePane:
            self.getFrame().setFocusedPane( self.getFrame().getPane( changePane ) )

    def executeCommand( self, keycode ):
        """ いろんなコマンドを実行
        """
        focusedItemIndex = self.GetFocusedItem()
        if keycode==Def.FILE_EDIT_KEYCODE:
            cmd = "mvim --remote-silent %s" %( self.getItemAbsPath( focusedItemIndex ) )
            Util.trace("file edit command( %s )" %(cmd) )
            os.system( cmd )
        elif keycode==Def.QUIT_KEYCODE:
            self.getFrame().Close()
        elif keycode==Def.COPY_KEYCODE:
            self.copyElem()
        elif keycode==Def.MOVE_KEYCODE:
            Util.trace( "!!! not implement" )
        elif keycode==Def.DELETE_KEYCODE:
            self.deleteElem()
        elif keycode==Def.SEARCH_KEYCODE:
            self.searchElem()

    def copyElem( self ):
        """ 選択中エレメントを非フォーカスペインのディレクトリへコピーする
        """
        focusedItemIndex = self.GetFocusedItem()
        if self.getElemCount() and focusedItemIndex>=0:
            forcusedElem = self.getElem( focusedItemIndex )
            srcPath = forcusedElem.getAbsPath()
            destPath = None
            unfocusedPane = self.getFrame().getUnFocusedPane()
            if unfocusedPane:
                destPath = unfocusedPane.getCurDir()
            if destPath and destPath!=os.path.dirname( srcPath ):
                cmd = "cp -rf %s %s" %( srcPath, destPath )
                Util.trace( cmd )
                os.system( cmd )

    def deleteElem( self ):
        """ 選択中エレメントをファイルリストから削除する
        """
        focusedItemIndex = self.GetFocusedItem()
        if self.getElemCount() and focusedItemIndex>=0:
            forcusedElem = self.getElem( focusedItemIndex )
            # elemListから削除
            self.elemList.remove( forcusedElem )
            # GUIから削除
            self.DeleteItem( focusedItemIndex )
            # FileSystemから削除
            cmd = "rm -rf %s" %( forcusedElem.getAbsPath() )
            Util.trace( cmd )
            os.system( cmd )
            # 両方のペインのファイルリスト更新
            self.getFrame().updateFileListBoth()
    
    def searchElem( self ):
        """ インクリメンタルサーチ
        """
        self.getFrame().getTextCtrl().SetFocus()

    def getItemAbsPath( self, itemId ):
        """ Itemの絶対パスを取得
        """
        elem = self.getElem( itemId )
        return elem.getAbsPath()

    def changeDir( self, path ):
        """ カレントディレクトリを移動
        """
        path = os.path.abspath( path )
        if os.path.isdir( path ):
            self.curDir = path
            self.updateFileList( self.curDir )
  
    def removeFileList( self ):
        """ ファイルリストを削除
        """
        Util.trace( "removeFileList" )
        self.DeleteAllItems()

    def updateFileList( self, curDir=None ):
        """ ファイルリストを更新
        """
        if curDir==None:
            curDir = self.curDir
        self.removeFileList()
        self.elemList = []

        Util.trace( "curDir [%s] updateFileList" %(curDir) )
        listdir = os.listdir( curDir )
        iFile = 0
        for e in listdir:
            absPath = "%s/%s" %( curDir, e )
            if os.path.isdir( absPath ):
                Util.trace( "add DIR " + e )
                elem = ElemDir( iFile, self, e )
            else:
                Util.trace( "add FILE " + e )
                elem = ElemFile( iFile, self, e )
            elem.update()
            self.elemList.append( elem )
            iFile += 1




