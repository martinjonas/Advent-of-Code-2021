import aocutils.input
import aocutils.parsing
import sys
import heapq
import itertools


def find_shortest(grid, target):
    # something like Dijkstra from the top of my head
    # it is 6 AM here… ¯\_(ツ)_/¯

    heap = [(0, (0, 0))]
    closed = set()

    while heap:
        (currentrisk, current) = heapq.heappop(heap)

        if current == target:
            return currentrisk

        if current in closed:
            continue

        closed.add(current)

        (v, h) = current
        for dv, dh in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            neighbor = (v + dv, h + dh)
            if neighbor not in grid or neighbor in closed:
                continue

            heapq.heappush(heap, (currentrisk + grid[neighbor], neighbor))

    assert False


def wrap(num):
    return num - 9 if num > 9 else num


def extend_grid(grid, size, n):
    return {
        (v + tile_v * size, h + tile_h * size): wrap(cell + tile_v + tile_h)
        for tile_v, tile_h in itertools.product(range(n), range(n))
        for (v, h), cell in grid.items()
    }


def main():
    input_file = "input"
    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    data = aocutils.input.read_lines(input_file)

    grid = {}
    for v, row in enumerate(data):
        for h, cell in enumerate(row):
            grid[(v, h)] = int(cell)

    size = len(data)
    target = (size - 1, size - 1)

    extgrid = extend_grid(grid, size, 5)
    exttarget = (size * 5 - 1, size * 5 - 1)

    print(find_shortest(grid, target))
    print(find_shortest(extgrid, exttarget))


main()
