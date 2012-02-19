#!/usr/bin/env python3

'''에디터에 대한 정보를 포함하는 파일'''

import logging
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class TextEditor(QTextEdit):
    '''텍스트 에디터 클래스'''
    def __init__(self, item=None, path=None, parent=None):
        super().__init__(parent)

        self.changed = False
        self.path = path
        self.item = item
        self.logger = logging.getLogger('textEditor.TextEditor')

        self.connect(self, SIGNAL('textChanged()'), self.Changed)

        self.Load()

    def Changed(self):
        '''에디터 변경 시 작동'''
        self.changed = True

    def SetFont(self):
        font, ok = QFontDialog.getFont(self.currentFont(), self)
        if ok:
            self.setCurrentFont(font)

    def SetBold(self, check):
        font = QFont(self.currentFont())
        font.setBold(check)
        self.setCurrentFont(font)

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
                return self.Save()

        return True

    def Load(self):
        '''에디터에 파일을 불러오는 메소드'''
        try:
            pageFile = open(self.path, 'r')
            self.setHtml(pageFile.read())
            pageFile.close()
            self.changed = False
        except Exception as err:
            self.logger.error('페이지 파일 불러오는 중에 오류 - ' + str(err))
            QMessageBox.critical(self, self.tr('페이지 불러오기 실패!'),
                    self.tr('페이지를 불러오는 중에 오류가 발생하였습니다!'))

    def Save(self):
        '''에디터를 파일에 저장하는 메소드'''
        try:
            self.setDocumentTitle(self.item.title)
            pageFile = open(self.path, 'w')
            pageFile.write(self.toHtml())
            pageFile.close()
            self.changed = False
            return True
        except Exception as err:
            self.logger.ERROR('페이지 저장 중에 오류 - ' + str(err))
            QMessageBox.critical(self, self.tr('페이지 저장 실패!'),
                    self.tr('페이지를 저장하는 중에 오류가 발생하였습니다!'))
            return False
