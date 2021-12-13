import aocutils.input
import aocutils.parsing
import sys
import collections


def solve(edges_from, allow_revisit):
    cache = {}

    def dfs(cur, path, allow_revisit):
        cache_key = (cur, tuple(sorted(path)), allow_revisit)
        cache_res = cache.get(cache_key)
        if cache_res is not None:
            return cache_res

        paths = 0
        for neighbor in edges_from[cur]:
            if (neighbor == 'end'):
                paths += 1
                continue
            if neighbor == 'start':
                continue
            if (neighbor.islower() and neighbor in path):
                if allow_revisit:
                    paths += dfs(neighbor, path, False)
            else:
                if neighbor.islower():
                    path.add(neighbor)
                paths += dfs(neighbor, path, allow_revisit)
                if neighbor.islower():
                    path.remove(neighbor)

        cache[cache_key] = paths
        return paths

    return dfs('start', set(['start']), allow_revisit)


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
