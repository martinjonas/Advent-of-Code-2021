import aocutils.input
import aocutils.parsing
import sys


def part1(data):
    return min(sum(abs(pos - crab) for crab in data)
               for pos in range(min(data), max(data) + 1))


def part2(data):
    return min(
        sum((abs(pos - crab) * (abs(pos - crab) + 1)) // 2 for crab in data)
        for pos in range(min(data), max(data) + 1)
    )


def main():
    input_file = "input"
    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    data = aocutils.input.read_lines(input_file)
    data = list(map(int, data[0].split(",")))

    print(part1(data))
    print(part2(data))


main()
