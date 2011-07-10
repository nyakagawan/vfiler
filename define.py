#!/usr/bin/python
# -*- coding: utf-8 -*-

class Def:
    PANE_KIND_INVALID = -1
    PANE_KIND_LEFT = 0
    PANE_KIND_RIGHT = 1

    CORSOR_UP_KEYCODE = ord("K")
    CORSOR_DOWN_KEYCODE = ord("J")
    CORSOR_LEFT_KEYCODE = ord("H")
    CORSOR_RIGHT_KEYCODE = ord("L")

    MOVE_DIR_UP_KEYCODE = ord("U")
    MOVE_DIR_DOWN_KEYCODE = ord("D")

    FILE_EDIT_KEYCODE = ord("E")
    QUIT_KEYCODE = ord("Q")
    COPY_KEYCODE = ord("C")
    MOVE_KEYCODE = ord("M")
    DELETE_KEYCODE = ord("D")
    SEARCH_KEYCODE = ord("/")

    LIST_COL_INDEX_NAME = 0
    LIST_COL_INDEX_EXT = 1
    LIST_COL_INDEX_SIZE = 2
    LIST_COL_INDEX_MTIME = 3

    MTIME_FORMAT = '%Y-%m-%d %H:%M'

