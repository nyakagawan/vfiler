#!/usr/bin/python
# -*- coding: utf-8 -*-

class Def:
    PANE_KIND_INVALID = -1
    PANE_KIND_LEFT = 0
    PANE_KIND_RIGHT = 1

    CORSOR_UP_KEYCODE = ord("k")
    CORSOR_DOWN_KEYCODE = ord("j")
    CORSOR_LEFT_KEYCODE = ord("h")
    CORSOR_RIGHT_KEYCODE = ord("l")

    MOVE_DIR_UP_KEYCODE = ord("u")
    MOVE_DIR_DOWN_KEYCODE = ord("d")

    FILE_EDIT_KEYCODE = ord("e")
    CANCEL_KEYCODE = ord("q")
    COPY_KEYCODE = ord("c")
    MOVE_KEYCODE = ord("m")

    LIST_COL_INDEX_NAME = 0
    LIST_COL_INDEX_EXT = 1
    LIST_COL_INDEX_SIZE = 2
    LIST_COL_INDEX_MTIME = 3

    MTIME_FORMAT = '%Y-%m-%d %H:%M'

