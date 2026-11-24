# question-frequency

Count how often topics appear across a list of past papers you keep yourself. Counts only.

## What it solves
When you plan revision you want to know which topics come up most often and which have not appeared for a while. You keep a plain list, one row per question with its year and topic, and this gives the counts, the share of all questions, the number of years each topic appeared in, and how long since it was last seen. It never reads or stores question text, only the year, the topic label and optionally the marks. Pure Python 3.10+, standard library only, exact fractions.

## Example
`counts.csv` (your own tally; these rows are invented):
```
year,topic,marks
2021,quadratics,3
2021,probability,2
2022,quadratics,4
2022,quadratics,2
2022,circles,5
2023,probability,3
2023,circles,4
2023,circles,1
2023,quadratics,2
```
```bash
python -m qfreq counts.csv
```
```
topic                questions  marks   years   share last seen
quadratics                   4     11   3/3     44.4%      2023
circles                      3     10   2/3     33.3%      2023
probability                  2      5   2/3     22.2%      2023
```

## The maths behind it
The share of a topic is `questions of that topic / all questions`, held as an exact `Fraction` (here 4/9), so the shares add up to exactly 1. The "years" column is the number of different years the topic appeared in, out of all years in your list (a topic with 4 questions in one year counts once). "Years since" is the latest year in the list minus the topic's last year. These are counts of what happened in the papers you listed. A topic being frequent or absent for a while shows a pattern in your list; it does not say what a future paper will contain, so use it to order your revision, not to skip topics.

## Install and run
```bash
python -m pip install -e .
python -m qfreq counts.csv
python -m pytest
```

## Licence
MIT. Made by Math & Myth (mathandmyth.ae): one to one maths mentoring, online, across the UAE.
