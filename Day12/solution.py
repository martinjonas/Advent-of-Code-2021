import aocutils.input
import aocutils.parsing
import sys
import collections


def solve(edges_from, allow_revisit):
    paths = [0]

    def dfs(cur, path, allow_revisit):
        for neighbor in edges_from[cur]:
            if (neighbor == 'end'):
                paths[0] += 1
                continue
            if neighbor == 'start':
                continue
            if (neighbor.islower() and neighbor in path):
                if allow_revisit:
                    dfs(neighbor, path, False)
            else:
                if neighbor.islower():
                    path.add(neighbor)
                dfs(neighbor, path, allow_revisit)
                if neighbor.islower():
                    path.remove(neighbor)

    dfs('start', set(['start']), allow_revisit)
    return paths[0]


def part1(edges_from):
    return solve(edges_from, False)


def part2(edges_from):
    return solve(edges_from, True)


def main():
    input_file = "input"
    if (len(sys.argv) > 1):
        input_file = sys.argv[1]

    data = aocutils.input.read_lines(input_file)
    data = [aocutils.parsing.break_words(line)
            for line in data]

    edges_from = collections.defaultdict(list)
    for [f, t] in data:
        edges_from[f].append(t)
        edges_from[t].append(f)

    print(part1(edges_from))
    print(part2(edges_from))


main()
