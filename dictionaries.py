# coding=utf-8
import os
from algs.strings.alphabet import Alphabet
from algs.strings.trie_st import TrieST

__author__ = 'boyan'

ENCODING = 'cp1251'


class MyDictionary:
    def __init__(self, filename, trieST):
        self._filename = filename
        self._st = trieST
        self._load()

    def alphabet(self):
        return self._st.alphabet()

    def keys_with_prefix(self, text, maxResults):
        return self._st.keys_with_prefix(text, maxResults)

    def longest_prefix_of(self, text):
        return self._st.longest_prefix_of(text)

    def translate(self, word):
        offset = self._st.get(word)
        if offset is None:
            return None

        with open(self._filename, "rb") as fh:
            fh.seek(offset)
            textBuilder = ['<b><font color=green>%s</font></b>' % word]
            while True:
                line = fh.readline().decode(ENCODING)
                if not line:
                    break
                index = line.find('\0')
                if index != -1:
                    textBuilder.append(line[:index])
                    break
                else:
                    textBuilder.append(line[:-1])
            return '<br />'.join(textBuilder)

    def _load(self):
        with open(self._filename, "rb") as fh:
            st = self._st
            while True:
                line = fh.readline()
                if not line:
                    break
                index = line.find('\0')
                if index != -1:
                    key = line[index + 1:-1]
                    val = fh.tell()
                    st.put(key.decode(ENCODING), val)


def en_bg():
    dir_ = os.path.dirname(__file__)
    filename = os.path.join(dir_, 'res', 'data', 'en_bg.dat')

    alphabet = Alphabet(u"ABCDEFGHIJKLMNOPQRSTUVWXYZ '-")
    st = TrieST(alphabet)

    return MyDictionary(filename, st)


def bg_en():
    dir_ = os.path.dirname(__file__)
    filename = os.path.join(dir_, 'res', 'data', 'bg_en.dat')

    alphabet = Alphabet(u"АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЬЮЯ '-")
    st = TrieST(alphabet)

    return MyDictionary(filename, st)
