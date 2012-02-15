#!/usr/bin/env python3

'''프로그램의 실행을 담당하는 파일'''

import sys, logging
import os
from PyQt4.QtCore import QTextCodec
from PyQt4.QtGui import QApplication
from kyuNotebook import mainWindow

def SetLogging():
    '''로그 파일을 설정해주는 함수'''
    logDir = os.path.expanduser('~/.kyuNotebook')
    if not os.path.exists(logDir):
        os.mkdir(logDir, 0o755)

    logPath = os.path.join(logDir, 'kyuNotebook.log')
    if os.path.exists(logPath):
        logFile = open(logPath, 'r')
        logList = logFile.readlines()
        logFile.close()
        logFile = open(logPath, 'w')
        logFile.writelines(logList[-1000:])
        logFile.close()

    logging.basicConfig(
            format='[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s',
            filename=logPath, level=logging.INFO)

if __name__ == '__main__':
    SetLogging()

    logging.info('Program start')
    app = QApplication(sys.argv)
    QTextCodec.setCodecForTr(QTextCodec.codecForName('UTF-8')) # trUtf8 대신 사용

    app.setOrganizationName('bluekyu')
    app.setOrganizationDomain('bluekyu.me')
    app.setApplicationName('kyuNotebook')

    mainWindow = mainWindow.MainWindow()
    mainWindow.show()
    app.exec_()
    logging.info('Program exit')
