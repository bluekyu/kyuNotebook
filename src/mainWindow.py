#!/usr/bin/env python3

"""
Copyright (C) 2012년 bluekyu (http://www.bluekyu.me/)
이 프로그램은 자유 소프트웨어입니다. 소프트웨어의 피양도자는 자유 소프트웨어
재단이 공표한 GNU 일반 공중 사용 허가서 2판 또는 그 이후 판을 임의로
선택해서, 그 규정에 따라 프로그램을 개작하거나 재배포할 수 있습니다.
이 프로그램은 유용하게 사용될 수 있으리라는 희망에서 배포되고 있지만,
특정한 목적에 맞는 적합성 여부나 판매용으로 사용할 수 있으리라는 묵시적인
보증을 포함한 어떠한 형태의 보증도 제공하지 않습니다. 보다 자세한 사항에
대해서는 GNU 일반 공중 사용 허가서를 참고하시기 바랍니다.
"""

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_mainWindow
import noteTreeWidget

__version__ = '0.0.1'
__program_name__ = 'kyuNotebook'
__author__ = 'YoungUk Kim'
__date__ = '02.02.2012'

class MainWindow(QMainWindow, ui_mainWindow.Ui_MainWindow):
    '''메인 윈도우 클래스'''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.noteTree = noteTreeWidget.NoteTreeWidget()
        self.noteTreeDockWidget.setWidget(self.noteTree)

        self.connect(self.noteTree,
            SIGNAL('currentItemChanged(QTreeWidgetItem*, QTreeWidgetItem*)'),
            self.NoteTreeActionEnabled)

        ### 설정 복원 ###
        settings = QSettings()
        self.filePath = settings.value('lastFilePath') or None
        self.restoreGeometry(settings.value('mainWindow.Geometry', 
            QByteArray()))
        self.restoreState(settings.value('mainWindow.State',
            QByteArray()))

        if self.filePath is None:
            rootItem = QTreeWidgetItem(self.noteTree, [self.tr('폴더 목록')])
            rootItem.setExpanded(True)
            self.noteTree.setCurrentItem(rootItem)

    ### 슬롯 ###
    @pyqtSignature('')
    def on_newDirAction_triggered(self):
        currentDir = self.noteTree.currentItem()
        dirItem = QTreeWidgetItem(
                    currentDir, [self.tr('새 폴더')], self.noteTree.DIR_TYPE)
        dirItem.setExpanded(True)

    @pyqtSignature('')
    def on_newNoteAction_triggered(self):
        currentDir = self.noteTree.currentItem()
        noteItem = QTreeWidgetItem(
                    currentDir, [self.tr('새 노트')], self.noteTree.NOTE_TYPE)
        noteItem.setExpanded(True)

    @pyqtSignature('')
    def on_newPageAction_triggered(self):
        currentNote = self.noteTree.currentItem()
        pageItem = QTreeWidgetItem(
                    currentNote, [self.tr('새 페이지')], self.noteTree.PAGE_TYPE)

    ### 메소드 ###
    def closeEvent(self, event):
        settings = QSettings()
        settings.setValue('lastFilePath', self.filePath)
        settings.setValue('mainWindow.Geometry', self.saveGeometry())
        settings.setValue('mainWindow.State', self.saveState())

    def NoteTreeActionEnabled(self, currentItem, previousItem):
        self.newDirAction.setEnabled(False)
        self.newNoteAction.setEnabled(False)
        self.newPageAction.setEnabled(False)
 
        currentType = currentItem.type()
        if currentType == self.noteTree.DIR_TYPE:
            self.newDirAction.setEnabled(True)
            self.newNoteAction.setEnabled(True)
        elif currentType == self.noteTree.NOTE_TYPE:
            self.newPageAction.setEnabled(True)
        elif currentType == self.noteTree.PAGE_TYPE:
            pass
        else:
            self.newDirAction.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    QTextCodec.setCodecForTr(QTextCodec.codecForName('UTF-8')) # trUtf8 대신 사용

    app.setOrganizationName('bluekyu')
    app.setOrganizationDomain('bluekyu.me')
    app.setApplicationName(__program_name__)

    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()
