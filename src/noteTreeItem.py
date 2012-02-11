#!/usr/bin/env python3

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class CommonItem(QTreeWidgetItem):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.setFlags(self.flags() | Qt.ItemIsEditable)
        self.setExpanded(True)

        self.key = ''

    def GetTitle(self):
        return self.text(0)
#        self.title = ''
#
#    def SetTitle(self, title):
#        self.title = title
#        self.setText(0, title)
#
#    def IsTitleChanged(self):
#        return self.title != self.text(0)

class NoteItem(CommonItem):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

class PageItem(CommonItem):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.setExpanded(False)

        self.editor = None
