#!/usr/bin/env python3

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_mainWindow
import noteTreeWidget
import fileManager

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
        self.noteDirPath = settings.value('lastNoteDirPath') or ''
        self.restoreGeometry(settings.value('mainWindow.Geometry', 
            QByteArray()))
        self.restoreState(settings.value('mainWindow.State',
            QByteArray()))

        # 기존 노트 열기
        if not fileManager.os.path.exists(self.noteDirPath):
            QTimer.singleShot(0, self.on_changeNoteDirAction_triggered)
        else:
            fileManager.LoadNote(self.noteDirPath)

    ### 슬롯 ###
    @pyqtSignature('')
    def on_newDirAction_triggered(self):
        self.noteTree.NewDir()

    @pyqtSignature('')
    def on_newNoteAction_triggered(self):
        self.noteTree.NewNote()

    @pyqtSignature('')
    def on_newPageAction_triggered(self):
        self.noteTree.NewPage()

    @pyqtSignature('')
    def on_changeNoteDirAction_triggered(self):
        self.noteDirPath = fileManager.ChangeNoteDirPath(self, self.noteDirPath)
        fileManager.LoadNote(self.noteDirPath)

    ### 메소드 ###
    def closeEvent(self, event):
        settings = QSettings()
        settings.setValue('lastNoteDirPath', self.noteDirPath)
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
