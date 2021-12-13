import aocutils.input
import aocutils.parsing
import sys


def fold_coord(coord, val):
    if coord < val:
        return coord
    elif coord > val:
        return val - (coord - val)
    assert False


def fold_grid(grid, axis, val):
    if axis == "y":
        return set((x, fold_coord(y, val)) for (x, y) in grid)
    elif axis == "x":
        return set((fold_coord(x, val), y) for (x, y) in grid)


def part1(grid, folds):
    return len(fold_grid(grid, folds[0][0], int(folds[0][1])))


def part2(grid, folds):
    for fold in folds:
        grid = fold_grid(grid, fold[0], int(fold[1]))

    for y in range(6):
        for x in range(40):
            print("#" if (x, y) in grid else " ", end="")
        print()


def main():
    input_file = "input"
    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    dots, folds = aocutils.input.read_groups(input_file)

    dots = set(tuple(map(int, aocutils.parsing.break_words(line)))
               for line in dots)
    folds = [aocutils.parsing.break_words(line)[2:]
             for line in folds]

    print(part1(dots, folds))
    part2(dots, folds)


main()
