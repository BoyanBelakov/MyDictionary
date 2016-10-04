# coding=utf-8


class AlphabetException(Exception):
    pass


class Alphabet:
    def __init__(self, chars="abcdefghijklmnopqrstuvwxyz"):
        if len(chars) == 0:
            raise AlphabetException("alphabet can not be empty")
        char_max_value = 0xFFFF + 1
        checked = [False] * char_max_value
        for c in chars:
            i = ord(c)
            if i >= char_max_value:
                raise AlphabetException("char must be between U+0000 and U+FFFF: " + c)
            if checked[i]:
                raise AlphabetException("duplicate char: " + c)
            checked[i] = True

        self._chars = chars
        self._indexes = {c: i for i, c in enumerate(chars)}
        self._R = len(chars)

    def chars(self):
        return self._chars

    def contains(self, c):
        return c in self._indexes

    def to_index(self, c):
        if not self.contains(c):
            raise AlphabetException("character '%s' not in alphabet" % c)

        return self._indexes[c]

    def to_char(self, i):
        if i < 0 or i >= self._R:
            raise AlphabetException("alphabet index out of bounds: " + str(i))

        return self._chars[i]

    def radix(self):
        return self._R


def unicode16():
    return Alphabet([unichr(i) for i in range(65536)])


def extended_ascii():
    return Alphabet([chr(i) for i in range(256)])


def ascii():
    return Alphabet([chr(i) for i in range(128)])


def lower_case_en():
    return Alphabet("abcdefghijklmnopqrstuvwxyz")


def lower_case_bg():
    return Alphabet(u"абвгдежзийклмнопрстуфхцчшщъьюя")


def dna():
    return Alphabet("ACTG")


def hexadecimal():
    return Alphabet("0123456789ABCDEF")


def decimal():
    return Alphabet("0123456789")


def octal():
    return Alphabet("01234567")


def binary():
    return Alphabet("01")
