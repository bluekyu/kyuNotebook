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

        noteTreeAction = [self.openPageAction, self.titleChangeAction]
        self.noteTree = noteTreeWidget.NoteTreeWidget(noteTreeAction, self)
        self.noteTreeDockWidget.setWidget(self.noteTree)

        self.connect(self.noteTree,
            SIGNAL('currentItemChanged(QTreeWidgetItem*, QTreeWidgetItem*)'),
            self.NoteTreeActionEnabled)

        self.connect(self.noteTree,
            SIGNAL('itemChanged(QTreeWidgetItem*, int)'),
            self.TitleChange)

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
        key = self.fileManager.NewNote(
                self.noteTree.GetCurrentItemPathList())
        self.noteTree.CurrentNewNote(key)

    @pyqtSignature('')
    def on_newPageAction_triggered(self):
        key, pagePath = self.fileManager.NewPage(
                self.noteTree.GetCurrentItemPathList())
        pageItem = self.noteTree.CurrentNewPage(key)
        editor = textEditor.TextEditor(pageItem.text(0), pagePath)
        self.pageTab.addTab(editor, pageItem.text(0))

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

    @pyqtSignature('')
    def on_allPageSaveAction_triggered(self):
        for tabIndex in range(len(self.pageTab)):
            editor = self.pageTab.widget(tabIndex)
            if editor is not None:
                editor.Save()

    @pyqtSignature('')
    def on_titleChangeAction_triggered(self):
        self.noteTree.EditTitle()

    @pyqtSignature('')
    def on_openPageAction_triggered(self):
        item = self.noteTree.currentItem()
        if item.type() == self.noteTree.PAGE_TYPE:
            pathList = self.noteTree.GetItemPathList(item)
            pagePath = self.fileManager.AbsoluteFilePath(*pathList)
            for tabIndex in range(len(self.pageTab)):
                if self.pageTab.widget(tabIndex).pagePath == pagePath:
                    self.pageTab.setCurrentIndex(tabIndex)
                    break
            else:
                editor = textEditor.TextEditor(item.text(0), pagePath)
                self.pageTab.addTab(editor, item.text(0))


    ### 메소드 ###
    def closeEvent(self, event):
        for tabIndex in range(len(self.pageTab)):
            editor = self.pageTab.widget(tabIndex)
            if editor.changed:
                if editor.CloseRequest() == False:
                    event.ignore()
                    return

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

    def TitleChange(self, item, column):
        if column != 0:
            return
        print('titleChanged 실행')
        title = item.text(0)
        pathList = self.noteTree.GetItemPathList(item)
        self.fileManager.TitleChange(title, pathList)
        pagePath = self.fileManager.AbsoluteFilePath(*pathList)
        for tabIndex in range(len(self.pageTab)):
            editor = self.pageTab.widget(tabIndex)
            if editor.pagePath == pagePath:
                self.pageTab.setTabText(tabIndex, title)
                editor.pageTitle = title
                break

def main():
    app = QApplication(sys.argv)
    QTextCodec.setCodecForTr(QTextCodec.codecForName('UTF-8')) # trUtf8 대신 사용

    app.setOrganizationName('bluekyu')
    app.setOrganizationDomain('bluekyu.me')
    app.setApplicationName(__program_name__)

    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()
