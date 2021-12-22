import collections
import itertools
import functools


def part1(data):
    positions = data
    scores = [0, 0]

    die = 1
    steps = 0

    while scores[1] < 1000:
        positions[0] = (positions[0] + (die + die + 1 + die + 2))
        positions[0] = ((positions[0] - 1) % 10) + 1
        scores[0] += positions[0]
        die = ((die - 1) + 3 % 999) + 1
        steps += 3

        positions[0], positions[1] = positions[1], positions[0]
        scores[0], scores[1] = scores[1], scores[0]

    return(scores[0]*steps)


cache = {}

def count_winning(target, current, positions, scores, remainingroundsteps):
    global cache

    key = (target, current, tuple(positions), tuple(scores), remainingroundsteps)
    if key in cache:
        return cache[key]

    result = 0
    for die in range(1, 4):
        newpos = positions[:]
        newscores = scores[:]

        newpos[current] = newpos[current] + die
        newpos[current] = ((newpos[current] - 1) % 10) + 1

        if remainingroundsteps == 1:
            newscores[current] += newpos[current]

        if newscores[current] >= 21:
            if current == target:
                result += 1
        else:
            if remainingroundsteps == 1:
                newplayer = (current + 1) % 2
                newsteps = 3
            else:
                newplayer = current
                newsteps = remainingroundsteps - 1

            result += count_winning(target, newplayer, newpos, newscores, newsteps)

    cache[key] = result
    return result


def part2(data):
    return max(count_winning(0, 0, data, [0, 0], 3),
               count_winning(1, 0, data, [0, 0], 3))



def main():
    #data = [4, 8]
    data = [4, 1]

    print(part1(data))
    print(part2(data))


main()
