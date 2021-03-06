#!/usr/bin/env python3

'''메인 윈도우의 실행을 담당하는 파일'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from kyunotebooklib import ui_mainWindow
from kyunotebooklib import noteTreeWidget
from kyunotebooklib import textEditor

class MainWindow(QMainWindow, ui_mainWindow.Ui_MainWindow):
    '''메인 윈도우 클래스'''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.AdditionalUi()

        ### 설정 복원 ###
        settings = QSettings()
        noteDirPath = settings.value('lastNoteDirPath') or ''
        self.restoreGeometry(settings.value('mainWindow.Geometry', 
            QByteArray()))
        self.restoreState(settings.value('mainWindow.State',
            QByteArray()))

        noteTreeAction = [self.editPageAction, self.changeTitleAction, 
                self.removeItemAction]
        self.noteTree = noteTreeWidget.NoteTreeWidget(
                            noteDirPath, noteTreeAction, self)
        self.noteTreeDockWidget.setWidget(self.noteTree)

        self.connect(self.noteTree,
            SIGNAL('currentItemChanged(QTreeWidgetItem*, QTreeWidgetItem*)'),
            self.NoteTreeActionEnabled)

        self.connect(self.noteTree,
            SIGNAL('itemChanged(QTreeWidgetItem*, int)'),
            self.ChangeItem)

        self.connect(self.noteTree,
            SIGNAL('itemDoubleClicked(QTreeWidgetItem*, int)'),
            self.ItemDoubleClicked)

    ### 슬롯 ###
    @pyqtSignature('')
    def on_newNoteAction_triggered(self):
        '''새 노트를 생성하는 슬롯'''
        self.noteTree.NewNote()
        self.statusbar.showMessage(self.tr('새 노트 생성 완료'), 5000)

    @pyqtSignature('')
    def on_newPageAction_triggered(self):
        '''새 페이지를 생성하는 슬롯'''
        item = self.noteTree.NewPage()
        self.AddPageTab(item)
        self.statusbar.showMessage(self.tr('새 페이지 생성 완료'), 5000)

    @pyqtSignature('')
    def on_changeNoteDirAction_triggered(self):
        '''노트 폴더 경로를 변경하는 슬롯'''
        if self.pageTab.count() != 0:
            QMessageBox.information(self, self.tr('페이지 열림'),
                    self.tr('먼저 열려있는 페이지를 모두 닫아주십시오!'))
            return
        if self.noteTree.ChangeNoteDirPath():
            self.noteTree.LoadNote()
            self.statusbar.showMessage(self.tr('노트 폴더 변경 완료'), 5000)

    @pyqtSignature('int')
    def on_pageTab_tabCloseRequested(self, tabIndex):
        '''탭 위젯에서 닫기 단추가 눌렸을 시 동작하는 슬롯'''
        editor = self.pageTab.widget(tabIndex)
        if editor.CloseRequest():
            editor.item.editor = None
            self.pageTab.removeTab(tabIndex)

    @pyqtSignature('int')
    def on_pageTab_currentChanged(self, tabIndex):
        '''현재 탭이 변경되었을 때 동작하는 슬롯'''
        if tabIndex >= 0:
            editor = self.pageTab.widget(tabIndex)
            self.FontToolBarActionEnabled(editor.currentCharFormat())

    @pyqtSignature('')
    def on_closeCurrentPageAction_triggered(self):
        '''현재 페이지를 닫는 요청 시에 동작하는 슬롯'''
        tabIndex = self.pageTab.currentIndex()
        if tabIndex >= 0:
            self.on_pageTab_tabCloseRequested(tabIndex)

    @pyqtSignature('')
    def on_savePageAction_triggered(self):
        '''현재 페이지를 저장하는 슬롯'''
        editor = self.pageTab.currentWidget()
        if editor is not None:
            editor.Save()
            self.statusbar.showMessage(self.tr('페이지 저장 완료'), 5000)

    @pyqtSignature('')
    def on_saveAllPageAction_triggered(self):
        '''현재 열린 모든 페이지를 저장하는 슬롯'''
        for tabIndex in range(len(self.pageTab)):
            editor = self.pageTab.widget(tabIndex)
            if editor is not None:
                editor.Save()
        self.statusbar.showMessage(self.tr('모든 페이지 저장 완료'), 5000)

    @pyqtSignature('')
    def on_changeTitleAction_triggered(self):
        '''현재 선택한 아이템에 대한 제목을 변경하는 슬롯'''
        self.noteTree.EditTitle()

    @pyqtSignature('')
    def on_editPageAction_triggered(self):
        '''현재 선택한 페이지를 탭에 여는 슬롯'''
        item = self.noteTree.currentItem()
        if not self.noteTree.IsPage(item):
            return
        if item.editor is not None:
            self.pageTab.setCurrentIndex(self.pageTab.indexOf(item.editor))
        else:
            self.AddPageTab(item)

    @pyqtSignature('')
    def on_removeItemAction_triggered(self):
        '''현재 선택한 아이템을 제거하는 슬롯'''
        item = self.noteTree.currentItem()
        if self.noteTree.IsPage(item):
            if QMessageBox.question(self, self.tr('페이지 삭제'),
                self.tr('현재 페이지를 정말 삭제하시겠습니까?'),
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == \
                QMessageBox.No:
                return

            if item.editor is not None:
                QMessageBox.warning(self, self.tr('페이지 열림'),
                    self.tr('삭제하려는 페이지가 열려 있습니다.\n'
                            '페이지를 닫은 후에 삭제하십시오.'))
                self.pageTab.setCurrentIndex(self.pageTab.indexOf(item.editor))
                return
        elif self.noteTree.IsNote(item):
            if QMessageBox.question(self, self.tr('노트 삭제'),
                self.tr('현재 노트 및 노트의 다른 항목 '
                    '모두를 정말 삭제하시겠습니까?'),
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == \
                QMessageBox.No:
                return
            path = self.noteTree.GetItemPath(item)
            for tabIndex in range(len(self.pageTab)):
                editor = self.pageTab.widget(tabIndex)
                if editor.path.startswith(path, 0):
                    QMessageBox.warning(self, self.tr('노트 열림'), self.tr(
                        '삭제하려는 노트에 있는 페이지가 열려 있습니다.\n'
                        '페이지를 닫은 후에 삭제하십시오.'))
                    self.pageTab.setCurrentIndex(tabIndex)
                    return
        else:
            return

        self.noteTree.RemoveItem(item)
        self.statusbar.showMessage(self.tr('삭제 완료'), 5000)

    @pyqtSignature('')
    def on_fontAction_triggered(self):
        '''글꼴 대화 상자를 엶'''
        editor = self.pageTab.currentWidget()
        if editor is not None:
            editor.SetFont()

    @pyqtSignature('bool')
    def on_boldAction_triggered(self, check):
        '''글꼴을 굵게 표시함'''
        editor = self.pageTab.currentWidget()
        if editor is not None:
            editor.setFontWeight(QFont.Bold if check else QFont.Normal)

    @pyqtSignature('bool')
    def on_italicAction_triggered(self, check):
        '''글꼴을 이탤릭체로 표시함'''
        editor = self.pageTab.currentWidget()
        if editor is not None:
            editor.setFontItalic(check)

    @pyqtSignature('bool')
    def on_underlineAction_triggered(self, check):
        '''글꼴에 밑줄을 표시함'''
        editor = self.pageTab.currentWidget()
        if editor is not None:
            editor.setFontUnderline(check)

    @pyqtSignature('bool')
    def on_strikeoutAction_triggered(self, check):
        '''글꼴에 취소선을 표시함'''
        editor = self.pageTab.currentWidget()
        if editor is not None:
            editor.SetStrikeout(check)

    @pyqtSignature('')
    def on_aboutAction_triggered(self):
        '''프로그램에 대한 정보를 보여줌'''
        from platform import python_version, system
        from kyunotebooklib import __version__, __program_name__, \
                __author__, __date__, __license__
        QMessageBox.about(self, self.tr('{} 정보').format(__program_name__),
            self.tr('''<p><b>{0}</b>&nbsp;&nbsp;v.{1}</p>
            <p>"{0}"은 노트 필기 프로그램입니다.</p>
            <p>파이썬 {2} - Qt {3} - PyQt {4} - 플랫폼 {5}<br/><br/>
            개발자: {6}<br/>
            라이선스: {7}<br/>
            일자: {8}</p>''').format(
                __program_name__, __version__, python_version, QT_VERSION_STR,
                PYQT_VERSION_STR, system(), __author__, __license__, __date__))

    ### 메소드 ###
    def closeEvent(self, event):
        '''프로그램 종료 이벤트'''
        for tabIndex in range(len(self.pageTab)):
            editor = self.pageTab.widget(tabIndex)
            if editor.changed:
                if editor.CloseRequest() == False:
                    event.ignore()
                    return

        settings = QSettings()
        settings.setValue('lastNoteDirPath', self.noteTree.noteDirPath)
        settings.setValue('mainWindow.Geometry', self.saveGeometry())
        settings.setValue('mainWindow.State', self.saveState())

    def FontComboBoxChanged(self, fontFamily):
        '''글꼴 콤보박스의 값을 적용함'''
        editor = self.pageTab.currentWidget()
        if editor is not None:
            editor.setFontFamily(fontFamily)

    def FontSizeComboBoxChanged(self, fontSizeString):
        '''글꼴 크기의 콤보박스의 값을 적용함'''
        fontSize = int(fontSizeString)
        if fontSize > 0:
            editor = self.pageTab.currentWidget()
            if editor is not None:
                editor.setFontPointSize(fontSize)

    def NoteTreeActionEnabled(self, currentItem, previousItem):
        '''선택하는 아이템이 변경될 시에 액션들에 대한 활성화 여부를 조절'''
        self.newNoteAction.setEnabled(False)
        self.newPageAction.setEnabled(False)
        self.editPageAction.setEnabled(False)
 
        if self.noteTree.IsNote(currentItem):
            self.newNoteAction.setEnabled(True)
            self.newPageAction.setEnabled(True)
        elif self.noteTree.IsPage(currentItem):
            self.editPageAction.setEnabled(True)
        else:
            self.newNoteAction.setEnabled(True)

    def FontToolBarActionEnabled(self, fontFormat):
        '''폰트 툴바의 액션들의 활성화 여부를 조절'''
        font = fontFormat.font()
        self.fontComboBox.setCurrentFont(font)
        self.fontSizeComboBox.setEditText(str(font.pointSize()))
        self.boldAction.setChecked(font.bold())
        self.italicAction.setChecked(font.italic())
        self.underlineAction.setChecked(font.underline())
        self.strikeoutAction.setChecked(font.strikeOut())

    def ChangeItem(self, item, column):
        '''아이템에 대한 정보가 변경되었을 시에 실행되는 슬롯'''
        # 제목 변경
        if column == 0 and item.IsTitleChanged():
            path = self.noteTree.ChangeTitle(item)
            if self.noteTree.IsPage(item) and item.editor is not None:
                tabIndex = self.pageTab.indexOf(item.editor)
                if tabIndex != -1:
                    self.pageTab.setTabText(tabIndex, item.title)
            self.statusbar.showMessage(self.tr('이름 변경 완료'), 5000)

    def ItemDoubleClicked(self, item, column):
        '''아이템이 더블 클릭 되었을 때 실행되는 슬롯'''
        if self.noteTree.IsPage(item):
            self.editPageAction.trigger()

    def AddPageTab(self, item):
        '''탭에 페이지를 추가하는 메소드'''
        path = self.noteTree.GetItemPath(item)
        item.editor = textEditor.TextEditor(item, path)
        self.connect(item.editor, 
                SIGNAL('currentCharFormatChanged(const QTextCharFormat&)'),
                self.FontToolBarActionEnabled)
        tabIndex = self.pageTab.addTab(item.editor, item.title)
        self.pageTab.setCurrentIndex(tabIndex)

    def AdditionalUi(self):
        '''추가적인 ui 설정'''
        # 폰트 콤보 박스
        self.fontComboBox = QFontComboBox()
        self.fontToolBar.insertWidget(self.boldAction, self.fontComboBox)
        self.connect(self.fontComboBox, SIGNAL('activated(const QString&)'),
            self.FontComboBoxChanged)
       
        # 폰트 크기 콤보 박스
        self.fontSizeComboBox = QComboBox()
        self.fontSizeComboBox.addItems(
            ['6', '7', '8', '9', '10', '11', '12', '14', '16', '18', '20',
             '22', '24', '26', '28', '36', '48', '72'])
        self.fontSizeComboBox.setEditable(True)
        self.fontSizeComboBox.setValidator(QIntValidator(1, 512, self))
        self.fontToolBar.insertWidget(self.boldAction, self.fontSizeComboBox)
        self.connect(self.fontSizeComboBox, SIGNAL('activated(const QString&)'),
            self.FontSizeComboBoxChanged)

        self.quitAction.setShortcuts(QKeySequence.Quit)
        self.newPageAction.setShortcuts(QKeySequence.New)
        self.savePageAction.setShortcuts(QKeySequence.Save)
        self.closeCurrentPageAction.setShortcuts(QKeySequence.Close)
