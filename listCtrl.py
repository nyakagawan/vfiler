#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import wx
import time
import re
import threading

from util import Util
from element import *
from define import Def
from keyReader import KeyReader
from intervalTimer import IntervalTimer
from dirCheck import DirCheck

class ListCtrl( wx.ListCtrl ):
    """ ファイルリストGUI
    """
    LIST_MODE_NORMAL = (1<<0)
    LIST_MODE_FILTERED = (1<<1)

    def __init__( self, parent, id, paneKind, frame ):
        wx.ListCtrl.__init__( self, parent, id, style=wx.LC_REPORT | wx.EXPAND )
        self.paneKind = paneKind
        self.elemList = []
        self.frame = frame
        self.listMode = 0
        self.setListMode( ListCtrl.LIST_MODE_NORMAL )

        self.initGui()
        self.Bind( wx.EVT_CHILD_FOCUS, self.OnChildFocus )

        self.updateTimer = IntervalTimer( 1, self.updateTimerCallback )
        self.updateTimer.start()

        self.checkDir = None

    def getFrame( self ):
        """ Frameオブジェクトを得る
        """
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
            このイベントは（何もしない場合でも）Skip()せずにフックする必要がある
        """
        if self.GetSelectedItemCount()==0 and len( self.elemList ):
            # フォーカスがあるときに常に項目を選択状態にするため、Select
            self.Select( 0, True )

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
        from keyMapper import KeyMapper_ListCtrl as KMap
        # マッピングされた各種コマンドの実行
        KMap.execute( event )
        # キャンセルキーが押されたときの処理
        if KMap.isCancel( event ):
            if self.getListMode()==ListCtrl.LIST_MODE_FILTERED:
                # ListModeがFilteredの時にキャンセルキー押されたら通常リストに戻す
                self.updateFileList()
                self.setListMode( ListCtrl.LIST_MODE_NORMAL )
        # ここでSkipをFalse（ほかにbindされた関数を呼ばない）にしないと
        # '/'押下でTextCtrlにフォーカスしたときにEVT_TEXTが発生して'/'が入力されてしまう
        # 理屈がいまいち分からんが、Skip(False)にしたらこれが無くなる。
        event.Skip( False )

    MOVE_DIR_UP =(1<<0)
    MOVE_DIR_DOWN =(1<<1)
    def moveDir( self, moveDirDirection ):
        """ Key入力によってディレクトリを移動する
        """
        nextPath = ""
        if moveDirDirection==self.MOVE_DIR_UP:
            nextPath = self.curDir + "/.."
        elif moveDirDirection==self.MOVE_DIR_DOWN:
            nextPath = self.getItemAbsPath( self.GetFocusedItem() )
        if os.path.isdir( nextPath ):
            Util.trace( "moveDir %s -> %s" %(self.getCurDir(), nextPath) )
            nextPath = os.path.normpath( nextPath )
            self.changeDir( nextPath )

    MOVE_CURSOR_UP = (1<<0)
    MOVE_CURSOR_DOWN = (1<<1)
    def moveCursor( self, moveCursorDirection ):
        """ カーソル移動
        """
        nowSel = self.GetFirstSelected()
        itemCount = self.GetItemCount()
        if not itemCount:
            return
        if moveCursorDirection==self.MOVE_CURSOR_UP:
            self.Select( nowSel, False )
            nowSel = (nowSel-1) if nowSel>0 else itemCount-1
        elif moveCursorDirection==self.MOVE_CURSOR_DOWN:
            self.Select( nowSel, False )
            nowSel = (nowSel+1) % itemCount
        if nowSel!=-1:
            self.Select( nowSel )
            self.Focus( nowSel )

    def changeFocus( self, paneKind ):
        """ Key入力によって、フォーカスしているペインをかえる
        """
        changePane = paneKind
        if changePane!=Def.PANE_KIND_INVALID and self.paneKind!=changePane:
            changePaneCtrl = self.getFrame().getPane( changePane )
            self.getFrame().setFocusedPane( changePaneCtrl )

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
            #self.getFrame().updateFileListBoth()
    
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
            self.dirChecker = DirCheck( path )
            self.getFrame().getPane( self.paneKind ).setPathText( path )

  
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
        # ディレクトリ群、ファイル群の順番にソート
        dirInfoList = []
        fileInfoList = []
        for e in listdir:
            info = {}
            if filterFmt!=None:
                p = re.compile( filterFmt, re.IGNORECASE )
                if not p.search( e ):
                    continue# マッチしなかったらフィルターする

            info["name"] = e
            absPath = "%s/%s" %( curDir, e )
            if os.path.isdir( absPath ):
                info["isDir"] = True
                dirInfoList.append( info )
            else:
                info["isDir"] = False
                fileInfoList.append( info )


        infoList = dirInfoList + fileInfoList
        # リストに追加
        iFile = 0
        for info in infoList:
            if info["isDir"]:
                #Util.trace( "add DIR " + e )
                elem = ElemDir( iFile, self, info["name"] )
            else:
                #Util.trace( "add FILE " + e )
                elem = ElemFile( iFile, self, info["name"] )
            elem.update()
            self.elemList.append( elem )
            iFile += 1

        # フォーカスがあるときに常に項目を選択状態にするため、Select
        if len( self.elemList ):
            self.Select( 0, True )

    def updateIncSearch( self, searchWord ):
        """ 検索ワードを受け取って、Incremental検索結果を更新
        """
        Util.trace( "search of " + searchWord )
        self.updateFileList( filterFmt=searchWord )
        self.setListMode( ListCtrl.LIST_MODE_FILTERED )

    def updateTimerCallback( self ):
        """ 一定間隔でコールバックされる。ディレクトリ監視状態などをチェック
        """
        if self.dirChecker and self.dirChecker.isChanged():
            self.updateFileList()
            self.dirChecker.offChangeFlag()




