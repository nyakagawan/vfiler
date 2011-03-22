#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

class Util( object ):
    def __init__( self ):
        pass

    @classmethod
    def trace( cls, string ):
        """ デバッグ用のトレース。
            __debug__は起動オプション-Oを指定するとFalseになるらしい
        """
        if __debug__:
            print string

    @classmethod
    def info( cls, string ):
        """ 本番でもトレース。使うか？
        """
        print string



