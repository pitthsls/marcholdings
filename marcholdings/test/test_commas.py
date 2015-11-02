import datetime
import unittest

from marcholdings import parse_holdings


class TestDateParsingFunctional(unittest.TestCase):
    def test_simple_start_date(self):
        holdings = parse_holdings("v.1(2010)-")
        self.assertEqual(holdings[0].start_date, datetime.date(2010, 1, 1))
        self.assertIsNone(holdings[0].end_date)

    def test_single_year(self):
        holdings = parse_holdings("v.1(1990)")
        self.assertEqual(holdings[0].start_date, datetime.date(1990, 1, 1))
        self.assertEqual(holdings[0].end_date, datetime.date(1990, 12, 31))
        self.assertEqual(len(holdings), 1)

    def test_partial_year(self):
        holdings = parse_holdings("v.1:no.2-4(1990:Feb.-Apr.)")
        self.assertEqual(holdings[0].start_date, datetime.date(1990, 2, 1))
        self.assertEqual(holdings[0].end_date, datetime.date(1990, 4, 30))
        self.assertEqual(len(holdings), 1)

    def test_complex_dates(self):
        holdings = parse_holdings("v.2:no.3-v.6:no.5(2002:Mar.-2006:May")
        self.assertEqual(holdings[0].start_date, datetime.date(2002, 3, 1))
        self.assertEqual(holdings[0].end_date, datetime.date(2006, 5, 31))
        self.assertEqual(len(holdings), 1)

    def test_with_days(self):
        holdings = parse_holdings(
            "v.2:no.3-v.6:no.5(2002:Mar. 2-2006:May 6")
        self.assertEqual(holdings[0].start_date, datetime.date(2002, 3, 2))
        self.assertEqual(holdings[0].end_date, datetime.date(2006, 5, 6))
        self.assertEqual(len(holdings), 1)

    def test_with_comma_simple(self):
        holdings = parse_holdings("v.1,3(1999,2001)")
        self.assertEqual(holdings[0].start_date, datetime.date(1999, 1, 1))
        self.assertEqual(holdings[0].end_date, datetime.date(1999, 12, 31))
        self.assertEqual(holdings[1].start_date, datetime.date(2001, 1, 1))
        self.assertEqual(holdings[1].end_date, datetime.date(2001, 12, 31))
        self.assertEqual(len(holdings), 2)

    def test_with_comma_date_only(self):
        holdings = parse_holdings("1999,2001")
        self.assertEqual(holdings[0].start_date, datetime.date(1999, 1, 1))
        self.assertEqual(holdings[0].end_date, datetime.date(1999, 12, 31))
        self.assertEqual(holdings[1].start_date, datetime.date(2001, 1, 1))
        self.assertEqual(holdings[1].end_date, datetime.date(2001, 12, 31))
        self.assertEqual(len(holdings), 2)

    def test_comma_ugly(self):
        holdings = parse_holdings(
            'v.1:no.3,5-6(1982:May/June,Sept./Oct.-Nov./Dec.)')
        self.assertEqual(len(holdings), 2)
        self.assertEqual(holdings[0].start_date, datetime.date(1982, 5, 1))
        self.assertEqual(holdings[0].end_date, datetime.date(1982, 6, 30))
        self.assertEqual(holdings[1].start_date, datetime.date(1982, 9, 1))
        self.assertEqual(holdings[1].end_date, datetime.date(1982, 12, 31))

    def test_with_semicolon_simple(self):
        holdings = parse_holdings("v.1;3(1999;2001)")
        self.assertEqual(holdings[0].start_date, datetime.date(1999, 1, 1))
        self.assertEqual(holdings[0].end_date, datetime.date(1999, 12, 31))
        self.assertEqual(holdings[1].start_date, datetime.date(2001, 1, 1))
        self.assertEqual(holdings[1].end_date, datetime.date(2001, 12, 31))
        self.assertEqual(len(holdings), 2)
