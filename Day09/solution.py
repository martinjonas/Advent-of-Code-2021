import aocutils.input
import aocutils.parsing
import sys
from functools import reduce
import operator


def get_neighbors(point):
    (h, v) = point
    yield (h + 1, v)
    yield (h - 1, v)
    yield (h, v + 1)
    yield (h, v - 1)


def get_lowpoints(plan):
    return [
        (pos, val)
        for pos, val in plan.items()
        if all(plan[n] > val for n in get_neighbors(pos) if n in plan)
    ]


def part1(plan):
    return sum(val + 1 for _, val in get_lowpoints(plan))


def part2(plan):
    def get_basin_size(start):
        seen = set([start])
        to_process = [start]
        while to_process:
            cur = to_process.pop()
            for n in get_neighbors(cur):
                if n in plan and n not in seen and plan[n] != 9:
                    seen.add(n)
                    to_process.append(n)
        return len(seen)

    lowpoints = [point for point, _ in get_lowpoints(plan)]
    basin_sizes = list(map(get_basin_size, lowpoints))
    basin_sizes.sort(reverse=True)

    return reduce(operator.mul, basin_sizes[0:3])


def main():
    input_file = "input"
    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    data = aocutils.input.read_lines(input_file)

    plan = {}
    for v, row in enumerate(data):
        for h, cell in enumerate(row):
            plan[(v, h)] = int(cell)

    print(part1(plan))
    print(part2(plan))


main()
