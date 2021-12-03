import aocutils.input
import sys
from collections import Counter


def most_common(it):
    counter = Counter(it)
    return '0' if counter['0'] > counter['1'] else '1'


def least_common(it):
    counter = Counter(it)
    return '0' if counter['0'] <= counter['1'] else '1'


def part1(data):
    mc = [most_common(col) for col in zip(*data)]
    mcstr = ''.join(mc)

    gamma = int(mcstr, 2)
    eps = int(mcstr.translate(mcstr.maketrans('01', '10')), 2)

    return gamma * eps


def part2(data):
    def get_rating(data, criterion):
        cur = data
        for i in range(len(data[0])):
            chosen = criterion([line[i] for line in cur])
            cur = [line for line in cur if line[i] == chosen]
            if len(cur) == 1:
                break
        return int(cur[0], 2)

    return get_rating(data, most_common) * get_rating(data, least_common)


def main():
    input_file = "input"
    if (len(sys.argv) > 1):
        input_file = sys.argv[1]

    data = aocutils.input.read_lines(input_file)

    print(part1(data))
    print(part2(data))


main()
