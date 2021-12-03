import aocutils.input
import sys


def part1(data):
    hor, depth = 0, 0

    for command, num in data:
        num = int(num)
        if command == 'forward':
            hor += num
        elif command == 'up':
            depth -= num
        elif command == 'down':
            depth += num

    return(hor*depth)


def part2(data):
    hor, depth, aim = 0, 0, 0

    for command, num in data:
        num = int(num)
        if command == 'forward':
            hor += num
            depth += aim * num
        elif command == 'up':
            aim -= num
        elif command == 'down':
            aim += num

    return(hor*depth)


def main():
    input_file = "input"
    if (len(sys.argv) > 1):
        input_file = sys.argv[1]

    data = aocutils.input.read_lines_words(input_file)

    print(part1(data))
    print(part2(data))


main()
