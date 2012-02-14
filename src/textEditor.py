#!/usr/bin/env python3

'''에디터에 대한 정보를 포함하는 파일'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class TextEditor(QTextEdit):
    '''텍스트 에디터 클래스'''
    def __init__(self, item=None, path=None, parent=None):
        super().__init__(parent)

        self.changed = False
        self.path = path
        self.item = item

        self.connect(self, SIGNAL('textChanged()'), self.Changed)

        self.Load()

    def Changed(self):
        '''에디터 변경 시 작동'''
        self.changed = True

    def CloseRequest(self):
        '''닫기 요청이 있을 시에 실행되는 메소드'''
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
        '''에디터에 파일을 불러오는 메소드'''
        pageFile = open(self.path, 'r')
        self.setHtml(pageFile.read())
        pageFile.close()
        self.changed = False

    def Save(self):
        '''에디터를 파일에 저장하는 메소드'''
        self.setDocumentTitle(self.item.title)
        pageFile = open(self.path, 'w')
        pageFile.write(self.toHtml())
        pageFile.close()
        self.changed = False
