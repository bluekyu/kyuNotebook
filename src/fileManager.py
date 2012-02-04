#!/usr/bin/env python3

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
