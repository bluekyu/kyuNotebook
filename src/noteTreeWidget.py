#!/usr/bin/env python3

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class NoteTreeWidget(QTreeWidget):
    '''노트 트리를 위한 클래스'''

    NOTE_TYPE = 1001
    PAGE_TYPE = 1002
 
    def __init__(self, contextAction=[], parent=None):
        super().__init__(parent)
        self.setHeaderLabel(self.tr('이름'))
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.addActions(contextAction)
        
    def MakeNote(self, root, title, key):
        self.blockSignals(True)
        noteItem = QTreeWidgetItem(
                    root, [title], self.NOTE_TYPE)
        noteItem.setData(1, Qt.UserRole, key)
        noteItem.setExpanded(True)
        noteItem.setFlags(noteItem.flags() | Qt.ItemIsEditable)
        self.blockSignals(False)

        return noteItem

    def MakePage(self, root, title, key):
        self.blockSignals(True)
        pageItem = QTreeWidgetItem(
                    root, [title], self.PAGE_TYPE)
        pageItem.setData(1, Qt.UserRole, key)
        pageItem.setFlags(pageItem.flags() | Qt.ItemIsEditable)
        self.blockSignals(False)

        return pageItem

    def GetItemPathList(self, item):
        pathList = []
        while True:
            if item.parent() is None:
                return pathList
            pathList.insert(0, item.data(1, Qt.UserRole))
            item = item.parent()

    def GetCurrentItemPathList(self):
        return self.GetItemPathList(self.currentItem())

    def CurrentNewNote(self, key):
        return self.MakeNote(self.currentItem(), self.tr('새 노트'), key)

    def CurrentNewPage(self, key):
        return self.MakePage(self.currentItem(), self.tr('새 페이지'), key)

    def EditTitle(self):
        self.editItem(self.currentItem())
