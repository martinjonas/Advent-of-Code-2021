import aocutils.input
import sys


def part1(data):
    print(sum(1 for f, s in zip(data, data[1:]) if s > f))


def part2(data):
    sw = [sum(data[i:i+3]) for i in range(len(data)-2)]
    part1(sw)


def main():
    input_file = "input"
    if (len(sys.argv) > 1):
        input_file = sys.argv[1]

    data = aocutils.input.read_numbers(input_file)

    part1(data)
    part2(data)


main()
