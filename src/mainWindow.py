#!/usr/bin/env python3

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_mainWindow
import noteTreeWidget
import fileManager
import textEditor

__version__ = '0.0.1'
__program_name__ = 'kyuNotebook'
__author__ = 'YoungUk Kim'
__date__ = '02.02.2012'

class MainWindow(QMainWindow, ui_mainWindow.Ui_MainWindow):
    '''메인 윈도우 클래스'''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.fileManager = fileManager.FileManager(self)
        self.noteTree = noteTreeWidget.NoteTreeWidget(self)
        self.noteTreeDockWidget.setWidget(self.noteTree)

        self.connect(self.noteTree,
            SIGNAL('currentItemChanged(QTreeWidgetItem*, QTreeWidgetItem*)'),
            self.NoteTreeActionEnabled)

        ### 설정 복원 ###
        settings = QSettings()
        self.fileManager.noteDirPath = settings.value('lastNoteDirPath') or ''
        self.restoreGeometry(settings.value('mainWindow.Geometry', 
            QByteArray()))
        self.restoreState(settings.value('mainWindow.State',
            QByteArray()))

        # 기존 노트 열기
        if not self.fileManager.NoteExists():
            QTimer.singleShot(0, self.on_changeNoteDirAction_triggered)
        else:
            self.fileManager.LoadNote(self.noteTree)

    ### 슬롯 ###
    @pyqtSignature('')
    def on_newNoteAction_triggered(self):
        key = self.fileManager.NewNote(self.noteTree.GetItemPathList())
        self.noteTree.CurrentNewNote(key)

    @pyqtSignature('')
    def on_newPageAction_triggered(self):
        key, pagePath = self.fileManager.NewPage(self.noteTree.GetItemPathList())
        self.noteTree.CurrentNewPage(key)
        pageTitle = self.tr('새 페이지')
        editor = textEditor.TextEditor(pageTitle, pagePath)
        self.pageTab.addTab(editor, pageTitle)

    @pyqtSignature('')
    def on_changeNoteDirAction_triggered(self):
        self.fileManager.ChangeNoteDirPath()
        self.fileManager.LoadNote(self.noteTree)

    @pyqtSignature('int')
    def on_pageTab_tabCloseRequested(self, tabIndex):
        editor = self.pageTab.widget(tabIndex)
        if editor.CloseRequest():
            self.pageTab.removeTab(tabIndex)

    @pyqtSignature('')
    def on_pageSaveAction_triggered(self):
        editor = self.pageTab.currentWidget()
        if editor is not None:
            editor.Save()

    def on_allPageSaveAction_triggered(self):
        for tabIndex in range(len(self.pageTab)):
            editor = self.pageTab.widget(tabIndex)
            if editor is not None:
                editor.Save()

    ### 메소드 ###
    def closeEvent(self, event):
        settings = QSettings()
        settings.setValue('lastNoteDirPath', self.fileManager.noteDirPath)
        settings.setValue('mainWindow.Geometry', self.saveGeometry())
        settings.setValue('mainWindow.State', self.saveState())

    def NoteTreeActionEnabled(self, currentItem, previousItem):
        self.newNoteAction.setEnabled(False)
        self.newPageAction.setEnabled(False)
 
        currentType = currentItem.type()
        if currentType == self.noteTree.NOTE_TYPE:
            self.newNoteAction.setEnabled(True)
            self.newPageAction.setEnabled(True)
        elif currentType == self.noteTree.PAGE_TYPE:
            pass
        else:
            self.newNoteAction.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    QTextCodec.setCodecForTr(QTextCodec.codecForName('UTF-8')) # trUtf8 대신 사용

    app.setOrganizationName('bluekyu')
    app.setOrganizationDomain('bluekyu.me')
    app.setApplicationName(__program_name__)

    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()
