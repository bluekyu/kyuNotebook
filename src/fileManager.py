#!/usr/bin/env python3

import os, shutil, tempfile
import xml.etree.ElementTree as xml
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class FileManager(QObject):
    CONFIG_FILE_NAME = 'config.xml'

    def __init__(self, parent=None):
        super().__init__(parent)

    def NoteExists(self):
        return os.path.exists(self.noteDirPath)

    def ChangeNoteDirPath(self):
        newNoteDirPath = QFileDialog.getExistingDirectory(self, 
                self.tr('새 폴더 목록'),
                oldNoteDirPath or os.path.expanduser('~'))

        if not newNoteDirPath:
            return

        # 기존 노트 복사
        try:
            if os.path.exists(self.noteDirPath):
                CopyTree(self.noteDirPath, newNoteDirPath)
        except OSError:
            QMessageBox.critical(parent,
                    self.tr('복사 오류!'),
                    self.tr('기존 노트의 복사 중에 오류가 발생하였습니다!\n'
                              '노트 폴더 변경을 중단합니다.'))
            return

        self.noteDirPath = newNoteDirPath

    def CopyTree(self, src, dest):
        '''src 폴더 내용을 dest 폴더에 복사'''
        for fileName in os.listdir(src):
            filePath = os.path.join(src, fileName)
            if os.path.isdir(filePath):
                shutil.copytree(filePath, os.path.join(dest, fileName))
            else:
                shutil.copy2(filePath, dest)

    def NewDir(self, pathList):
        dirPath = os.path.join(self.noteDirPath, *pathList)
        dirName = self.MakeTempName('', '', dirPath)
        newDirPath = os.path.join(dirPath, dirName)
        os.mkdir(newDirPath, 0o755)

        # xml에 폴더 추가
        xmlPath = os.path.join(dirPath, self.CONFIG_FILE_NAME)
        configXml = xml.ElementTree()
        rootElement = configXml.parse(xmlPath)
        newElement = xml.Element('dir', 
                {'title': self.tr('새 폴더'), 'name': dirName})
        rootElement.append(newElement)
        configXml.write(xmlPath, 'unicode', True)

        # xml 추가
        xmlPath = os.path.join(newDirPath, self.CONFIG_FILE_NAME)
        xml.ElementTree(xml.Element('directory')).write(
                xmlPath, 'unicode', True)

        return dirName

    def MakeTempName(self, prefix, suffix, dirPath):
        while True:
            name = os.path.basename(tempfile.mkdtemp(suffix, prefix))
            if not os.path.exists(os.path.join(dirPath, name)):
                break

        return name

    def LoadNote(self, noteTree):
        xmlPath = os.path.join(self.noteDirPath, self.CONFIG_FILE_NAME)
        if not os.path.exists(xmlPath):
            xml.ElementTree(xml.Element('directory')).write(
                    xmlPath, 'unicode', True)
        rootElement = xml.ElementTree().parse(xmlPath)
        rootItem = QTreeWidgetItem(noteTree, [self.tr('노트 폴더')])
        rootItem.setExpanded(True)
