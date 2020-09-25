import pytest

import marcholdings


@pytest.mark.parametrize(
    ["holding"], [("v.1(2010)",), ("v.1(2010)-",), ("v.1-2(2010-2011)",),]
)
def test_string_roundtrip(holding):
    assert holding == str(marcholdings.Holding.from_text(holding))
