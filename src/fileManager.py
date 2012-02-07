#!/usr/bin/env python3

import os, shutil, tempfile
import xml.etree.ElementTree as xml
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class FileManager(QObject):
    CONFIG_FILE_NAME = 'config.xml'

    def __init__(self, parent=None):
        super().__init__(parent)
        self.noteDirPath = ''

    def NoteExists(self):
        return os.path.exists(self.noteDirPath)

    def AbsoluteFilePath(self, *pathList):
        return os.path.join(self.noteDirPath, *pathList)

    def ChangeNoteDirPath(self):
        newNoteDirPath = QFileDialog.getExistingDirectory(self, 
                self.tr('새 노트 폴더'),
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

    def NewNote(self, pathList):
        notePath = os.path.join(self.noteDirPath, *pathList)
        noteName = self.MakeTempName('', '', notePath)
        newNotePath = os.path.join(notePath, noteName)
        os.mkdir(newNotePath, 0o755)

        # xml에 노트 추가
        xmlPath = os.path.join(notePath, self.CONFIG_FILE_NAME)
        configXml = xml.ElementTree()
        rootElement = configXml.parse(xmlPath)
        newElement = xml.Element('subnote', 
                {'title': self.tr('새 노트'), 'name': noteName})
        rootElement.append(newElement)
        configXml.write(xmlPath, 'unicode', True)

        # xml 추가
        xmlPath = os.path.join(newNotePath, self.CONFIG_FILE_NAME)
        xml.ElementTree(xml.Element('note')).write(
                xmlPath, 'unicode', True)

        return noteName

    def NewPage(self, pathList):
        notePath = os.path.join(self.noteDirPath, *pathList)
        pageName = self.MakeTempName('', '.html', notePath)
        pagePath = os.path.join(notePath, pageName)
        open(pagePath, 'w').close()

        # xml에 페이지 추가
        xmlPath = os.path.join(notePath, self.CONFIG_FILE_NAME)
        configXml = xml.ElementTree()
        rootElement = configXml.parse(xmlPath)
        newElement = xml.Element('page',
                {'title': self.tr('새 페이지'), 'name': pageName})
        rootElement.append(newElement)
        configXml.write(xmlPath, 'unicode', True)

        return (pageName, pagePath)

    def MakeTempName(self, prefix, suffix, dirPath):
        while True:
            name = os.path.basename(tempfile.mkdtemp(suffix, prefix))
            if not os.path.exists(os.path.join(dirPath, name)):
                break

        return name

    def LoadNote(self, noteTree):
        xmlDir = self.noteDirPath
        xmlPath = os.path.join(xmlDir, self.CONFIG_FILE_NAME)
        # xml 새로 생성
        if not os.path.exists(xmlPath):
            xml.ElementTree(xml.Element('note')).write(
                    xmlPath, 'unicode', True)
        rootElement = xml.ElementTree().parse(xmlPath)
        rootItem = QTreeWidgetItem(noteTree, [self.tr('노트 폴더')])
        rootItem.setExpanded(True)

        noteList = []
        while True:
            for note in rootElement.iter('subnote'):
                item = noteTree.MakeNote(
                        rootItem, note.get('title'), note.get('name'))
                noteList.insert(0, (item, 
                    os.path.join(xmlDir, note.get('name'))))

            for page in rootElement.iter('page'):
                noteTree.MakePage(
                        rootItem, page.get('title'), page.get('name'))

            if noteList == []:
                break

            rootItem, xmlDir = noteList.pop()
            rootElement = xml.ElementTree().parse(
                    os.path.join(xmlDir, self.CONFIG_FILE_NAME))

    def TitleChange(self, title, itemType, pathList):
        pass
