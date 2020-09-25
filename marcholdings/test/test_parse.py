import datetime
import unittest

import marcholdings


class TestDateParsing(unittest.TestCase):
    def test_simple_start_date(self):
        holding = marcholdings.Holding.from_text("v.1(2010)-")
        self.assertEqual(holding.start_date, datetime.date(2010, 1, 1))
        self.assertIsNone(holding.end_date)
        self.assertEqual(holding.start_volume, "1")
        self.assertEqual(holding.end_volume, "")

    def test_single_year(self):
        holding = marcholdings.Holding.from_text("v.1(1990)")
        self.assertEqual(holding.start_date, datetime.date(1990, 1, 1))
        self.assertEqual(holding.end_date, datetime.date(1990, 12, 31))

    def test_partial_volume(self):
        holding = marcholdings.Holding.from_text("v.1:no.1-3")
        self.assertEqual(holding.start_volume, "1")
        self.assertEqual(holding.end_volume, "1")
        self.assertEqual(holding.start_issue, "1")
        self.assertEqual(holding.end_issue, "3")

    def test_partial_year(self):
        holding = marcholdings.Holding.from_text("v.1:no.2-4(1990:Feb.-Apr.)")
        self.assertEqual(holding.start_date, datetime.date(1990, 2, 1))
        self.assertEqual(holding.end_date, datetime.date(1990, 4, 30))

    def test_complex_dates(self):
        holding = marcholdings.Holding.from_text("v.2:no.3-v.6:no.5(2002:Mar.-2006:May")
        self.assertEqual(holding.start_date, datetime.date(2002, 3, 1))
        self.assertEqual(holding.end_date, datetime.date(2006, 5, 31))
        self.assertEqual(holding.start_volume, "2")
        self.assertEqual(holding.end_volume, "6")
        self.assertEqual(holding.start_issue, "3")
        self.assertEqual(holding.end_issue, "5")

    def test_complex_dates_june(self):
        holding = marcholdings.Holding.from_text("v.2:no.3-v.6:no.5(2002:June-2006:May")
        self.assertEqual(holding.start_date, datetime.date(2002, 6, 1))
        self.assertEqual(holding.end_date, datetime.date(2006, 5, 31))
        self.assertEqual(holding.start_volume, "2")
        self.assertEqual(holding.end_volume, "6")
        self.assertEqual(holding.start_issue, "3")
        self.assertEqual(holding.end_issue, "5")

    def test_with_days(self):
        holding = marcholdings.Holding.from_text(
            "v.2:no.3-v.6:no.5(2002:Mar. 2-2006:May 6"
        )
        self.assertEqual(holding.start_date, datetime.date(2002, 3, 2))
        self.assertEqual(holding.end_date, datetime.date(2006, 5, 6))

    def test_open_partial(self):
        holding = marcholdings.Holding.from_text("v.1:no.2(1990:Feb.)-")
        self.assertEqual(holding.start_date, datetime.date(1990, 2, 1))
        self.assertIsNone(holding.end_date)

    def test_open_year_only(self):
        holding = marcholdings.Holding.from_text("1990-")
        self.assertEqual(holding.start_date, datetime.date(1990, 1, 1))
        self.assertIsNone(holding.end_date)

    def test_multi_year_open(self):
        holding = marcholdings.Holding.from_text("1992/1996-")
        self.assertEqual(holding.start_date, datetime.date(1992, 1, 1))
        self.assertIsNone(holding.end_date)

    def test_multi_year_single_volume(self):
        holding = marcholdings.Holding.from_text("v.1(1840/1842)")
        self.assertEqual(holding.start_date, datetime.date(1840, 1, 1))
        self.assertEqual(holding.end_date, datetime.date(1842, 12, 31))

    def test_seasons(self):
        holding = marcholdings.Holding.from_text("v.1-2(1990:fall-2000:spring)")
        self.assertEqual(holding.start_date, datetime.date(1990, 9, 1))
        self.assertEqual(holding.end_date, datetime.date(2000, 6, 30))

    def test_ugly_comma(self):
        holding = marcholdings.Holding.from_text(
            "v.1:no.3,5-6(1982:May/June,Sept./Oct.-Nov./Dec.)-"
        )
        self.assertEqual(holding.start_date, datetime.date(1982, 5, 1))
        self.assertIsNone(holding.end_date)

    def test_volume_only_open(self):
        holding = marcholdings.Holding.from_text("v.1-")
        self.assertIsNone(holding.start_date)
        self.assertIsNone(holding.end_date)

    def test_volumes_only(self):
        holding = marcholdings.Holding.from_text("v.1-7")
        self.assertIsNone(holding.start_date)
        self.assertIsNone(holding.end_date)

    def test_volume_only(self):
        holding = marcholdings.Holding.from_text("v.1")
        self.assertIsNone(holding.start_date)
        self.assertIsNone(holding.end_date)
        self.assertEqual(holding.end_volume, "1")

    def test_parens(self):
        holding = marcholdings.Holding.from_text("(1998-2006)")
        self.assertEqual(holding.start_date, datetime.date(1998, 1, 1))
        self.assertEqual(holding.end_date, datetime.date(2006, 12, 31))
