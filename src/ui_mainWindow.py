# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../ui/mainWindow.ui'
#
# Created: Fri Feb  3 00:34:58 2012
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
        MainWindow.resize(720, 547)
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "kyuNotebook", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pageTab = QtGui.QTabWidget(self.centralwidget)
        self.pageTab.setObjectName(_fromUtf8("pageTab"))
        self.newPage = QtGui.QWidget()
        self.newPage.setObjectName(_fromUtf8("newPage"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.newPage)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.pageTab.addTab(self.newPage, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.pageTab)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 720, 22))
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
        self.fileToolBar = QtGui.QToolBar(MainWindow)
        self.fileToolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.fileToolBar.setObjectName(_fromUtf8("fileToolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.fileToolBar)
        self.noteTreeDockWidget = QtGui.QDockWidget(MainWindow)
        self.noteTreeDockWidget.setWindowTitle(QtGui.QApplication.translate("MainWindow", "노트 트리", None, QtGui.QApplication.UnicodeUTF8))
        self.noteTreeDockWidget.setObjectName(_fromUtf8("noteTreeDockWidget"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.noteTreeDockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.noteTreeDockWidget)
        self.quitAction = QtGui.QAction(MainWindow)
        self.quitAction.setText(QtGui.QApplication.translate("MainWindow", "종료", None, QtGui.QApplication.UnicodeUTF8))
        self.quitAction.setObjectName(_fromUtf8("quitAction"))
        self.newPageAction = QtGui.QAction(MainWindow)
        self.newPageAction.setText(QtGui.QApplication.translate("MainWindow", "새 페이지", None, QtGui.QApplication.UnicodeUTF8))
        self.newPageAction.setObjectName(_fromUtf8("newPageAction"))
        self.newNoteAction = QtGui.QAction(MainWindow)
        self.newNoteAction.setText(QtGui.QApplication.translate("MainWindow", "새 노트", None, QtGui.QApplication.UnicodeUTF8))
        self.newNoteAction.setObjectName(_fromUtf8("newNoteAction"))
        self.newDirAction = QtGui.QAction(MainWindow)
        self.newDirAction.setText(QtGui.QApplication.translate("MainWindow", "새 폴더", None, QtGui.QApplication.UnicodeUTF8))
        self.newDirAction.setObjectName(_fromUtf8("newDirAction"))
        self.fileMenu.addAction(self.newDirAction)
        self.fileMenu.addAction(self.newNoteAction)
        self.fileMenu.addAction(self.newPageAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAction)
        self.menubar.addAction(self.fileMenu.menuAction())
        self.menubar.addAction(self.editMenu.menuAction())
        self.menubar.addAction(self.toolMenu.menuAction())
        self.menubar.addAction(self.helpMenu.menuAction())
        self.fileToolBar.addAction(self.newDirAction)
        self.fileToolBar.addAction(self.newNoteAction)
        self.fileToolBar.addAction(self.newPageAction)

        self.retranslateUi(MainWindow)
        self.pageTab.setCurrentIndex(0)
        QtCore.QObject.connect(self.quitAction, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.pageTab.setTabText(self.pageTab.indexOf(self.newPage), QtGui.QApplication.translate("MainWindow", "새 페이지", None, QtGui.QApplication.UnicodeUTF8))

