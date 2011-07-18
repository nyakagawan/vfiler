#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import wx
import time

from util import Util
from element import *
from define import Def
from keyReader import KeyReader

class TextCtrl( wx.TextCtrl ):
    """ ファイルリストGUI
    """
    MODE_SEARCH = (1<<0)
    MODE_GREP = (1<<1)

    def __init__( self, parent, id, frame ):
        wx.TextCtrl.__init__( self, parent, id )
        self.frame = frame
        self.mode = TextCtrl.MODE_SEARCH
        self.Bind( wx.EVT_KEY_DOWN, self.OnKeyDown )
        self.Bind( wx.EVT_SET_FOCUS, self.OnFocus )

    def getFrame( self ):
        return self.frame

    def setMode( self, mode ):
        self.mode = mode
        self.Clear()

    def OnKeyDown( self, event ):
        """ キーダウンイベントハンドラ
        """
        kr = KeyReader( event )
        if kr.cancel():
            # ESC押されたらListCtrlにフォーカスを戻す
            self.getFrame().setFocusedPane( self.getFrame().getFocusedPane() )
        else:
            if self.mode==TextCtrl.MODE_SEARCH:
                # インクリメンタルサーチ結果を更新する
                self.EmulateKeyPress( event )
                if len( self.GetLineText(0) ):
                    self.getFrame().getFocusedPane().updateIncSearch( self.GetLineText(0) )
                return
            elif self.mode==TextCtrl.MODE_GREP:
                if kr.pressEnter():
                    # grepを行う
                    curDir = self.getFrame().getFocusedPane().getCurDir()
                    # まず処理するファイル総数を計測
                    totalFileCount = 0
                    for path,dirs,files in os.walk( curDir ):
                        for f in files:
                            totalFileCount += 1

                    # プログレスダイアログを生成
                    pd = wx.ProgressDialog(
                            title="--- GREP ---",
                            message="This is a Grep!",
                            maximum=totalFileCount,
                            parent=self.getFrame(),
                            style=wx.PD_AUTO_HIDE|wx.PD_APP_MODAL|wx.PD_SMOOTH|wx.PD_ESTIMATED_TIME
                            )
                    pd.ShowModal()

                    """ このあたり作りかけ。Grepよりほかの実装項目を優先
                    """
                    # ファイル舞にGrep処理
                    procedFileCount = 0
                    for path,dirs,files in os.walk( curDir ):
                        for f in files:
                            print os.path.join( path, f )
                            procedFileCount += 1
                            pd.Update( procedFileCount )

                    pd.Update( totalFileCount )
                    pd.Destroy()
        event.Skip()

    def OnFocus( self, event ):
        event.Skip()

