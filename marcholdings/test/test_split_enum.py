import unittest

from marcholdings.helpers import split_enum


class TestCaptions(unittest.TestCase):
    def test_simple_vol(self):
        splitparts = split_enum("v.1")
        self.assertEqual(splitparts.caption, "v.")
        self.assertEqual(splitparts.enumeration, "1")

    def test_space(self):
        splitparts = split_enum("issue 1")
        self.assertEqual(splitparts.caption, "issue")
        self.assertEqual(splitparts.enumeration, "1")

    def test_multipart(self):
        splitparts = split_enum("v.1A")
        self.assertEqual(splitparts.caption, "v.")
        self.assertEqual(splitparts.enumeration, "1A")

    def test_backward(self):
        splitparts = split_enum("1st ed.")
        self.assertEqual(splitparts.caption, "ed.")
        self.assertEqual(splitparts.enumeration, "1")

    def test_no_caption(self):
        splitparts = split_enum("2")
        self.assertEqual(splitparts.enumeration, "2")
