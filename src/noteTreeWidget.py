#!/usr/bin/env python3

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class NoteTreeWidget(QTreeWidget):
    '''노트 트리를 위한 클래스'''

    DIR_TYPE = 1001
    NOTE_TYPE = 1002
    PAGE_TYPE = 1003
 
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderLabel(self.tr('이름'))

    def NewDir(self):
        currentDir = self.currentItem()
        dirItem = QTreeWidgetItem(
                    currentDir, [self.tr('새 폴더')], self.DIR_TYPE)
        dirItem.setExpanded(True)

    def NewNote(self):
        currentDir = self.currentItem()
        noteItem = QTreeWidgetItem(
                    currentDir, [self.tr('새 노트')], self.NOTE_TYPE)
        noteItem.setExpanded(True)

    def NewPage(self):
        currentNote = self.currentItem()
        pageItem = QTreeWidgetItem(
                    currentNote, [self.tr('새 페이지')], self.PAGE_TYPE)
