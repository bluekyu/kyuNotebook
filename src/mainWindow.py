#!/usr/bin/env python3

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_mainWindow
import noteTreeWidget
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

        ### 설정 복원 ###
        settings = QSettings()
        noteDirPath = settings.value('lastNoteDirPath') or ''
        self.restoreGeometry(settings.value('mainWindow.Geometry', 
            QByteArray()))
        self.restoreState(settings.value('mainWindow.State',
            QByteArray()))

        noteTreeAction = [self.openPageAction, self.changeTitleAction]
        self.noteTree = noteTreeWidget.NoteTreeWidget(
                            noteDirPath, noteTreeAction, self)
        self.noteTreeDockWidget.setWidget(self.noteTree)

        self.connect(self.noteTree,
            SIGNAL('currentItemChanged(QTreeWidgetItem*, QTreeWidgetItem*)'),
            self.NoteTreeActionEnabled)

        self.connect(self.noteTree,
            SIGNAL('itemChanged(QTreeWidgetItem*, int)'),
            self.ChangeItem)

    ### 슬롯 ###
    @pyqtSignature('')
    def on_newNoteAction_triggered(self):
        self.noteTree.NewNote()
        self.statusbar.showMessage(self.tr('새 노트 생성 완료'), 5000)

    @pyqtSignature('')
    def on_newPageAction_triggered(self):
        item = self.noteTree.NewPage()
        path = self.noteTree.GetItemPath(item)
        item.editor = textEditor.TextEditor(item, path)
        self.pageTab.addTab(item.editor, item.title)
        self.statusbar.showMessage(self.tr('새 페이지 생성 완료'), 5000)

    @pyqtSignature('')
    def on_changeNoteDirAction_triggered(self):
        if self.noteTree.ChangeNoteDirPath(self):
            self.noteTree.LoadNote(self.noteTree)
            self.statusbar.showMessage(self.tr('노트 폴더 변경 완료'), 5000)

    @pyqtSignature('int')
    def on_pageTab_tabCloseRequested(self, tabIndex):
        editor = self.pageTab.widget(tabIndex)
        if editor.CloseRequest():
            editor.item.editor = None
            self.pageTab.removeTab(tabIndex)

    @pyqtSignature('')
    def on_savePageAction_triggered(self):
        editor = self.pageTab.currentWidget()
        if editor is not None:
            editor.Save()
            self.statusbar.showMessage(self.tr('페이지 저장 완료'), 5000)

    @pyqtSignature('')
    def on_saveAllPageAction_triggered(self):
        for tabIndex in range(len(self.pageTab)):
            editor = self.pageTab.widget(tabIndex)
            if editor is not None:
                editor.Save()
        self.statusbar.showMessage(self.tr('모든 페이지 저장 완료'), 5000)

    @pyqtSignature('')
    def on_changeTitleAction_triggered(self):
        self.noteTree.EditTitle()

    @pyqtSignature('')
    def on_openPageAction_triggered(self):
        item = self.noteTree.GetCurrentPage()
        if item is None:
            return
        if item.editor is not None:
            self.pageTab.setCurrentIndex(self.pageTab.indexOf(item.editor))
        else:
            path = self.noteTree.GetItemPath(item)
            item.editor = textEditor.TextEditor(item, path)
            self.pageTab.addTab(item.editor, item.title)

    @pyqtSignature('')
    def on_removeNoteAction_triggered(self):
        pass

    ### 메소드 ###
    def closeEvent(self, event):
        for tabIndex in range(len(self.pageTab)):
            editor = self.pageTab.widget(tabIndex)
            if editor.changed:
                if editor.CloseRequest() == False:
                    event.ignore()
                    return

        settings = QSettings()
        settings.setValue('lastNoteDirPath', self.noteTree.noteDirPath)
        settings.setValue('mainWindow.Geometry', self.saveGeometry())
        settings.setValue('mainWindow.State', self.saveState())

    def NoteTreeActionEnabled(self, currentItem, previousItem):
        self.newNoteAction.setEnabled(False)
        self.newPageAction.setEnabled(False)
        self.openPageAction.setEnabled(False)
 
        if self.noteTree.IsNote(currentItem):
            self.newNoteAction.setEnabled(True)
            self.newPageAction.setEnabled(True)
        elif self.noteTree.IsPage(currentItem):
            self.openPageAction.setEnabled(True)
        else:
            self.newNoteAction.setEnabled(True)

    def ChangeItem(self, item, column):
        if column == 0 and item.IsTitleChanged():
            path = self.noteTree.ChangeTitle(item)
            if self.noteTree.IsPage(item) and item.editor is not None:
                tabIndex = self.pageTab.indexOf(item.editor)
                if tabIndex != -1:
                    self.pageTab.setTabText(tabIndex, item.title)
            self.statusbar.showMessage(self.tr('이름 변경 완료'), 5000)

def main():
    app = QApplication(sys.argv)
    QTextCodec.setCodecForTr(QTextCodec.codecForName('UTF-8')) # trUtf8 대신 사용

    app.setOrganizationName('bluekyu')
    app.setOrganizationDomain('bluekyu.me')
    app.setApplicationName(__program_name__)

    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()
