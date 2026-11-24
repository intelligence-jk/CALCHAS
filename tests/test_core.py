from fractions import Fraction as F

import pytest

from qfreq import read_rows, summarise
from qfreq.__main__ import main

DATA = """year,topic,marks
2021,quadratics,3
2021,probability,2
2022,quadratics,4
2022,quadratics,2
2022,circles,5
2023,probability,3
2023,circles,4
2023,circles,1
2023,quadratics,2
"""


def test_counts_and_shares_exact():
    s = {x.topic: x for x in summarise(read_rows(DATA))}
    assert s["quadratics"].questions == 4 and s["quadratics"].marks == 11
    assert s["circles"].questions == 3 and s["circles"].marks == 10
    assert s["probability"].questions == 2
    assert s["quadratics"].share == F(4, 9)
    assert sum(x.share for x in s.values()) == 1


def test_years_present_and_gap():
    s = {x.topic: x for x in summarise(read_rows(DATA))}
    assert (s["quadratics"].years_present, s["quadratics"].years_total) == (3, 3)
    assert s["probability"].year_rate == F(2, 3)
    assert s["probability"].last_year == 2023 and s["probability"].years_since == 0


def test_gap_when_topic_missing_recently():
    rows = read_rows("year,topic\n2020,a\n2021,b\n2022,b\n")
    s = {x.topic: x for x in summarise(rows)}
    assert s["a"].years_since == 2 and s["a"].year_rate == F(1, 3)


def test_order_most_first_then_name():
    names = [x.topic for x in summarise(read_rows(DATA))]
    assert names == ["quadratics", "circles", "probability"]


def test_topic_case_folded_and_marks_default():
    rows = read_rows("year,topic\n2020,Circles\n2021, circles \n")
    assert [r.topic for r in rows] == ["circles", "circles"] and rows[0].marks == 1


@pytest.mark.parametrize(
    "bad",
    ["topic\nx\n", "year,topic\nabc,x\n", "year,topic\n2020,\n", "year,topic,marks\n2020,x,-1\n", "year,topic\n"],
)
def test_bad_input(bad):
    with pytest.raises(ValueError):
        read_rows(bad)


def test_cli(tmp_path, capsys):
    f = tmp_path / "c.csv"
    f.write_text(DATA)
    assert main([str(f)]) == 0
    out = capsys.readouterr().out.splitlines()
    assert out[1].startswith("quadratics") and "44.4%" in out[1]
