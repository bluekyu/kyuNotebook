#!/usr/bin/env python3

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class TextEditor(QTextEdit):
    def __init__(self, item=None, path=None, parent=None):
        super().__init__(parent)

        self.changed = False
        self.path = path
        self.item = item

        self.connect(self, SIGNAL('textChanged()'), self.Changed)

        self.Load()

    def Changed(self):
        self.changed = True

    def CloseRequest(self):
        if self.changed:
            answer = QMessageBox.question(self, self.tr('페이지 저장'), 
                self.tr('"{0}" 페이지를 저장하시겠습니까?').format(
                    self.item.title),
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

            if answer == QMessageBox.Cancel:
                return False
            elif answer == QMessageBox.Yes:
                self.Save()

        return True

    def Load(self):
        pageFile = open(self.path, 'r')
        self.setHtml(pageFile.read())
        pageFile.close()
        self.changed = False

    def Save(self):
        self.setDocumentTitle(self.item.title)
        pageFile = open(self.path, 'w')
        pageFile.write(self.toHtml())
        pageFile.close()
        self.changed = False
