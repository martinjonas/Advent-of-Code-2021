import aocutils.input
import aocutils.parsing
import sys
import collections
from itertools import repeat

def incl_range(f, t, step):
    return repeat(f) if step == 0 else range(f, t+step, step)


def part2(data):
    counts = collections.Counter()

    for (x1, y1, x2, y2) in data:
        dx = 1 if x2 > x1 else (-1 if x2 < x1 else 0)
        dy = 1 if y2 > y1 else (-1 if y2 < y1 else 0)
        counts.update(zip(incl_range(x1, x2, dx), incl_range(y1, y2, dy)))

    return sum(1 for v in counts.values() if v >= 2)


def part1(data):
    return part2((x1, y1, x2, y2)
                 for (x1, y1, x2, y2) in data
                 if x1 == x2 or y1 == y2)


def main():
    input_file = "input"
    if (len(sys.argv) > 1):
        input_file = sys.argv[1]

    data = aocutils.input.read_lines(input_file)
    data = [list(map(int, aocutils.parsing.break_words(line)))
            for line in data]

    print(part1(data))
    print(part2(data))


main()
