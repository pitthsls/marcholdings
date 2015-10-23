"""MARC holdings"""

import calendar
import datetime
import re


class Holding(object):
    """Holdings information from a MARC record

    :param text_holding: text of a non-gap holding
    """
    def __init__(self, text_holding):
        date_part = None
        if '(' not in text_holding:
            date_part = text_holding
        else:
            date_part = text_holding.split('(')[1].split(')')[0]
        if text_holding.endswith('-'):
            self.end_date = None
            self.start_date = parse_date(date_part.rstrip('-'))
        else:
            parts = date_part.split('-')
            start = parts[0]
            end = parts[1] if len(parts) > 1 else parts[0]
            if (':' not in end and not end.isdigit() and
                    not all(x.isdigit() for x in end.split('/'))):
                end = start[0:5] + end
            self.start_date = parse_date(start)
            self.end_date = parse_date(end, True)


def parse_date(date_string, end=False):
    """Parse a date string in Z39.71 format, return a datetime.date

    :param date_string: date in Z39.71 format
    :param end: Boolean; whether date represents the end of a range
    """
    months = [None, 'Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'June', 'July',
              'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.', ]
    parts = re.split('[: ]', date_string)
    text_year = parts[0]
    if '/' in text_year:
        text_year = text_year.split('/')[1 if end else 0]
    year = int(text_year)
    month = 1
    if len(parts) > 1:
        month_text = parts[1]
        if '/' in month_text:
            month_text = month_text.split('/')[1 if end else 0]
        try:
            month = months.index(month_text)
        except ValueError:
            try:
                month = season_to_month(month_text, end)
            except ValueError:
                raise ValueError("Bad month/season: %s" % month_text)
    elif end:
        month = 12

    day = 1
    if len(parts) == 3:
        day = int(parts[2])
    elif end:
        day = calendar.monthrange(year, month)[1]

    return datetime.date(year, month, day)


def season_to_month(season_text, end):
    """Convert a season name to the correct month

    :param season_text: name of season
    :param end: bool; whether we're looking for end of season
    """
    seasons = {
        'fall': (9, 12),
        'winter': (12, 3),
        'spring': (3, 6),
        'summer': (6, 9),
    }
    return seasons[season_text][end]