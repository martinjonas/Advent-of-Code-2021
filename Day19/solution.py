import aocutils.input
import aocutils.parsing
import sys
import itertools
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True, order=True)
class Orientation:
    x_to: str
    x_neg: bool
    rotated: int


def get_orientations():
    return [Orientation(x_to, x_neg, rotated)
            for x_to in ("x", "y", "z")
            for x_neg in (False, True)
            for rotated in range(4)]


def apply_orientation(orientation, position):
    x, y, z = position
    if orientation.x_to == "x" and not orientation.x_neg:
        x, y, z = x, y, z
    elif orientation.x_to == "x" and orientation.x_neg:
        x, y, z = -x, -y, z
    elif orientation.x_to == "y" and not orientation.x_neg:
        x, y, z = y, -x, z
    elif orientation.x_to == "y" and orientation.x_neg:
        x, y, z = -y, x, z
    elif orientation.x_to == "z" and not orientation.x_neg:
        x, y, z = z, y, -x
    elif orientation.x_to == "z" and orientation.x_neg:
        x, y, z = -z, y, x

    if orientation.rotated == 1:
        y, z = -z, y
    elif orientation.rotated == 2:
        y, z = -y, -z
    elif orientation.rotated == 3:
        y, z = z, -y

    return np.array((x, y, z))


def find_overlaps(list_a, list_b, treshold):
    set_a = set(map(tuple, list_a))

    for aligned_a in list_a:
        for aligned_b in list_b[:-11]:
            offset = aligned_b - aligned_a

            overlaps = sum(tuple(b - offset) in set_a for b in list_b)

            if overlaps >= treshold:
                return offset

    return None


def solve(scannerdata):
    scanners = list(range(len(scannerdata)))

    possibilities = {}
    for scanner, data in enumerate(scannerdata):
        possibilities[scanner] = {ori: [apply_orientation(ori, pos) for pos in data]
                                  for ori in get_orientations()}

    fixed = {0: np.array([0, 0, 0])}
    fixed_data = {0: scannerdata[0]}
    to_process = [0]

    while to_process:
        cur = to_process.pop()

        for scanner in scanners:
            if scanner in fixed:
                continue

            for scanner_data in possibilities[scanner].values():
                offset = find_overlaps(fixed_data[cur], scanner_data, 12)

                if offset is not None:
                    fixed[scanner] = offset
                    fixed_data[scanner] = [pos - offset for pos in scanner_data]
                    to_process.append(scanner)
                    break

    # PART 1
    beacon_positions = set.union(*[set(map(tuple, data))
                                   for data in fixed_data.values()])
    print(len(beacon_positions))

    # PART 2
    maxdist = max(
        sum(map(abs, scanner1 - scanner2))
        for scanner1, scanner2
        in itertools.combinations(fixed.values(), 2))
    print(maxdist)


def main():
    input_file = "input"
    if (len(sys.argv) > 1):
        input_file = sys.argv[1]

    data = aocutils.input.read_groups(input_file)

    scannerdata = [[np.array(list(map(int, line.split(","))))
                    for line in group[1:]]
                   for group in data]

    solve(scannerdata)


main()
