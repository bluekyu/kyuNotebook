#!/usr/bin/env python3

'''프로그램의 실행을 담당하는 파일'''

import sys
from PyQt4.QtCore import QTextCodec
from PyQt4.QtGui import QApplication
from kyuNotebook import mainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    QTextCodec.setCodecForTr(QTextCodec.codecForName('UTF-8')) # trUtf8 대신 사용

    app.setOrganizationName('bluekyu')
    app.setOrganizationDomain('bluekyu.me')
    app.setApplicationName('kyuNotebook')

    mainWindow = mainWindow.MainWindow()
    mainWindow.show()
    app.exec_()
