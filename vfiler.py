#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import wx

from listCtrl import ListCtrl
from define import Def

ID_BUTTON = 100
ID_EXIT = 200
ID_SPLITTER = 300

class VFiler( wx.Frame ):
    def __init__( self, parent, id, title ):
        wx.Frame.__init__( self, parent, -1, title )
        self.Center()

        self.splitter = wx.SplitterWindow( self, ID_SPLITTER, style=wx.SP_BORDER )
        self.splitter.SetMinimumPaneSize( 50 )

        paneLeft = ListCtrl( self.splitter, -1, Def.PANE_KIND_LEFT )
        paneRight = ListCtrl( self.splitter, -1, Def.PANE_KIND_RIGHT )
        self.splitter.SplitVertically( paneLeft, paneRight )

        # 最初っからリストにフォーカスさせとく
        paneLeft.SetFocus()
        self.paneDict = {}
        self.paneDict[ Def.PANE_KIND_LEFT ] = paneLeft
        self.paneDict[ Def.PANE_KIND_RIGHT ] = paneRight
        
        self.Bind( wx.EVT_SIZE, self.OnSize )
        self.Bind( wx.EVT_SPLITTER_DCLICK, self.OnDoubleClick, id=ID_SPLITTER )

        self.CreateWxMenu()

        self.sizer = wx.BoxSizer( wx.VERTICAL )
        self.sizer.Add( self.splitter, 1, wx.EXPAND )
        #self.sizer.Add( self.sizer2, 0, wx.EXPAND )
        self.SetSizer( self.sizer )

        #size = wx.DisplaySize()
        size = (800,400)
        self.SetSize( size )

        self.sb = self.CreateStatusBar()
        self.sb.SetStatusText( os.getcwd() )
        self.Center()
        self.Show( True )

    def getPane( self, paneKind ):
        return self.paneDict[ paneKind ]
    def getFocusedPane( self ):
        focusedItem = self.FindFocus()
        if focusedItem in self.paneDict.values():
            return focusedItem
        return None
    def getUnFocusedPane( self ):
        focusedPane = self.getFocusedPane()
        for pane in self.paneDict.values():
            if pane!=focusedPane:
                return pane
        return None

    def CreateWxMenu( self ):
        filemenu = wx.Menu()
        filemenu.Append( ID_EXIT, "E&xit", "Terminate the program" )
        editmenu = wx.Menu()
        netmenu = wx.Menu()
        showmenu = wx.Menu()
        configmenu = wx.Menu()
        helpmenu = wx.Menu()

        menuBar = wx.MenuBar()
        menuBar.Append( filemenu, "&File" )
        menuBar.Append( editmenu, "&Edit" )
        menuBar.Append( netmenu, "&Net" )
        menuBar.Append( showmenu, "&Show" )
        menuBar.Append( configmenu, "&Config" )
        menuBar.Append( helpmenu, "&Help" )
        self.SetMenuBar( menuBar )
        self.Bind( wx.EVT_MENU, self.OnExit, id=ID_EXIT )

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

    def CreateWxFunctionButton( self ):
        self.sizer2 = wx.BoxSizer( wx.HORIZONTAL )

        button1 = wx.Button( self, ID_BUTTON + 1, "F3 View" )
        button2 = wx.Button( self, ID_BUTTON + 2, "F4 Edit" )
        button3 = wx.Button( self, ID_BUTTON + 3, "F5 Copy" )
        button4 = wx.Button( self, ID_BUTTON + 4, "F6 Move" )
        button5 = wx.Button( self, ID_BUTTON + 5, "F7 Mkdir" )
        button6 = wx.Button( self, ID_BUTTON + 6, "F8 Delte" )
        button7 = wx.Button( self, ID_BUTTON + 7, "F9 Rename" )
        button8 = wx.Button( self, ID_EXIT, "F10 Quit" )

        self.sizer2.Add( button1, 1, wx.EXPAND )
        self.sizer2.Add( button2, 1, wx.EXPAND )
        self.sizer2.Add( button3, 1, wx.EXPAND )
        self.sizer2.Add( button4, 1, wx.EXPAND )
        self.sizer2.Add( button5, 1, wx.EXPAND )
        self.sizer2.Add( button6, 1, wx.EXPAND )
        self.sizer2.Add( button7, 1, wx.EXPAND )
        self.sizer2.Add( button8, 1, wx.EXPAND )

        self.Bind( wx.EVT_BUTTON, self.OnExit, id=ID_EXIT )

    def OnExit( self, e ):
        self.Close( True )

    def OnSize( self, event ):
        size = self.GetSize()
        self.splitter.SetSashPosition( size.x / 2 )
        self.sb.SetStatusText( os.getcwd() )
        event.Skip()

    def OnDoubleClick( self, event ):
        size = self.GetSize()
        self.splitter.SetSashPosition( size.x / 2 )


app = wx.App( 0 )
VFiler( None, -1, "VFiler" )
app.MainLoop()






