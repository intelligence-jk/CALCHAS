"""python -m qfreq counts.csv"""
import sys

from .core import read_rows, summarise


def main(argv=None) -> int:
    a = sys.argv[1:] if argv is None else argv
    if len(a) != 1:
        print("usage: python -m qfreq counts.csv", file=sys.stderr)
        return 2
    try:
        stats = summarise(read_rows(open(a[0]).read()))
    except (ValueError, OSError) as e:
        print(f"Cannot read counts: {e}", file=sys.stderr)
        return 1
    print(f"{'topic':20s} {'questions':>9s} {'marks':>6s} {'years':>7s} {'share':>7s} {'last seen':>9s}")
    for s in stats:
        print(
            f"{s.topic:20s} {s.questions:9d} {s.marks:6d} {s.years_present:>3d}/{s.years_total:<3d} "
            f"{float(s.share) * 100:6.1f}% {s.last_year:>9d}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
