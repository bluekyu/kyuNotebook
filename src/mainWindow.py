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

__version__ = '0.0.1'
__program_name__ = 'kyuNotebook'
__author__ = 'YoungUk Kim'
__date__ = '02.02.2012'

class MainWindow(QMainWindow, ui_mainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setOrganizationName('bluekyu')
    app.setOrganizationDomain('bluekyu.me')
    app.setApplicationName(__program_name__)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()
