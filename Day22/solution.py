import aocutils.input
import aocutils.parsing
import sys
import itertools
from functools import reduce
import re
from dataclasses import dataclass
import operator


@dataclass
class Hypercuboid:
    minpoint: list[int]
    maxpoint: list[int]

    def __contains__(self, point):
        return all(map(lambda p, lower, upper: lower <= p <= upper,
                       point, self.minpoint, self.maxpoint))


def part1(data):
    on = set()

    for turn_on, hc in data:
        points = itertools.product(
            *map(lambda lower, upper: range(max(lower, -50), min(upper, 50)+1),
                 hc.minpoint, hc.maxpoint))

        if turn_on:
            on |= set(points)
        else:
            on -= set(points)

    return len(on)


def diff(point):
    return point[1] - point[0]


def subspace_count_on(subspace_limits, instructions, dimension):
    cur_dim = len(subspace_limits)

    if cur_dim == dimension:
        minpoint = [lim[0] for lim in subspace_limits]
        matching_instr = (on for on, hc in reversed(instructions) if minpoint in hc)
        is_on = next(matching_instr, False)

        return reduce(operator.mul, map(diff, subspace_limits)) if is_on else 0

    split_points = set()
    for _, r in instructions:
        split_points.add(r.minpoint[cur_dim])
        split_points.add(r.maxpoint[cur_dim] + 1)

    turned_on = 0
    for lower, upper in itertools.pairwise(sorted(split_points)):
        relevant = [
            (on, hc) for on, hc in instructions
            if (hc.minpoint[cur_dim] <= lower <= hc.maxpoint[cur_dim]) or \
               (hc.minpoint[cur_dim] <= upper <= hc.maxpoint[cur_dim])]

        subspace_limits.append((lower, upper))
        turned_on += subspace_count_on(subspace_limits, relevant, dimension)
        subspace_limits.pop()

    return turned_on


def part2(instructions):
    return subspace_count_on([], instructions, 3)


def main():
    input_file = "input"
    if (len(sys.argv) > 1):
        input_file = sys.argv[1]

    instr_re = re.compile(r"(on|off).+x=(-?[0-9]+)\.\.(-?[0-9]+),y=(-?[0-9]+)\.\.(-?[0-9]+),z=(-?[0-9]+)\.\.(-?[0-9]+)")

    data = aocutils.input.read_lines(input_file)
    data = (instr_re.search(line).groups() for line in data)

    instructions = [(inst == "on",
                     Hypercuboid([int(xmin), int(ymin), int(zmin)],
                                 [int(xmax), int(ymax), int(zmax)]))
                    for (inst, xmin, xmax, ymin, ymax, zmin, zmax) in data]

    print(part1(instructions))
    print(part2(instructions))


main()
