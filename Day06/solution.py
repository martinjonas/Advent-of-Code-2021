import aocutils.input
import aocutils.parsing
import sys
import collections


def fish_after_days(data, days):
    of_age = collections.Counter(data)
    of_age = collections.deque(of_age[i] for i in range(9))

    for _ in range(days):
        of_age.rotate(-1)
        of_age[6] += of_age[8]

    return(sum(of_age))


def main():
    input_file = "input"
    if (len(sys.argv) > 1):
        input_file = sys.argv[1]

    data = aocutils.input.read_lines(input_file)
    data = list(map(int, data[0].split(',')))

    print(fish_after_days(data, 80))
    print(fish_after_days(data, 256))


main()
