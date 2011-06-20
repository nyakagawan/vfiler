#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import wx
import time

from util import Util
from define import Def

BG_COLOR        = '#191970'
ITEM_BG_COLOR   = '#191970'
ITEM_TEXT_COLOR = '#ffc0cb'
ITEM_TEXT_COLOR_DIR = '#66cdaa'


class ElemBase( object ):
    """ エレメント基本
    """
    def __init__( self, listCtrl ):
        self.index_ = 0
        self.name_ = ""
        self.size_ = 0
        self.mtime_ = 0
        self.bgColor_ = ITEM_BG_COLOR
        self.textColor_ = ITEM_TEXT_COLOR
        self.listCtrl_ = listCtrl

    def setIndex( self, index ):
        self.index_ = index
    def setName( self, name ):
        self.name_ = name
    def setSize( self, size ):
        self.size_ = size
    def setMtime( self, time ):
        self.mtime_ = time
    def setBgColor( self, color ):
        self.bgColor_ = color
    def setTextColor( self, color ):
        self.textColor_ = color
    def setListCtrl( self, listCtrl ):
        self.listCtrl_ = listCtrl

    def getListCtrl( self ):
        return self.listCtrl_

    def insertStringItem( self, index, string ):
        self.getListCtrl().InsertStringItem( index, string )
    def setStringItem( self, index, column, string ):
        self.getListCtrl().SetStringItem( index, column, string )
    def setItemBackgroundColour( self, index, color ):
        self.getListCtrl().SetItemBackgroundColour( index, color )
    def setItemTextColour( self, index, color ):
        self.getListCtrl().SetItemTextColour( index, color )

    def _dumpVariable( self ):
        Util.trace( "---------------------------" )
        Util.trace( "index:   " + str( self.index_ ) )
        Util.trace( "name:    " + str( self.name_ ) )
        #Util.trace( "ext:     " + str( self.ext_ ) )
        Util.trace( "mtime:   " + str( self.mtime_ ) )
        Util.trace( "bgColor: " + str( self.bgColor_ ) )

    def update( self ):
        """ エレメントの内容をGUIに反映する
        """
        self.insertStringItem( self.index_, self.name_ )
        self.setStringItem( self.index_, Def.LIST_COL_INDEX_SIZE, str( self.size_ ) + 'B' )
        self.setStringItem( self.index_, Def.LIST_COL_INDEX_MTIME, time.strftime( Def.MTIME_FORMAT, time.localtime( self.mtime_ ) ) )
        self.setItemBackgroundColour( self.index_, self.bgColor_ )
        self.setItemTextColour( self.index_, self.textColor_ )
        #self._dumpVariable()


class ElemFile( ElemBase ):
    """ ファイルエレメント
    """

    def __init__( self, index, listCtrl, fileName ):
        ElemBase.__init__( self, listCtrl )

        self.ext_ = ""
        self.setIndex( index )
        ( name, ext ) = os.path.splitext( fileName )
        self.setName( name )
        self.setExt( ext[ 1: ] )
        self.setSize( os.path.getsize( fileName ) )
        self.setMtime( os.path.getmtime( fileName ) )
        self.setBgColor( ITEM_BG_COLOR )
        self.setTextColor( ITEM_TEXT_COLOR )

    def setExt( self, ext ):
        self.ext_ = ext

    def update( self ):
        ElemBase.update( self )
        self.setStringItem( self.index_, Def.LIST_COL_INDEX_EXT, self.ext_ )

class ElemDir( ElemBase ):
    """ ディレクトリエレメント
    """
    def __init__( self, index, listCtrl, dirName ):
        ElemBase.__init__( self, listCtrl )

        self.setIndex( index )
        self.setName( dirName )
        self.setSize( os.path.getsize( dirName ) )
        self.setMtime( os.path.getmtime( dirName ) )
        self.setBgColor( ITEM_BG_COLOR )
        self.setTextColor( ITEM_TEXT_COLOR_DIR )
        self.setListCtrl( listCtrl )

#        self.setElemList( [] )
#        self.setSelectList( [] )
#        self.setCursorElem( self.getElem( 0 ) )

#    def setElemList( self, elemList ):
#        self.elemList_ = elemList
#    def setSelectList( self, elemList ):
#        self.selectList_ = elemList
#    def setCursorElem( self, elem ):
#        self.cursorElem_ = elem
#
#    def clear( self ):
#        del self.elemList_[:]
#
#    def getElem( self, index ):
#        if index<len( elemList_ ):
#            return elemList_[ index ]
#        return None
#
#    def addElem( self, elemFile ):
#        """ ファイルエレメントの追加
#        """
#        self.elemList_.append( elemFile )
#
#    def removeElem( self, elem ):
#        try:
#            self.elemList_.remove( elem )
#        except ValueError:
#            Util.trace( "can't remove elem" )



