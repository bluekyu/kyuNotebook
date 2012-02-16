#!/usr/bin/env python3

'''트리 위젯에 추가되는 아이템들에 대한 정보를 포함하는 파일'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class CommonItem(QTreeWidgetItem):
    '''아이템의 공통 요소를 모은 클래스'''
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.title = self.text(0)
        self.key = ''

        self.setExpanded(True)

    def IsTitleChanged(self):
        '''제목이 변경되었는지 알려주는 메소드'''
        if self.title == self.text(0):
            return False
        else:
            self.title = self.text(0)
            return True

class NoteItem(CommonItem):
    '''노트 아이템에 대한 클래스'''
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.setFlags(self.flags() | Qt.ItemIsEditable)

class PageItem(CommonItem):
    '''페이지 아이템에 대한 클래스'''
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.editor = None

        self.setFlags(self.flags() | Qt.ItemIsEditable)
        self.setExpanded(False)
