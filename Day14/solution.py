import itertools
import aocutils.input
import aocutils.parsing
import sys
import collections


def solve(template, rules, steps):
    letter_counts = collections.Counter(template)
    pair_counts = collections.Counter(itertools.pairwise(template))

    for _ in range(steps):
        new_pair_counts = collections.defaultdict(int)
        for ((left, right), ins) in rules:
            matching = pair_counts[(left, right)]
            new_pair_counts[(left, ins)] += matching
            new_pair_counts[(ins, right)] += matching
            letter_counts[ins] += matching
        pair_counts = new_pair_counts

    ordered_counts = letter_counts.most_common(None)
    return(ordered_counts[0][1] - ordered_counts[-1][1])


def main():
    input_file = "input"
    if (len(sys.argv) > 1):
        input_file = sys.argv[1]

    data = aocutils.input.read_groups(input_file)
    template = data[0][0]
    rules = list(map(aocutils.parsing.break_words, data[1]))

    print(solve(template, rules, 10))
    print(solve(template, rules, 40))


main()
