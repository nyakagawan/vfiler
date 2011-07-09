#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import wx

from listCtrl import ListCtrl
from textCtrl import TextCtrl
from define import Def

ID_SPLITTER_LISTCTRL = 300
ID_SPLITTER_TEXTCTRL = 301
ID_LISTCTRL_LEFT = 500
ID_LISTCTRL_RIGHT = 501
ID_TEXTCTRL = 505

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

        self.initGui()

        #size = wx.DisplaySize()
        size = (1000,400)
        self.SetSize( size )
        self.setDefaultSashPosition()

        self.Center()
        self.Show( True )

    def initGui( self, textCtrlClass=None ):
        # まずファイラー下のTextCtrlと上の縦Splitterを分けるSplitterを作る
        self.splitTextCtrl = wx.SplitterWindow( self, ID_SPLITTER_TEXTCTRL )
        self.splitTextCtrl.SetMinimumPaneSize( 20 )

        self.textCtrl = TextCtrl( self.splitTextCtrl, ID_TEXTCTRL, self )
        self.textCtrl.SetSize( wx.Size(800,20) )

        # ListCtrlを分けるSplitterを作る
        self.splitListCtrl = wx.SplitterWindow( self.splitTextCtrl, ID_SPLITTER_LISTCTRL )
        self.splitListCtrl.SetMinimumPaneSize( 50 )

        paneLeft = ListCtrl( self.splitListCtrl, ID_LISTCTRL_LEFT, Def.PANE_KIND_LEFT, self )
        paneRight = ListCtrl( self.splitListCtrl, ID_LISTCTRL_RIGHT, Def.PANE_KIND_RIGHT, self )
        self.splitListCtrl.SplitVertically( paneLeft, paneRight )

        # 上のSplitterと下のTextCtrlをSplitte
        self.splitTextCtrl.SplitHorizontally( self.splitListCtrl, self.textCtrl )

        # 最初っからリストにフォーカスさせとく
        self.setFocusedPane( paneLeft )
        self.paneDict[ Def.PANE_KIND_LEFT ] = paneLeft
        self.paneDict[ Def.PANE_KIND_RIGHT ] = paneRight

        # Sizerを設定
        self.sizer = wx.BoxSizer( wx.VERTICAL )
        self.sizer.Add( self.splitTextCtrl, 1, wx.EXPAND )
        self.SetSizer( self.sizer )


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

    def getTextCtrl( self ):
        return self.textCtrl

    def updateFileList( self, paneKind ):
        self.getPane( paneKind ).updateFileList()
    def updateFileListBoth( self ):
        self.updateFileList( Def.PANE_KIND_LEFT )
        self.updateFileList( Def.PANE_KIND_RIGHT )

    def setDefaultSashPosition( self ):
        size = self.GetSize()
        self.splitListCtrl.SetSashPosition( size.x / 2 )
        self.splitTextCtrl.SetSashPosition( size.y - 20 )

    def CreateWxToolBar( self ):
        tb = self.CreateToolBar( wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT )
        tb.AddSimpleTool( 10, wx.Bitmap( 'images/previous.png' ), 'Previous' )
        tb.AddSimpleTool( 20, wx.Bitmap( 'images/up.png' ), 'Up one directory' )
        tb.AddSimpleTool( 30, wx.Bitmap( 'images/home.png' ), 'Home' )
        tb.AddSimpleTool( 40, wx.Bitmap( 'images/refresh.png' ), 'Refresh' )
        tb.AddSeparator()
        tb.AddSimpleTool( 50, wx.Bitmap( 'images/write.png' ), 'Editor' )
        tb.AddSimpleTool( 60, wx.Bitmap( 'images/terminal.png' ), 'Terminal' )
        tb.AddSeparator()
        tb.AddSimpleTool( 70, wx.Bitmap( 'images/help.png' ), 'Help' )
        tb.Realize()

    def OnExit( self, e ):
        self.Close( True )

    def OnSize( self, event ):
        self.setDefaultSashPosition()
        event.Skip()


app = wx.App( 0 )
VFiler( None, -1, "VFiler" )
app.MainLoop()






