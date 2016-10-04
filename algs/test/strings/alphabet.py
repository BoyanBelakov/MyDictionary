# -*- coding:utf-8 -*-

import unittest
from algs.strings.alphabet import Alphabet, AlphabetException

__author__ = 'boyan'


class AlphabetTest(unittest.TestCase):
    def test_empty_alphabet(self):
        self.assertRaises(AlphabetException, Alphabet, '')

    def test_duplicate_chars(self):
        self.assertRaises(AlphabetException, Alphabet, 'aba')

    def test_contains(self):
        a = Alphabet(u'QЯ')
        self.assertTrue(a.contains('Q'))
        self.assertTrue(a.contains(u'Я'))
        self.assertFalse(a.contains('z'))

    def test_to_index(self):
        a = Alphabet("abcdefghijklmnopqrstuvwxyz")
        self.assertEqual(0, a.to_index('a'))
        self.assertEqual(25, a.to_index('z'))

        self.assertRaises(AlphabetException, a.to_index, 'A')
        self.assertRaises(AlphabetException, a.to_index, u'Я')

    def test_to_char(self):
        a = Alphabet("0123456789")
        self.assertEqual('0', a.to_char(0))
        self.assertEqual('9', a.to_char(9))

        self.assertRaises(AlphabetException, a.to_char, 10)
        self.assertRaises(AlphabetException, a.to_char, 11)
        self.assertRaises(AlphabetException, a.to_char, -1)

    def test_radix(self):
        a = Alphabet("01")
        self.assertEqual(2, a.radix())

    def test_unicode16(self):
        char_max_val = 65536
        chars = [unichr(i) for i in range(char_max_val+1)]
        self.assertRaises(AlphabetException, Alphabet, chars)

    def runTest(self):
        self.test_empty_alphabet()
        self.test_contains()
        self.test_duplicate_chars()
        self.test_radix()
        self.test_to_char()
        self.test_to_index()
        self.test_unicode16()

if __name__ == '__main__':
    unittest.main()
