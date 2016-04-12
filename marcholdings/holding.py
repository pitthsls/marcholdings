"""MARC holdings"""

import calendar
from collections import deque
import datetime
import re


class Holding(object):
    """Holdings information from a MARC record

    Args:
        start_date (datetime.date): date holdings begin.
        end_date (Optional[datetime.date]): date holdings end.

    """
    def __init__(self, start_date=None, end_date=None):
        self.start_date = start_date
        self.end_date = end_date

    @classmethod
    def from_text(cls, text_holding):
        """Create a Holding from Z39.71 non-gap text holding

        Args:
            text_holding (str): text of a non-gap holding

        Returns:
            Holding: a Holding object

        """
        date_part = ''
        if '(' not in text_holding and text_holding[0:4].isdigit():
            date_part = text_holding
        elif '(' in text_holding:
            date_part = text_holding.split('(')[1].split(')')[0]
        if text_holding.endswith('-'):
            end_date = None
            if date_part:
                start_date = parse_date(date_part.rstrip('-'))
            else:
                start_date = None
        else:
            parts = date_part.split('-')
            start = parts[0]
            end = parts[1] if len(parts) > 1 else parts[0]
            if (':' not in end and not end.isdigit() and
                    not all(x.isdigit() for x in end.split('/'))):
                end = start[0:5] + end
            if date_part == '':
                start_date = None
                end_date = None
            else:
                start_date = parse_date(start)
                end_date = parse_date(end, True)
        return cls(start_date, end_date)

def parse_date(date_string, end=False):
    """Parse a date string in Z39.71 format

    Args:
        date_string (str): date in Z39.71 format
        end (bool): whether date represents the end of a range

    Returns:
        datetime.date: parsed date
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

    Args:
        season_text (str): name of season
        end (bool): whether we're looking for end of season

    Returns:
        int: month number
    """
    seasons = {
        'fall': (9, 12),
        'autumn': (9, 12),
        'winter': (12, 3),
        'spring': (3, 6),
        'summer': (6, 9),
    }
    return seasons[season_text.lower()][end]


def parse_holdings(text_holdings):
    """Parse a holdings statement.

    Accepts a MARC holdings statement, possibly with gaps, and returns a list
    of Holding objects.

    Args:
        text_holdings (str): textual holdings

    Returns:
        List[Holding]: non-gap holdings objects
    """
    return [Holding.from_text(th) for th in _comma_split(text_holdings)]


def _comma_split(text_holdings):
    """Split a holding with commas into parts.

    Args:
        text_holdings (str): textual holding

    Returns:
        List[str]: holding text without commas, separated
    """
    parts = []
    holding_open = text_holdings.endswith('-')
    paren_split = text_holdings.split('(')
    if len(paren_split) > 1:
        enums = paren_split[0]
        chrons = paren_split[1].split(')')[0]
    else:
        if paren_split[0][0:4].isdigit():
            chrons = paren_split[0]
            enums = None
        else:
            enums = paren_split[0]
            chrons = None
    enumlist = []
    if enums:
        esplit = deque(re.split('([ .,:;])', enums))
        ec1 = ''.join([esplit.popleft(), esplit.popleft()])
        accum = ec1
        while esplit:
            accum += esplit.popleft()
            if not esplit or esplit[0] in ',;':
                enumlist.append(accum)
                accum = ec1
                if esplit:
                    esplit.popleft()

    chronlist = []
    if chrons:
        csplit = deque(re.split('([,:;])', chrons))
        caccum = ''
        deep = False
        while csplit:
            token = csplit.popleft()
            caccum += token
            if token == ':':
                deep = True
            if not csplit or csplit[0] in ',;':
                chronlist.append(caccum)
                if not deep or (csplit and csplit[1].isnumeric()):
                    caccum = ''
                    deep = False
                else:
                    caccum = caccum.split(':')[0] + ':'
                if csplit:
                    csplit.popleft()
    if enumlist and chronlist:
        for i, val in enumerate(enumlist):
            parts.append("%s(%s)" % (val, chronlist[i]))
    elif chronlist:
        parts = chronlist
    else:
        parts = enumlist
    if holding_open:
        parts[-1] += "-"
    return parts
