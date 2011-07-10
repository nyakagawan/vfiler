#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import wx
import time
import re

from util import Util
from element import *
from define import Def
from keyReader import KeyReader

class ListCtrl( wx.ListCtrl ):
    """ ファイルリストGUI
    """
    LIST_MODE_NORMAL = (1<<0)
    LIST_MODE_FILTERED = (1<<1)

    def __init__( self, parent, id, paneKind, frame ):
        wx.ListCtrl.__init__( self, parent, id, style=wx.LC_REPORT )
        self.paneKind = paneKind
        self.elemList = []
        self.frame = frame
        self.listMode = 0
        self.setListMode( ListCtrl.LIST_MODE_NORMAL )

        self.initGui()
        self.changeDir( os.path.abspath( os.getcwd() ) )
        self.Bind( wx.EVT_CHILD_FOCUS, self.OnChildFocus )

    def getFrame( self ):
        """ Frameオブジェクトを得る
        """
        #return self.GetParent().GetParent()
        return self.frame

    def setListMode( self, listMode ):
        Util.trace( "change list mode %d => %d" %(self.listMode, listMode) )
        self.listMode = listMode
    def getListMode( self ):
        return self.listMode

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
        self.Bind( wx.EVT_KEY_DOWN, self.OnKeyDown )

    def OnItemSelected( self, event ):
        #print "OnItemSelected !!!"
        pass

    def OnKeyDown( self, event ):
        """ キーダウンイベントハンドラ
        """
        #print "OnKeyDown !!!!" + str( event.GetKeyCode() )
        kr = KeyReader( event )
        self.moveDir( kr )
        self.moveCursor( kr )
        self.changeFocus( kr )
        self.executeCommand( kr )
        # ここでSkipをFalse（ほかにbindされた関数を呼ばない）にしないと
        # '/'押下でTextCtrlにフォーカスしたときにEVT_TEXTが発生して'/'が入力されてしまう
        # 理屈がいまいち分からんが、Skip(False)にしたらこれが無くなる。
        event.Skip( False )

    def moveDir( self, kr ):
        """ Key入力によってディレクトリを移動する
        """
        nextPath = ""
        if kr.moveDirUp():
            nextPath = self.curDir + "/.."
        elif kr.moveDirDown():
            nextPath = self.getItemAbsPath( self.GetFocusedItem() )
        if os.path.isdir( nextPath ):
            Util.trace( "moveDir %s -> %s" %(self.getCurDir(), nextPath) )
            nextPath = os.path.normpath( nextPath )
            self.changeDir( nextPath )

    def moveCursor( self, kr ):
        """ カーソル移動
        """
        nowSel = self.GetFirstSelected()
        itemCount = self.GetItemCount()
        if kr.cursorUp():
            self.Select( nowSel, False )
            nowSel = (nowSel-1) if nowSel>0 else itemCount-1
        elif kr.cursorDown():
            self.Select( nowSel, False )
            nowSel = (nowSel+1) % itemCount
        if nowSel!=-1:
            self.Select( nowSel )
            self.Focus( nowSel )

    def changeFocus( self, kr ):
        """ Key入力によって、フォーカスしているペインをかえる
        """
        changePane = Def.PANE_KIND_INVALID
        if kr.cursorLeft():
            changePane = Def.PANE_KIND_LEFT
        elif kr.cursorRight():
            changePane = Def.PANE_KIND_RIGHT
        if changePane!=Def.PANE_KIND_INVALID and self.paneKind!=changePane:
            self.getFrame().setFocusedPane( self.getFrame().getPane( changePane ) )

    def executeCommand( self, kr ):
        """ いろんなコマンドを実行
        """
        focusedItemIndex = self.GetFocusedItem()
        if kr.fileEdit():
            cmd = "mvim --remote-silent %s" %( self.getItemAbsPath( focusedItemIndex ) )
            Util.trace("file edit command( %s )" %(cmd) )
            os.system( cmd )
        elif kr.quit():
            self.getFrame().Close()
        elif kr.copy():
            self.copyElem()
        elif kr.move():
            Util.trace( "!!! not implement" )
        elif kr.delete():
            self.deleteElem()
        elif kr.search():
            self.searchElem()
        elif kr.grep():
            self.grepElem()
        elif kr.cancel():
            if self.getListMode()==ListCtrl.LIST_MODE_FILTERED:
                # ListModeがFilteredの時にキャンセルキー押されたら通常リストに戻す
                self.updateFileList()
                self.setListMode( ListCtrl.LIST_MODE_NORMAL )

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
        self.getFrame().focusSearchTextCtrl()

    def grepElem( self ):
        """ Grep
        """
        self.getFrame().focusGrepTextCtrl()

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

    def updateFileList( self, curDir=None, filterFmt=None ):
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
            if filterFmt!=None:
                p = re.compile( filterFmt, re.IGNORECASE )
                if not p.search( e ):
                    continue# マッチしなかったらフィルターする

            absPath = "%s/%s" %( curDir, e )
            if os.path.isdir( absPath ):
                #Util.trace( "add DIR " + e )
                elem = ElemDir( iFile, self, e )
            else:
                #Util.trace( "add FILE " + e )
                elem = ElemFile( iFile, self, e )
            elem.update()
            self.elemList.append( elem )
            iFile += 1

    def updateIncSearch( self, searchWord ):
        """ 検索ワードを受け取って、Incremental検索結果を更新
        """
        Util.trace( "search of " + searchWord )
        self.updateFileList( filterFmt=searchWord )
        self.setListMode( ListCtrl.LIST_MODE_FILTERED )




