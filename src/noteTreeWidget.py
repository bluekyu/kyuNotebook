#!/usr/bin/env python3

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class NoteTreeWidget(QTreeWidget):
    '''노트 트리를 위한 클래스'''

    NOTE_TYPE = 1001
    PAGE_TYPE = 1002
 
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderLabel(self.tr('이름'))

    def MakeNote(self, root, title, key):
        noteItem = QTreeWidgetItem(
                    root, [title], self.NOTE_TYPE)
        noteItem.setData(1, Qt.UserRole, key)
        noteItem.setExpanded(True)

        return noteItem

    def MakePage(self, root, title, key):
        pageItem = QTreeWidgetItem(
                    root, [title], self.PAGE_TYPE)
        pageItem.setData(1, Qt.UserRole, key)

        return pageItem

    def GetItemPathList(self):
        pathList = []
        currentItem = self.currentItem()
        while True:
            if currentItem.parent() is None:
                return pathList
            pathList.insert(0, currentItem.data(1, Qt.UserRole))
            currentItem = currentItem.parent()

    def CurrentNewNote(self, key):
        self.MakeNote(self.currentItem(), self.tr('새 노트'), key)

    def CurrentNewPage(self, key):
        self.MakePage(self.currentItem(), self.tr('새 페이지'), key)
