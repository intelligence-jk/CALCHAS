"""Count how often topics appear across papers. Counts only: no question text is read or stored.

Input is your own list, one row per question: year,topic[,marks]
"""
from __future__ import annotations

import csv
import io
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Row:
    year: int
    topic: str
    marks: int = 1


@dataclass(frozen=True)
class TopicStats:
    topic: str
    questions: int
    marks: int
    years_present: int
    years_total: int
    last_year: int
    years_since: int
    share: Fraction  # of all questions

    @property
    def year_rate(self) -> Fraction:
        """Fraction of the years in which the topic appeared at least once."""
        return Fraction(self.years_present, self.years_total)


def read_rows(text: str) -> list[Row]:
    rows = []
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames or not {"year", "topic"} <= {f.strip() for f in reader.fieldnames}:
        raise ValueError("the file needs a header row with at least: year,topic")
    for n, r in enumerate(reader, 2):
        r = {k.strip(): (v or "").strip() for k, v in r.items() if k}
        try:
            year = int(r["year"])
            marks = int(r["marks"]) if r.get("marks") else 1
        except ValueError:
            raise ValueError(f"line {n}: year and marks must be whole numbers")
        if not r["topic"]:
            raise ValueError(f"line {n}: topic is empty")
        if marks < 0:
            raise ValueError(f"line {n}: marks cannot be negative")
        rows.append(Row(year, r["topic"].lower(), marks))
    if not rows:
        raise ValueError("no rows found")
    return rows


def summarise(rows: list[Row]) -> list[TopicStats]:
    """One entry per topic, most questions first (ties: more years, then name)."""
    years = sorted({r.year for r in rows})
    latest = years[-1]
    total = len(rows)
    out = []
    for topic in sorted({r.topic for r in rows}):
        mine = [r for r in rows if r.topic == topic]
        yrs = {r.year for r in mine}
        out.append(
            TopicStats(
                topic=topic,
                questions=len(mine),
                marks=sum(r.marks for r in mine),
                years_present=len(yrs),
                years_total=len(years),
                last_year=max(yrs),
                years_since=latest - max(yrs),
                share=Fraction(len(mine), total),
            )
        )
    out.sort(key=lambda s: (-s.questions, -s.years_present, s.topic))
    return out
