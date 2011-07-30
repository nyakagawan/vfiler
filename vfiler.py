#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import wx

from listCtrl import ListCtrl
from textCtrl import TextCtrl
from define import Def
from keyMapper import KeyMapper_ListCtrl

ID_SPLITTER_LISTCTRL = 300
ID_SPLITTER_TEXTCTRL = 301
ID_SPLITTER_PATH_LABEL = 302
ID_LISTCTRL_LEFT = 500
ID_LISTCTRL_RIGHT = 501
ID_TEXTCTRL = 505

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
        self.listCtrl = ListCtrl( self, -1, self.paneKind, self.frame )
        vbox.Add( self.listCtrl, 1, wx.EXPAND )
        self.SetSizer( vbox )

    def getListCtrl( self ):
        return self.listCtrl

    def setPathText( self, text ):
        self.staticText.SetLabel( text )

class VFiler( wx.Frame ):
    def __init__( self, parent, id, title ):
        wx.Frame.__init__( self, parent, -1, title )
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
        self.splitTextCtrl = wx.SplitterWindow( self, ID_SPLITTER_TEXTCTRL )
        self.splitTextCtrl.SetMinimumPaneSize( 20 )

        self.textCtrl = TextCtrl( self.splitTextCtrl, ID_TEXTCTRL, self )
        self.textCtrl.SetSize( wx.Size(800,20) )

        splitListCtrlParent = self.splitTextCtrl

        # ListCtrlを分けるSplitterを作る
        self.splitListCtrl = wx.SplitterWindow( splitListCtrlParent, ID_SPLITTER_LISTCTRL )
        self.splitListCtrl.SetMinimumPaneSize( 50 )

        paneLeft = self.initGuiPartOfList(
                self.splitListCtrl, ID_LISTCTRL_LEFT, Def.PANE_KIND_LEFT )
        paneRight = self.initGuiPartOfList(
                self.splitListCtrl, ID_LISTCTRL_RIGHT, Def.PANE_KIND_RIGHT )
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
vfiler = VFiler( None, -1, "VFiler" )
KeyMapper_ListCtrl.setup( vfiler )
app.SetTopWindow( vfiler )
app.MainLoop()






