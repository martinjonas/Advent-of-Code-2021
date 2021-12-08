import aocutils.input
import aocutils.parsing
import sys
import collections
import itertools


signals_to_number = {
    "abcefg": 0,
    "cf": 1,
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9,
}


letters = ["a", "b", "c", "d", "e", "f", "g"]


def part1(data):
    return sum(
        sum(len(segment) in (2, 3, 4, 7) for segment in line[11:]) for line in data
    )


def normalize(signals):
    return "".join(sorted(signals))


def get_fingerprint(letters):
    counter = collections.Counter(itertools.chain(*letters))
    return {
        normalize(letter): tuple(sorted(counter[sig] for sig in letter))
        for letter in letters
    }


def part2(data):
    correct_numbers = list(signals_to_number)
    correct_fingerprint = get_fingerprint(correct_numbers)
    fingerprint_to_number = {
        correct_fingerprint[letter]: i
        for i, letter in enumerate(correct_numbers)
    }

    result = 0
    for line in data:
        unique = line[:10]
        outputs = line[11:]

        unique_fingerprint = get_fingerprint(unique)

        number = 0
        for output in outputs:
            letter_fingerprint = unique_fingerprint[normalize(output)]
            number = number * 10 + fingerprint_to_number[letter_fingerprint]

        result += number
    return result


def main():
    input_file = "input"
    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    data = aocutils.input.read_lines_words(input_file)

    print(part1(data))
    print(part2(data))


main()
