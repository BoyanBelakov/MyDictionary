# -*- coding:utf-8 -*-

from algs.strings.trie_st import TrieST
import unittest


class TrieSTTest(unittest.TestCase):
    def test_put_none(self):
        st = TrieST()
        try:
            st.put('she', None)
        except ValueError:
            pass
        else:
            self.fail()

    def test_put_get_size_keys(self):
        st = TrieST()
        self.assertEqual(0, st.size())
        self.assertEqual(0, len(st.keys()))

        key = 'she'
        val = u'тя'
        st.put(key, val)

        self.assertEqual(val, st.get(key))
        self.assertEqual(1, st.size())
        self.assertTrue(st.get('shell') is None)

        key = 'shell'
        val = u'черупка'
        st.put(key, val)

        self.assertEqual(val, st.get(key))
        self.assertEqual(2, st.size())

        keys = st.keys()
        self.assertEqual(keys[0], 'she')
        self.assertEqual(keys[1], 'shell')

    def test_keys_with_prefix(self):
        st = TrieST()
        st.put('she', 0)
        st.put('shells', 1)
        st.put('sea', 3)
        st.put('sells', 4)
        st.put('shore', 5)
        st.put('by', 2)
        st.put('the', 6)

        for key in st.keys_with_prefix('sh'):
            print key

        self.assertEqual(0, len(st.keys_with_prefix('sort')))

    def test_longest_prefix_of(self):
        st = TrieST()
        st.put('she', 0)
        st.put('shells', 1)

        self.assertEqual('she', st.longest_prefix_of('she'))
        self.assertEqual('she', st.longest_prefix_of('shell'))
        self.assertEqual('shells', st.longest_prefix_of('shellsort'))
        self.assertEqual('she', st.longest_prefix_of('shelters'))
        self.assertEqual('', st.longest_prefix_of(''))
        self.assertEqual('', st.longest_prefix_of('he'))
        self.assertEqual('', st.longest_prefix_of('ell'))
        self.assertEqual('', st.longest_prefix_of('ells'))

if __name__ == '__main__':
    unittest.main()
