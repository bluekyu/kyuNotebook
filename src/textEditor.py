#!/usr/bin/env python3

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class TextEditor(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.pageFile = None
