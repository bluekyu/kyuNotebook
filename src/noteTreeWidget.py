#!/usr/bin/env python3

import os, shutil, tempfile
import xml.etree.ElementTree as xml
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from noteTreeItem import *

### 파일 처리 함수 ###
def MakeKey(prefix, suffix, dirPath):
    while True:
        name = os.path.basename(tempfile.mkdtemp(suffix, prefix))
        if not os.path.exists(os.path.join(dirPath, name)):
            break

    return name

def CopyTree(src, dest):
    '''src 폴더 내용을 dest 폴더에 복사'''
    for fileName in os.listdir(src):
        filePath = os.path.join(src, fileName)
        if os.path.isdir(filePath):
            shutil.copytree(filePath, os.path.join(dest, fileName))
        else:
            shutil.copy2(filePath, dest)

### 노트 트리 클래스 ###
class NoteTreeWidget(QTreeWidget):
    '''노트 트리를 위한 클래스'''

    def __init__(self, noteDirPath='', contextAction=[], parent=None):
        super().__init__(parent)
        self.setHeaderLabel(self.tr('이름'))
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.addActions(contextAction)

        self.noteDirPath = noteDirPath
        self.configFileName = 'config.xml'
        self.LoadNote()

    def LoadNote(self):
        if os.path.exists(self.noteDirPath) == False:
            # 노트 폴더 생성
            if self.ChangeNoteDirPath() == False:
                QMessageBox.critical(self, self.tr('노트 폴더 생성 불가'),
                        self.tr('노트 폴더가 생성되지 않았습니다.\n'
                            '노트 폴더가 없으면 기능을 사용할 수 없습니다.'))
                return

        xmlDir = self.noteDirPath
        xmlPath = os.path.join(xmlDir, self.configFileName)

        # xml 새로 생성
        if not os.path.exists(xmlPath):
            xml.ElementTree(xml.Element('note')).write(
                    xmlPath, 'unicode', True)
        rootElement = xml.ElementTree().parse(xmlPath)
        rootItem = CommonItem(self, [self.tr('노트 폴더')])

        noteList = []
        while True:
            for note in rootElement.iter('subnote'):
                item = self.AddNote(
                        rootItem, note.get('title'), note.get('key'))
                noteList.insert(0, (item, 
                    os.path.join(xmlDir, note.get('key'))))

            for page in rootElement.iter('page'):
                self.AddPage(
                        rootItem, page.get('title'), page.get('key'))

            if noteList == []:
                break

            rootItem, xmlDir = noteList.pop()
            rootElement = xml.ElementTree().parse(
                    os.path.join(xmlDir, self.configFileName))

    def ChangeNoteDirPath(self):
        newNoteDirPath = QFileDialog.getExistingDirectory(self, 
                self.tr('새 노트 폴더'),
                self.noteDirPath or os.path.expanduser('~'))

        if not newNoteDirPath:
            return False

        # 기존 노트 복사
        try:
            if os.path.exists(self.noteDirPath):
                CopyTree(self.noteDirPath, newNoteDirPath)
        except OSError:
            QMessageBox.critical(self,
                    self.tr('복사 오류!'),
                    self.tr('기존 노트의 복사 중에 오류가 발생하였습니다!\n'
                              '노트 폴더 변경을 중단합니다.'))
            return False

        self.noteDirPath = newNoteDirPath
        return True
  
    def AddNote(self, root, title, key):
        item = NoteItem(root, [title])
        item.key = key

        return item

    def AddPage(self, root, title, key):
        item = PageItem(root, [title])
        item.key = key

        return item

    def NewNote(self):
        currentItem = self.currentItem()
        notePath = self.GetItemPath(currentItem)
        key = MakeKey('', '', notePath)
        newNotePath = os.path.join(notePath, key)
        os.mkdir(newNotePath, 0o755)
        title = self.tr('새 노트')

        # xml에 노트 추가
        xmlPath = os.path.join(notePath, self.configFileName)
        configXml = xml.ElementTree()
        rootElement = configXml.parse(xmlPath)
        newElement = xml.Element('subnote', {'title': title, 'key': key})
        rootElement.append(newElement)
        configXml.write(xmlPath, 'unicode', True)

        # xml 추가
        xmlPath = os.path.join(newNotePath, self.configFileName)
        xml.ElementTree(xml.Element('note')).write(
                xmlPath, 'unicode', True)

        return self.AddNote(currentItem, title, key)

    def NewPage(self):
        currentItem = self.currentItem()
        notePath = self.GetItemPath(currentItem)
        key = MakeKey('', '.html', notePath)
        pagePath = os.path.join(notePath, key)
        open(pagePath, 'w').close()
        title = self.tr('새 페이지')

        # xml에 페이지 추가
        xmlPath = os.path.join(notePath, self.configFileName)
        configXml = xml.ElementTree()
        rootElement = configXml.parse(xmlPath)
        newElement = xml.Element('page', {'title': title, 'key': key})
        rootElement.append(newElement)
        configXml.write(xmlPath, 'unicode', True)

        return self.AddPage(currentItem, title, key)

    def EditTitle(self):
        self.editItem(self.currentItem())

    def RemoveNote(self):
        pass

    def IsNote(self, item):
        return isinstance(item, NoteItem)

    def IsPage(self, item):
        return isinstance(item, PageItem)

    def ChangeTitle(self, item):
        itemPath = self.GetItemPath(item)
        key = os.path.basename(itemPath)
        dirPath = os.path.dirname(itemPath)
        xmlPath = os.path.join(dirPath, self.configFileName)

        configXml = xml.ElementTree()
        rootElement = configXml.parse(xmlPath)
        for element in rootElement.iter():
            if element.get('key') == key:
                element.set('title', item.title)
                break
        configXml.write(xmlPath, 'unicode', True)

        return itemPath

    def GetItemPath(self, item):
        keyList = []
        while True:
            if item.parent() is None:
                break
            keyList.insert(0, item.key)
            item = item.parent()

        return os.path.join(self.noteDirPath, *keyList)

    def GetCurrentPage(self):
        item = self.currentItem()
        if self.IsPage(item):
            return item
        else:
            return None
