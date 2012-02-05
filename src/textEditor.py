#!/usr/bin/env python3

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class TextEditor(QTextEdit):
    def __init__(self, pagePath=None, parent=None):
        super().__init__(parent)

        self.pagePath = pagePath
        self.changed = False

        self.connect(self, SIGNAL('textChanged()'), self.Changed)

    def Changed(self):
        self.changed = True

    def CloseRequest(self):
        if self.changed:
            answer = QMessageBox.question(self, self.tr('노트 저장'), 
                    self.tr('노트를 저장하시겠습니까?'),
                    QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

            if answer == QMessageBox.Cancel:
                return False
            elif answer == QMessageBox.Yes:
                self.Save()

        return True

    def Save(self):
        pageFile = open(self.pagePath, 'w')
        pageFile.write(self.toHtml())
        pageFile.close()
