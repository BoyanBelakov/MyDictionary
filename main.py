#!/usr/bin/python
# coding=utf-8


__author__ = 'boyan'
__version__ = '1.2'

import sys
import os
import platform
import dictionaries
import re

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from collections import deque

from find_dialog import FindDialog


DIR_NAME = os.path.dirname(__file__)
FILE_NAME_BACK_IMAGE = os.path.join(DIR_NAME, 'res', 'images', 'back.png')
FILE_NAME_FORWARD_IMAGE = os.path.join(DIR_NAME, 'res', 'images', 'forward.png')
FILE_NAME_WINDOW_ICON = os.path.join(DIR_NAME, 'res', 'images', 'icon.gif')

DEF_FONT_POINT_SIZE = 14
DEF_FONT_FAMILY = 'Monospace'

LINE_EDIT_MIN_WIDTH = 300
TEXT_BROWSER_MIN_HEIGHT = 300
WORD_BUFFER_SIZE = 20

SETTINGS_GEOMETRY = 'Geometry'
SETTINGS_MAIN_WINDOW_STATE = 'MainWindow/State'
SETTINGS_FONT_FAMILY = 'Font/Family'
SETTINGS_FONT_POINT_SIZE = 'Font/PointSize'
SETTINGS_FONT_IS_BOLD = 'Font/IsBold'

MAX_RESULTS = 20

class DictionaryLoader(QThread):
    loadingError = pyqtSignal(Exception)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.myDictionary = None
        self.create = None

    def run(self):
        try:
            self.myDictionary = self.create()
        except Exception as e:
            self.loadingError.emit(e)


class DicHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        QSyntaxHighlighter.__init__(self, parent)

        numberFormat = QTextCharFormat()
        numberFormat.setForeground(Qt.darkBlue)
        numberFormat.setFontWeight(QFont.Bold)

        numberPatten = re.compile(r'\d+\.')
        romanPatten = re.compile(r'[IVXLSDM]+\.')

        self.rules = [(numberPatten, numberFormat), (romanPatten, numberFormat)]

    def highlightBlock(self, text):
        text = unicode(text)
        for patten, format in self.rules:
            for match in patten.finditer(text):
                start = match.start()
                length = match.end() - start
                self.setFormat(start, length, format)


class DicWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.lineEdit = QLineEdit()
        self.lineEdit.setMinimumWidth(LINE_EDIT_MIN_WIDTH)
        self.lineEdit.setPlaceholderText('Enter word')

        self.listWidget = QListWidget()

        self.textBrowser = QTextBrowser()
        self.textBrowser.setMinimumHeight(TEXT_BROWSER_MIN_HEIGHT)

        vbox = QVBoxLayout()
        vbox.addWidget(self.lineEdit)
        vbox.addWidget(self.listWidget)
        vbox.addWidget(self.textBrowser)
        self.setLayout(vbox)


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None)

        self.setWindowTitle('My Dictionary')
        self.setWindowIcon(QIcon(FILE_NAME_WINDOW_ICON))

        self.findDialog = FindDialog(self)
        self.findDialog.match.connect(self.match)

        self.dicComboBox = QComboBox()
        self.dicComboBox.setFocusPolicy(Qt.NoFocus)
        self.dicComboBox.addItems(['EN-BG', 'BG-EG'])
        self.dicComboBox.currentIndexChanged.connect(self.load)

        self.backAction = QAction(QIcon(FILE_NAME_BACK_IMAGE), 'Back', self)
        self.backAction.setEnabled(False)
        self.backAction.setShortcut('F2')
        self.backAction.triggered.connect(self.back)

        self.forwardAction = QAction(QIcon(FILE_NAME_FORWARD_IMAGE), 'Forward', self)
        self.forwardAction.setEnabled(False)
        self.forwardAction.setShortcut('F3')
        self.forwardAction.triggered.connect(self.forward)

        self.aboutAction = QAction('About', self)
        self.aboutAction.triggered.connect(self.about)

        self.fontAction = QAction('Font', self)
        self.fontAction.triggered.connect(self.showFontDialog)

        self.findAction = QAction('Find', self)
        self.findAction.triggered.connect(self.findDialog.show)

        self.toolBar = self.addToolBar('ToolBar')
        self.toolBar.setObjectName('ToolBar')

        self.swapDicAction = self.toolBar.addWidget(self.dicComboBox)
        self.swapDicAction.setShortcut('F1')
        self.swapDicAction.triggered.connect(self.swapDic)

        self.toolBar.addSeparator()
        self.toolBar.addAction(self.backAction)
        self.toolBar.addAction(self.forwardAction)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.fontAction)
        self.toolBar.addAction(self.aboutAction)

        self.ui = DicWidget()
        self.ui.lineEdit.textChanged.connect(self.updateListWidget)
        self.ui.lineEdit.returnPressed.connect(self.updateTextBrowser)
        self.ui.listWidget.currentTextChanged.connect(self.updateTextBrowser)
        self.ui.textBrowser.textChanged.connect(self.textBrowserTextChanged)
        self.ui.textBrowser.addAction(self.findAction)
        self.ui.textBrowser.setContextMenuPolicy(Qt.ActionsContextMenu)

        self.highlighter = DicHighlighter(self.ui.textBrowser.document())

        self.setCentralWidget(self.ui)

        self.progressBar = QProgressBar()
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(0)
        self.statusBar().addPermanentWidget(self.progressBar)

        self.wordBuffer = deque(maxlen=WORD_BUFFER_SIZE)
        self.wordBufferIndex = -1
        self.currentDicIndex = -1;

        self.dictionaryLoader = DictionaryLoader(self)
        self.dictionaryLoader.finished.connect(self.loadingFinished)
        self.dictionaryLoader.loadingError.connect(self.loadingError)

        settings = QSettings()
        self.restoreGeometry(settings.value(SETTINGS_GEOMETRY).toByteArray())
        self.restoreState(settings.value(SETTINGS_MAIN_WINDOW_STATE).toByteArray())

        defFamily = QVariant(DEF_FONT_FAMILY)
        family = settings.value(SETTINGS_FONT_FAMILY, defFamily).toString()

        defPointSize = QVariant(DEF_FONT_POINT_SIZE)
        pointSize, ok = settings.value(SETTINGS_FONT_POINT_SIZE, defPointSize).toInt()
        if not ok:
            pointSize = DEF_FONT_POINT_SIZE

        defIsBold = QVariant(False)
        isBold = settings.value(SETTINGS_FONT_IS_BOLD, defIsBold).toBool()

        font = QFont()
        font.setFamily(family)
        font.setPointSize(pointSize)
        if isBold:
            font.setBold(True)
        self.setFont(font)

        self.load(0)

    def showFontDialog(self):
        font, ok = QFontDialog.getFont(self.font())
        if ok:
            self.setFont(font)

    def textBrowserTextChanged(self):
        self.findDialog.text = unicode(self.ui.textBrowser.toPlainText())

    def match(self, start, end):
        cursor = self.ui.textBrowser.textCursor()
        cursor.setPosition(start)
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, end - start)
        self.ui.textBrowser.setTextCursor(cursor)

    def swapDic(self):
        self.currentDicIndex = (self.currentDicIndex + 1) % 2
        self.dicComboBox.setCurrentIndex(self.currentDicIndex)

    def loadingError(self, e):
        QMessageBox.warning(self, 'Error', str(e))
        self.close()

    def about(self):
        text = '''
        <b>My Dictionary</b> v %s
        <p>Copyright &copy; 2015 Boyan Belakov.<br/>
        e-mail: belako.pl@gmail.com</p>
        Python %s - Qt %s - PyQt %s on %s
        ''' % (__version__, platform.python_version(), QT_VERSION_STR, PYQT_VERSION_STR, platform.system())
        QMessageBox.about(self, 'About My Dictionary', text)

    def forward(self):
        self.wordBufferIndex += 1
        translation = self.wordBuffer[self.wordBufferIndex][1]
        self.ui.textBrowser.setText(translation)

        if self.wordBufferIndex == len(self.wordBuffer) - 1:
            self.forwardAction.setEnabled(False)
        self.backAction.setEnabled(True)

    def back(self):
        self.wordBufferIndex -= 1
        translation = self.wordBuffer[self.wordBufferIndex][1]
        self.ui.textBrowser.setText(translation)

        if self.wordBufferIndex == 0:
            self.backAction.setEnabled(False)
        self.forwardAction.setEnabled(True)

    def updateTextBrowser(self, word=None):
        if word is None:
            word = self.ui.lineEdit.text()
        if len(word) == 0:
            return
        word = unicode(word).upper()

        for w, t in self.wordBuffer:
            if w == word:
                self.ui.textBrowser.setText(t)
                return

        if not self.isAlphabetText(word):
            self.ui.textBrowser.setText('<b><font color=red>Unsupported character</font></b>')
            return

        translation = self.dictionaryLoader.myDictionary.translate(word)
        if (translation is None):
            self.ui.textBrowser.setText('<b><font color=red>Word not found</font></b>')
        else:
            self.ui.textBrowser.setText(translation)

            self.wordBuffer.append((word, translation))
            if len(self.wordBuffer) > 1:
                self.backAction.setEnabled(True)
            self.wordBufferIndex = len(self.wordBuffer) - 1
            self.forwardAction.setEnabled(False)

    def closeEvent(self, event):
        settings = QSettings()
        settings.setValue(SETTINGS_MAIN_WINDOW_STATE, QVariant(self.saveState()))
        settings.setValue(SETTINGS_GEOMETRY, QVariant(self.saveGeometry()))

        font = self.font()
        settings.setValue(SETTINGS_FONT_FAMILY, QVariant(font.family()))
        settings.setValue(SETTINGS_FONT_POINT_SIZE, QVariant(font.pointSize()))
        settings.setValue(SETTINGS_FONT_IS_BOLD, QVariant(font.bold()))

        QMainWindow.closeEvent(self, event)

    def updateListWidget(self, text):
        self.ui.listWidget.clear()

        text = unicode(text).upper()
        if not self.isAlphabetText(text):
            return

        results = self.dictionaryLoader.myDictionary.keys_with_prefix(text, MAX_RESULTS)
        if len(results) == 0:
            s = self.dictionaryLoader.myDictionary.longest_prefix_of(text)
            if len(s) != 0:
                results.append(s)
        self.ui.listWidget.addItems(results)

    def isAlphabetText(self, text):
        if not text:
            return False
        alphabet = self.dictionaryLoader.myDictionary.alphabet()
        count = 0
        for c in text:
            if alphabet.contains(c):
                count += 1
        return count == len(text)

    def loadingFinished(self):
        self.ui.setEnabled(True)
        self.toolBar.setEnabled(True)
        self.statusBar().showMessage('Loading finished', 3000)
        self.ui.lineEdit.setFocus()
        self.progressBar.setVisible(False)

    def load(self, dicIndex):
        self.currentDicIndex = dicIndex
        self.ui.setEnabled(False)
        self.toolBar.setEnabled(False)
        self.statusBar().showMessage('Please wait...')
        self.ui.listWidget.clear()
        self.progressBar.setVisible(True)

        if dicIndex == 0:
            self.dictionaryLoader.create = dictionaries.en_bg
        elif dicIndex == 1:
            self.dictionaryLoader.create = dictionaries.bg_en
        self.dictionaryLoader.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('mydic')
    app.setOrganizationDomain('boyanbelakov.com')
    app.setOrganizationName('Boyan Belakov Soft')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

