#!/usr/bin/env python3

'''
Copyright (C) 2012년 bluekyu (http://www.bluekyu.me/)
이 프로그램은 자유 소프트웨어입니다. 소프트웨어의 피양도자는 자유 소프트웨어
재단이 공표한 GNU 일반 공중 사용 허가서 2판 또는 그 이후 판을 임의로
선택해서, 그 규정에 따라 프로그램을 개작하거나 재배포할 수 있습니다.
이 프로그램은 유용하게 사용될 수 있으리라는 희망에서 배포되고 있지만,
특정한 목적에 맞는 적합성 여부나 판매용으로 사용할 수 있으리라는 묵시적인
보증을 포함한 어떠한 형태의 보증도 제공하지 않습니다. 보다 자세한 사항에
대해서는 GNU 일반 공중 사용 허가서를 참고하시기 바랍니다.
'''

import os
import shutil
from PyQt4.QtCore import *
from PyQt4.QtGui import *

def ChangeNoteDirPath(parent, oldNoteDirPath):
    newNoteDirPath = QFileDialog.getExistingDirectory(parent, 
            parent.tr('새 폴더 목록'),
            oldNoteDirPath or os.path.expanduser('~'))

    if not newNoteDirPath:
        return oldNoteDirPath

    # 기존 노트 복사
    try:
        if os.path.exists(oldNoteDirPath):
            CopyTree(oldNoteDirPath, newNoteDirPath)
    except OSError:
        QMessageBox.critical(parent,
                parent.tr('복사 오류!'),
                parent.tr('기존 노트의 복사 중에 오류가 발생하였습니다!\n'
                          '노트 폴더 변경을 중단합니다.'))
        return oldNoteDirPath

    return newNoteDirPath

def CopyTree(src, dest):
    '''src 폴더 내용을 dest 폴더에 복사'''
    for fileName in os.listdir(src):
        filePath = os.path.join(src, fileName)
        if os.path.isdir(filePath):
            shutil.copytree(filePath, os.path.join(dest, fileName))
        else:
            shutil.copy2(filePath, dest)

def LoadNote(noteDirPath):
    pass
