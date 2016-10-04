# coding=utf-8
import re
from PyQt4.QtCore import *
from PyQt4.QtGui import *

__author__ = 'boyan'


class FindDialog(QDialog):
    match = pyqtSignal(int, int)

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.text = ''
        self._results = []
        self._index = -1

        self.findLineEdit = QLineEdit()
        self.findLineEdit.setPlaceholderText('Enter text')
        self.findLineEdit.setMinimumWidth(150)

        self.caseSensitiveCheckBox = QCheckBox('&Case sensitive')
        self.caseSensitiveCheckBox.setChecked(True)

        self.wholeWordsCheckBox = QCheckBox('Wh&ole words')
        self.infoLabel = QLabel()

        self.findButton = QPushButton('&Find')
        self.findButton.setEnabled(False)

        self.nextButton = QPushButton('&Next')
        self.nextButton.setEnabled(False)

        self.prevButton = QPushButton('&Prev')
        self.prevButton.setEnabled(False)

        buttonBox = QVBoxLayout()
        buttonBox.addWidget(self.findButton)
        buttonBox.addStretch()
        buttonBox.addWidget(self.nextButton)
        buttonBox.addWidget(self.prevButton)

        grid = QGridLayout()
        grid.addWidget(self.findLineEdit, 0, 0)
        grid.addWidget(self.caseSensitiveCheckBox, 1, 0)
        grid.addWidget(self.wholeWordsCheckBox, 2, 0)
        grid.addLayout(buttonBox, 0, 1, 3, 1)
        grid.addWidget(self.infoLabel, 3, 0, 1, 2)
        self.setLayout(grid)

        self.findLineEdit.textChanged.connect(self._textChanged)
        self.findLineEdit.returnPressed.connect(self._find)
        self.findButton.clicked.connect(self._find)
        self.nextButton.clicked.connect(self._next)
        self.prevButton.clicked.connect(self._prev)

    def _textChanged(self, text):
        self.findButton.setEnabled(not text.isEmpty())

    def _next(self):
        self._index += 1
        self._updateUi()

    def _prev(self):
        self._index -= 1
        self._updateUi()

    def _find(self):
        patten = self.findLineEdit.text()
        if patten.isEmpty():
            return
        patten = _escape(unicode(patten))

        flags = re.UNICODE if self.caseSensitiveCheckBox.isChecked() else re.UNICODE | re.IGNORECASE

        if self.wholeWordsCheckBox.isChecked():
            patten = r'\b%s\b' % patten

        self._results = [m for m in re.compile(patten, flags).finditer(self.text)]

        if len(self._results) != 0:
            self._index = 0
        else:
            self._index = -1

        self._updateUi()

    def _updateUi(self):
        length = len(self._results)
        if length == 0:
            self.infoLabel.setText('Not found')
            self.nextButton.setEnabled(False)
            self.prevButton.setEnabled(False)
        elif length == 1:
            self.infoLabel.setText('1 match')
            self.nextButton.setEnabled(False)
            self.prevButton.setEnabled(False)

            match = self._results[0]
            start, end = match.span()
            self.match.emit(start, end)
        else:
            self.infoLabel.setText('%s of %s matches' % (self._index + 1, length))

            self.nextButton.setEnabled(-1 < self._index < length - 1)
            self.prevButton.setEnabled(0 < self._index < length)

            match = self._results[self._index]
            start, end = match.start(), match.end()
            self.match.emit(start, end)


def _escape(text):
    s = list(text)
    alphanum = u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789' \
               u'абвгдежзийклмнопрстуфхцчшщъьюяАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЬЮЯ'

    for i, c in enumerate(text):
        if c not in alphanum:
            s[i] = u"\\" + c
    return u''.join(s)
