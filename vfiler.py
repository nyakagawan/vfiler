#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import wx

from listPanel import ListPanel
from textCtrl import TextCtrl
from define import Def
from keyMapper import KeyMapper_ListCtrl, KeyMapper_TextCtrl
from idManager import IdManager

class VFiler( wx.Frame ):
    def __init__( self, parent, id, title ):
        wx.Frame.__init__( self, parent, id, title )
        self.Center()

        self.Bind( wx.EVT_SIZE, self.OnSize )

        self.splitTextCtrl = None
        self.textCtrl = None
        self.splitListCtrl = None
        self.paneDict = {}
        self.paneDict[ Def.PANE_KIND_LEFT ] = None
        self.paneDict[ Def.PANE_KIND_RIGHT ] = None
        self.sizer = None
        self.focusedPane = None

        self.initGui()

        #size = wx.DisplaySize()
        size = (1000,400)
        self.SetSize( size )
        self.setDefaultSashPosition()

        self.Center()
        self.Show( True )

    def initGui( self ):
        # まずファイラー下のTextCtrlと上の縦Splitterを分けるSplitterを作る
        self.splitTextCtrl = wx.SplitterWindow( self, IdManager.textCtrlSplitter() )
        self.splitTextCtrl.SetMinimumPaneSize( 20 )

        self.textCtrl = TextCtrl( self.splitTextCtrl, IdManager.textCtrl(), self )
        self.textCtrl.SetSize( wx.Size(800,20) )

        splitListCtrlParent = self.splitTextCtrl

        # ListCtrlを分けるSplitterを作る
        self.splitListCtrl = wx.SplitterWindow( splitListCtrlParent, IdManager.listPanelSplitter() )
        self.splitListCtrl.SetMinimumPaneSize( 50 )

        paneLeft = self.initGuiPartOfList(
                self.splitListCtrl, IdManager.listPanel( Def.PANE_KIND_LEFT ), Def.PANE_KIND_LEFT )
        paneRight = self.initGuiPartOfList(
                self.splitListCtrl, IdManager.listPanel( Def.PANE_KIND_RIGHT ), Def.PANE_KIND_RIGHT )
        self.splitListCtrl.SplitVertically( paneLeft, paneRight )

        # 最初っからリストにフォーカスさせとく
        self.setFocusedPane( paneLeft )
        self.paneDict[ Def.PANE_KIND_LEFT ] = paneLeft
        self.paneDict[ Def.PANE_KIND_RIGHT ] = paneRight
        for pane in self.paneDict.values():
            pane.getListCtrl().changeDir( os.path.abspath( os.getcwd() ) )

        # 上のSplitterと下のTextCtrlをSplitte
        self.splitTextCtrl.SplitHorizontally( self.splitListCtrl, self.textCtrl )

        # Sizerを設定
        self.sizer = wx.BoxSizer( wx.VERTICAL )
        self.sizer.Add( self.splitTextCtrl, 1, wx.EXPAND )
        self.SetSizer( self.sizer )
        self.setDefaultSashPosition()


    def initGuiPartOfList( self, parent, guiId, paneKind ):
        panel = ListPanel( parent, guiId, paneKind, self )
        panel.initGui()
        return panel


    def getPane( self, paneKind ):
        return self.paneDict[ paneKind ]
    def setFocusedPane( self, pane ):
        self.focusedPane = pane
        self.focusedPane.SetFocus()
    def getFocusedPane( self ):
        return self.focusedPane
    def getUnFocusedPane( self ):
        for pane in self.paneDict.values():
            if pane!=self.focusedPane:
                return pane
        return None
    def getFocusedListCtrl( self ):
        return self.getFocusedPane().getListCtrl()
    def getUnFocusedListCtrl( self ):
        return self.getUnFocusedPane().getListCtrl()

    def getTextCtrl( self ):
        return self.textCtrl
    def focusSearchTextCtrl( self ):
        self.getTextCtrl().SetFocus()
        self.getTextCtrl().setMode( TextCtrl.MODE_SEARCH )
    def focusGrepTextCtrl( self ):
        self.getTextCtrl().SetFocus()
        self.getTextCtrl().setMode( TextCtrl.MODE_GREP )

    def updateFileList( self, paneKind ):
        self.getPane( paneKind ).getListCtrl().updateFileList()

    def updateFileListBoth( self ):
        self.updateFileList( Def.PANE_KIND_LEFT )
        self.updateFileList( Def.PANE_KIND_RIGHT )

    def setDefaultSashPosition( self ):
        size = self.GetSize()
        self.splitListCtrl.SetSashPosition( size.x / 2 )
        if self.splitTextCtrl:
            self.splitTextCtrl.SetSashPosition( size.y - 20 )

    def OnExit( self, e ):
        self.Close( True )

    def OnSize( self, event ):
        self.setDefaultSashPosition()
        event.Skip()


app = wx.App( 0 )
vfiler = VFiler( None, IdManager.frame(), "VFiler" )
KeyMapper_ListCtrl.setup( vfiler )
KeyMapper_TextCtrl.setup( vfiler )
app.SetTopWindow( vfiler )
app.MainLoop()






