"""helper functions for marcholdings"""
from collections import namedtuple
import re

SplitEnum = namedtuple("SplitEnum", ["caption", "enumeration"])


def split_whole_enum(enumeration):
    """split a whole enum into volume and issue."""
    vol, _, iss = enumeration.partition(":")
    return tuple(split_enum(x).enumeration for x in (vol, iss))


def split_enum(enumeration):
    """split a textual enumeration into its caption and enumeration parts

    :param enumeration: the textual enumeration to be split
    """
    parts = ["", enumeration]
    if "." in enumeration[1:-1]:
        parts = enumeration.split(".", 1)
        parts[0] += "."
    elif " " in enumeration:
        parts = enumeration.split(" ", 1)
        if parts[0][0].isdigit():
            parts.reverse()
            parts[1] = trim_ordinal(parts[1])
    return SplitEnum(*parts)


def trim_ordinal(ordinal):
    """trim the suffix of an ordinal number off

    :param ordinal: ordinal number to trim
    """
    return re.sub(r"(st|nd|rd|th)$", "", ordinal)
