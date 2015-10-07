import unittest

from marcholdings.helpers import split_enum


class TestCaptions(unittest.TestCase):
    def test_simple_vol(self):
        sc = split_enum('v.1')
        self.assertEqual(sc.caption, 'v.')
        self.assertEqual(sc.enumeration, '1')

    def test_space(self):
        sc = split_enum('issue 1')
        self.assertEqual(sc.caption, 'issue')
        self.assertEqual(sc.enumeration, '1')

    def test_multipart(self):
        sc = split_enum('v.1A')
        self.assertEqual(sc.caption, 'v.')
        self.assertEqual(sc.enumeration, '1A')

    def test_backward(self):
        sc = split_enum('1st ed.')
        self.assertEqual(sc.caption, 'ed.')
        self.assertEqual(sc.enumeration, '1')
