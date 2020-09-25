import pytest

import marcholdings


@pytest.mark.parametrize(
    ["holding"],
    [
        ("v.1(2010)",),
        ("v.1(2010)-",),
        ("v.1-2(2010-2011)",),
        ("v.1:no.1-3",),
        ("v.2:no.3-v.6:no.5(2002:Mar.-2006:May)",),
        ("v.1",),
        ("v.1:no.2(2016:Feb.)-",),
    ],
)
def test_string_roundtrip(holding):
    assert holding == str(marcholdings.Holding.from_text(holding))
