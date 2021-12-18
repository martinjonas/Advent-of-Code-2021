import aocutils.input
import aocutils.parsing
import sys
import itertools
import functools
import copy


def add_to_leftmost(number, val):
    match number:
        case [int(), _]:
            number[0] += val
        case [l, _]:
            add_to_leftmost(l, val)


def add_to_rightmost(number, val):
    match number:
        case [_ , int()]:
            number[1] += val
        case [_, r]:
            add_to_rightmost(r, val)


def do_explode(number, depth):
    match number:
        case [int(), int()] if depth >= 4:
            return number, False, False
        case [int(), int()] if depth < 4:
            return None, False, False
        case list():
            for i, child in enumerate(number):
                (to_explode, added_to_left, added_to_right) = do_explode(child, depth+1)

                if to_explode and not added_to_left and not added_to_right:
                    number[i] = 0

                if to_explode is not None:
                    if not added_to_left and i > 0:
                        if isinstance(number[i-1], int):
                            number[i-1] += to_explode[0]
                        else:
                            add_to_rightmost(number[i-1], to_explode[0])
                        added_to_left = True
                    if not added_to_right and i < len(number) - 1:
                        if isinstance(number[i+1], int):
                            number[i+1] += to_explode[1]
                        else:
                            add_to_leftmost(number[i+1], to_explode[1])
                        added_to_right = True
                    return (to_explode, added_to_left, added_to_right)

    return None, False, False


def explode(number):
    (to_explode, _, _) = do_explode(number, 0)
    return to_explode is not None


def split(number):
    assert(isinstance(number, list))

    for i, child in enumerate(number):
        if isinstance(child, int):
            if child >= 10:
                number[i] = [child // 2, child // 2 + (child % 2)]
                return True
        else:
            has_split = split(child)
            if has_split:
                return True

    return False


def normalize(number):
    while True:
        has_exploded = explode(number)
        if has_exploded:
            continue

        has_split = split(number)
        if not has_split:
            break


def add(l, r):
    res = [l, r]
    normalize(res)
    return(res)


def magnitude(number):
    match number:
        case [l, r]:
            return 3*magnitude(l) + 2*magnitude(r)
        case number:
            return number


def part1(data):
    return magnitude(functools.reduce(add, data))


def part2(data):
    return max(
        max(magnitude(add(copy.deepcopy(l), copy.deepcopy(r))),
            magnitude(add(copy.deepcopy(r), copy.deepcopy(l))))
        for l, r in itertools.combinations(data, 2))


def main():
    input_file = "input"
    if (len(sys.argv) > 1):
        input_file = sys.argv[1]

    data = [eval(line) for line in aocutils.input.read_lines(input_file)]

    print(part1(copy.deepcopy(data)))
    print(part2(data))


main()
