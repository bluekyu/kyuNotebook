#!/usr/bin/env python3

'''config 파일에 대한 정보를 다루는 파일'''

from os.path import join, exists
import xml.etree.ElementTree
import logging

class ConfigManager:
    '''config 파일을 처리하는 클래스'''
    configFileName = 'config.xml'

    def __init__(self, xmlDir):
        self.xmlPath = join(xmlDir, self.configFileName)
        self.logger = logging.getLogger('configManger.ConfigManager')

        if exists(self.xmlPath):
            try:
                self.xml = xml.etree.ElementTree.ElementTree()
                self.root = self.xml.parse(self.xmlPath)
            except Exception as err:
                self.logger.error('xml 읽기 실패 - ' + str(err))
        else:
            # config 새로 생성
            self.root = xml.etree.ElementTree.Element('note')
            self.xml = xml.etree.ElementTree.ElementTree(self.root)
            self.Write()

    def AddNote(self, title, key):
        '''노트를 config 에 추가'''
        note = xml.etree.ElementTree.Element('subnote', 
                {'title': title, 'key': key})
        self.root.append(note)

    def AddPage(self, title, key):
        '''페이지를 config에 추가'''
        page = xml.etree.ElementTree.Element('page',
                {'title': title, 'key': key})
        self.root.append(page)

    def RemoveNote(self, key):
        '''노트를 config에서 제거'''
        for note in self.root.iter('subnote'):
            if note.get('key') == key:
                self.root.remove(note)
                return True
        return False

    def RemovePage(self, key):
        '''페이지를 config에서 제거'''
        for page in self.root.iter('page'):
            if page.get('key') == key:
                self.root.remove(page)
                return True
        return False

    def ChangeTitle(self, title, key):
        '''아이템의 제목을 변경'''
        for item in self.root.iter():
            if item.get('key') == key:
                item.set('title', title)
                return True
        return False

    def Write(self):
        '''변경된 config 파일을 씀'''
        try:
            self.xml.write(self.xmlPath, 'UTF-8', True)
        except Exception as err:
            self.logger.error('xml 파일 쓰기 실패 - ' + str(err))

    def Load(self, tag=None):
        '''config 의 태그 정보들을 가져옴'''
        infoList = []
        for element in self.root.iter(tag):
            infoList.append(dict(element.items()))

        return infoList

    def LoadNote(self):
        '''노트에 대한 태그 정보를 가져옴'''
        return self.Load('subnote')

    def LoadPage(self):
        '''페이지에 대한 태그 정보를 가져옴'''
        return self.Load('page')
