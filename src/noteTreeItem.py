#!/usr/bin/env python3

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class CommonItem(QTreeWidgetItem):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.title = self.text(0)
        self.key = ''

        self.setFlags(self.flags() | Qt.ItemIsEditable)
        self.setExpanded(True)

    def IsTitleChanged(self):
        if self.title == self.text(0):
            return False
        else:
            self.title = self.text(0)
            return True

class NoteItem(CommonItem):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

class PageItem(CommonItem):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.setExpanded(False)

        self.editor = None
