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

    def NewNote(self, key):
        currentDir = self.currentItem()
        noteItem = QTreeWidgetItem(
                    currentDir, [self.tr('새 노트')], self.NOTE_TYPE)
        noteItem.setData(1, Qt.UserRole, key)
        noteItem.setExpanded(True)

    def NewPage(self):
        currentNote = self.currentItem()
        pageItem = QTreeWidgetItem(
                    currentNote, [self.tr('새 페이지')], self.PAGE_TYPE)

    def GetItemPathList(self):
        pathList = []
        currentItem = self.currentItem()
        while True:
            if currentItem.parent() is None:
                return pathList
            pathList.insert(0, currentItem.data(1, Qt.UserRole))
            currentItem = currentItem.parent()

