from alphabet import Alphabet


class Node:
    def __init__(self, r):
        self.val = None
        self.alphabet = [None] * r


class TrieST:
    def __init__(self, alphabet=Alphabet()):
        self._alphabet = alphabet
        self._root = None
        self._R = alphabet.radix()
        self._N = 0

    def alphabet(self):
        return self._alphabet

    def size(self):
        return self._N

    def put(self, key, val):
        if val is None:
            raise ValueError("val is None")
        else:
            self._root = self._put(self._root, key, val, 0)

    def _put(self, node, key, val, d):
        if node is None:
            node = Node(self._R)
        if d == len(key):
            if node.val is None:
                self._N += 1
            node.val = val
            return node

        c = key[d]
        i = self._alphabet.to_index(c)
        node.alphabet[i] = self._put(node.alphabet[i], key, val, d + 1)

        return node

    def get(self, key):
        node = self._get(self._root, key, 0)
        if node is None:
            return None
        return node.val

    def _get(self, node, key, d):
        if node is None:
            return None
        if d == len(key):
            return node
        c = key[d]
        i = self._alphabet.to_index(c)
        return self._get(node.alphabet[i], key, d + 1)

    def keys(self):
        results = []
        self._travel(self._root, '', results, -1)
        return results

    def keys_with_prefix(self, pre, maxResults=-1):
        results = []
        node = self._get(self._root, pre, 0)
        self._travel(node, pre, results, maxResults)
        return results

    def _travel(self, node, pre, results, maxResults):
        if node is None:
            return
        if maxResults == len(results):
            return
        if node.val is not None:
            results.append(pre)

        for i in range(self._R):
            c = self._alphabet.to_char(i)
            self._travel(node.alphabet[i], pre + c, results, maxResults)

    def longest_prefix_of(self, s):
        length = self._longest_prefix_of(self._root, s, 0, 0)
        return s[:length]

    def _longest_prefix_of(self, node, s, d, length):
        if node is None:
            return length
        if node.val is not None:
            length = d
        if d == len(s):
            return length

        c = s[d]
        i = self._alphabet.to_index(c)
        return self._longest_prefix_of(node.alphabet[i], s, d + 1, length)
