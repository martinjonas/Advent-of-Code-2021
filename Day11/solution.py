import aocutils.input
import aocutils.parsing
import sys


def simulate_round(grid):
    for pos in grid:
        grid[pos] += 1

    to_process = [pos for pos, cell in grid.items() if cell > 9]
    has_flashed = set(to_process)

    while to_process:
        (v, h) = to_process.pop()

        neighbors = ((nv, nh)
                     for nv in range(v-1, v+2)
                     for nh in range(h-1, h+2)
                     if nv != v or nh != h)

        for pos in neighbors:
            if pos in grid:
                grid[pos] += 1
                if grid[pos] > 9 and pos not in has_flashed:
                    has_flashed.add(pos)
                    to_process.append(pos)

    for pos in has_flashed:
        grid[pos] = 0

    return len(has_flashed)


def part1(grid):
    grid = grid.copy()

    res = 0
    for _ in range(100):
        res += simulate_round(grid)
    return res


def part2(grid):
    i = 0
    while True:
        i += 1
        res = simulate_round(grid)
        if res == len(grid):
            return i


def main():
    input_file = "input"
    if (len(sys.argv) > 1):
        input_file = sys.argv[1]

    data = aocutils.input.read_lines(input_file)

    grid = {}
    for v, row in enumerate(data):
        for h, cell in enumerate(row):
            grid[(v, h)] = int(cell)

    print(part1(grid))
    print(part2(grid))


main()
