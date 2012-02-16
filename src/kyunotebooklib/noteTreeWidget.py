#!/usr/bin/env python3

'''트리 위젯에 대한 정보 및 파일 관리를 담당하는 파일'''

import os, shutil, tempfile, logging
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from kyunotebooklib.noteTreeItem import CommonItem, NoteItem, PageItem
from kyunotebooklib.configManager import ConfigManager

### 파일 처리 함수 ###
def MakeKey(prefix, suffix, dirPath):
    '''임시 키를 생성하는 함수'''
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
    '''노트 트리 및 파일 관리를 위한 클래스'''

    def __init__(self, noteDirPath='', contextAction=[], parent=None):
        super().__init__(parent)
        self.setHeaderLabel(self.tr('이름'))
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.addActions(contextAction)

        self.noteDirPath = noteDirPath
        self.logger = logging.getLogger('noteTreeWidget.NoteTreeWidget')
        self.LoadNote()

    def LoadNote(self):
        '''노트를 불러오는 메소드'''
        if os.path.exists(self.noteDirPath) == False:
            # 노트 폴더 생성
            if self.ChangeNoteDirPath() == False:
                QMessageBox.critical(self, self.tr('노트 폴더 생성 불가'),
                        self.tr('노트 폴더가 생성되지 않았습니다.\n'
                            '노트 폴더가 없으면 기능을 사용할 수 없습니다.'))
                return

        noteDir = self.noteDirPath
        config = ConfigManager(noteDir)
        self.clear()
        rootItem = CommonItem(self, [self.tr('노트 폴더')])

        noteList = []
        try:
            while True:
                for note in config.LoadNote():
                    item = self.AddNote(
                            rootItem, note['title'], note['key'])
                    noteList.insert(0, (item, 
                        os.path.join(noteDir, note['key'])))

                for page in config.LoadPage():
                    self.AddPage(
                            rootItem, page['title'], page['key'])

                if noteList == []:
                    break

                rootItem, noteDir = noteList.pop()
                config = ConfigManager(noteDir)
        except Exception as err:
            self.logger.error('노트 불러오는 중에 오류 - ' + str(err))
            QMessageBox.critical(self, self.tr('노트 불러오기 실패!'),
                    self.tr('노트를 불러오는 중에 오류가 발생하였습니다!'))

    def ChangeNoteDirPath(self):
        '''노트 폴더 경로를 변경하는 메소드'''
        newNoteDirPath = QFileDialog.getExistingDirectory(self, 
                self.tr('새 노트 폴더'),
                self.noteDirPath or os.path.expanduser('~'))

        if not newNoteDirPath:
            return False

        if os.listdir(newNoteDirPath) != []:
            QMessageBox.warning(self, self.tr('폴더가 비어있지 않음!'),
                    self.tr('폴더가 비어 있지 않습니다!\n'
                    '비어있는 폴더를 생성해주십시오!'))
            return False

        # 기존 노트 복사
        try:
            if os.path.exists(self.noteDirPath):
                CopyTree(self.noteDirPath, newNoteDirPath)
        except OSError as err:
            self.logger.error('노트 폴더 복사 부분 오류 - ' + str(err))
            QMessageBox.critical(self,
                    self.tr('복사 오류!'),
                    self.tr('기존 노트의 복사 중에 다음 오류가 발생하였습니다!\n'
                              '노트 폴더 변경을 중단합니다.'))
            return False

        self.noteDirPath = newNoteDirPath
        return True
  
    def AddNote(self, root, title, key):
        '''노트를 추가하는 메소드'''
        item = NoteItem(root, [title])
        item.key = key

        return item

    def AddPage(self, root, title, key):
        '''페이지를 추가하는 메소드'''
        item = PageItem(root, [title])
        item.key = key

        return item

    def NewNote(self):
        '''새로운 노트를 생성하는 메소드'''
        currentItem = self.currentItem()
        notePath = self.GetItemPath(currentItem)
        key = MakeKey('', '', notePath)
        newNotePath = os.path.join(notePath, key)
        os.mkdir(newNotePath, 0o755)
        title = self.tr('새 노트')

        config = ConfigManager(notePath)
        config.AddNote(title, key)
        config.Write()

        ConfigManager(newNotePath)

        return self.AddNote(currentItem, title, key)

    def NewPage(self):
        '''새로운 페이지를 생성하는 메소드'''
        currentItem = self.currentItem()
        notePath = self.GetItemPath(currentItem)
        key = MakeKey('', '.html', notePath)
        pagePath = os.path.join(notePath, key)
        open(pagePath, 'w').close()
        title = self.tr('새 페이지')

        config = ConfigManager(notePath)
        config.AddPage(title, key)
        config.Write()

        return self.AddPage(currentItem, title, key)

    def EditTitle(self):
        '''아이템 제목 편집 메소드'''
        self.editItem(self.currentItem())

    def RemoveItem(self, item):
        '''아이템 제거 메소드'''
        itemPath = self.GetItemPath(item)
        dirPath, key = os.path.split(itemPath)
        config = ConfigManager(dirPath)
        try:
            if self.IsPage(item):
                os.remove(itemPath)
                config.RemovePage(key)                
            else:
                shutil.rmtree(itemPath)
                config.RemoveNote(key)
            config.Write()
        except Exception as err:
            self.logger.error('파일 삭제 중에 오류 - ' + str(err))
            QMessageBox.critical(self, self.tr('파일 삭제 오류!'),
                    self.tr('파일을 삭제하는 중에 오류가 발생하였습니다!'))
            return

        parent = item.parent()
        parent.takeChild(parent.indexOfChild(item))
        
    def IsNote(self, item):
        '''노트인지 판별해주는 메소드'''
        return isinstance(item, NoteItem)

    def IsPage(self, item):
        '''페이지인지 판별해주는 메소드'''
        return isinstance(item, PageItem)

    def ChangeTitle(self, item):
        '''아이템 제목을 변경하는 메소드'''
        itemPath = self.GetItemPath(item)
        dirPath, key = os.path.split(itemPath)

        config = ConfigManager(dirPath)
        config.ChangeTitle(item.title, key)
        config.Write()

        return itemPath

    def GetItemPath(self, item):
        '''아이템의 실제 경로를 반환하는 메소드'''
        keyList = []
        while True:
            if item.parent() is None:
                break
            keyList.insert(0, item.key)
            item = item.parent()

        return os.path.join(self.noteDirPath, *keyList)

    def GetCurrentPage(self):
        '''현재 페이지 아이템을 반환하는 메소드'''
        item = self.currentItem()
        if self.IsPage(item):
            return item
        else:
            return None
