# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../ui/mainWindow.ui'
#
# Created: Thu Feb  2 12:34:24 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(723, 496)
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "kyuNotebook", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pageTab = QtGui.QTabWidget(self.centralwidget)
        self.pageTab.setObjectName(_fromUtf8("pageTab"))
        self.page1 = QtGui.QWidget()
        self.page1.setObjectName(_fromUtf8("page1"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.page1)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.textEdit1 = QtGui.QTextEdit(self.page1)
        self.textEdit1.setObjectName(_fromUtf8("textEdit1"))
        self.horizontalLayout_3.addWidget(self.textEdit1)
        self.pageTab.addTab(self.page1, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.pageTab)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 723, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.fileMenu = QtGui.QMenu(self.menubar)
        self.fileMenu.setTitle(QtGui.QApplication.translate("MainWindow", "파일", None, QtGui.QApplication.UnicodeUTF8))
        self.fileMenu.setObjectName(_fromUtf8("fileMenu"))
        self.editMenu = QtGui.QMenu(self.menubar)
        self.editMenu.setTitle(QtGui.QApplication.translate("MainWindow", "편집", None, QtGui.QApplication.UnicodeUTF8))
        self.editMenu.setObjectName(_fromUtf8("editMenu"))
        self.toolMenu = QtGui.QMenu(self.menubar)
        self.toolMenu.setTitle(QtGui.QApplication.translate("MainWindow", "도구", None, QtGui.QApplication.UnicodeUTF8))
        self.toolMenu.setObjectName(_fromUtf8("toolMenu"))
        self.helpMenu = QtGui.QMenu(self.menubar)
        self.helpMenu.setTitle(QtGui.QApplication.translate("MainWindow", "도움말", None, QtGui.QApplication.UnicodeUTF8))
        self.helpMenu.setObjectName(_fromUtf8("helpMenu"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget = QtGui.QDockWidget(MainWindow)
        self.dockWidget.setWindowTitle(QtGui.QApplication.translate("MainWindow", "노트 트리", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidget.setObjectName(_fromUtf8("dockWidget"))
        self.dockWidgetContent = QtGui.QWidget()
        self.dockWidgetContent.setObjectName(_fromUtf8("dockWidgetContent"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.dockWidgetContent)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.noteTree = QtGui.QTreeWidget(self.dockWidgetContent)
        self.noteTree.setObjectName(_fromUtf8("noteTree"))
        self.noteTree.headerItem().setText(0, _fromUtf8("1"))
        self.horizontalLayout_2.addWidget(self.noteTree)
        self.dockWidget.setWidget(self.dockWidgetContent)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget)
        self.quitAction = QtGui.QAction(MainWindow)
        self.quitAction.setText(QtGui.QApplication.translate("MainWindow", "종료", None, QtGui.QApplication.UnicodeUTF8))
        self.quitAction.setObjectName(_fromUtf8("quitAction"))
        self.newDirAction = QtGui.QAction(MainWindow)
        self.newDirAction.setText(QtGui.QApplication.translate("MainWindow", "새 폴더", None, QtGui.QApplication.UnicodeUTF8))
        self.newDirAction.setObjectName(_fromUtf8("newDirAction"))
        self.newNoteAction = QtGui.QAction(MainWindow)
        self.newNoteAction.setText(QtGui.QApplication.translate("MainWindow", "새 노트", None, QtGui.QApplication.UnicodeUTF8))
        self.newNoteAction.setObjectName(_fromUtf8("newNoteAction"))
        self.openNoteAction = QtGui.QAction(MainWindow)
        self.openNoteAction.setText(QtGui.QApplication.translate("MainWindow", "노트 열기", None, QtGui.QApplication.UnicodeUTF8))
        self.openNoteAction.setObjectName(_fromUtf8("openNoteAction"))
        self.saveNoteAction = QtGui.QAction(MainWindow)
        self.saveNoteAction.setText(QtGui.QApplication.translate("MainWindow", "노트 저장", None, QtGui.QApplication.UnicodeUTF8))
        self.saveNoteAction.setObjectName(_fromUtf8("saveNoteAction"))
        self.fileMenu.addAction(self.newDirAction)
        self.fileMenu.addAction(self.newNoteAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.openNoteAction)
        self.fileMenu.addAction(self.saveNoteAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAction)
        self.menubar.addAction(self.fileMenu.menuAction())
        self.menubar.addAction(self.editMenu.menuAction())
        self.menubar.addAction(self.toolMenu.menuAction())
        self.menubar.addAction(self.helpMenu.menuAction())

        self.retranslateUi(MainWindow)
        self.pageTab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.pageTab.setTabText(self.pageTab.indexOf(self.page1), QtGui.QApplication.translate("MainWindow", "페이지1", None, QtGui.QApplication.UnicodeUTF8))

