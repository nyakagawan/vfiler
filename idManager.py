#!/usr/bin/python
# -*- coding: utf-8 -*-

class IdManager:
    @classmethod
    def frame( cls ):
        return 0

    @classmethod
    def listPanel( cls, paneKind ):
        return 10 + paneKind

    @classmethod
    def listCtrl( cls, paneKind ):
        return 15 + paneKind

    @classmethod
    def textCtrl( cls ):
        return 30

    @classmethod
    def listPanelSplitter( cls ):
        return 20

    @classmethod
    def textCtrlSplitter( cls ):
        return 40

