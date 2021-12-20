import aocutils.input
import aocutils.parsing
import sys
import itertools


def neighbors(pos):
    (h, v) = pos
    return ((nh, nv) for nv in range(v-1, v+2) for nh in range(h-1, h+2))


def enhance(algorithm, image):
    (cells_inside, cell_outside) = image
    (hmin, vmin) = map(min, *cells_inside)
    (hmax, vmax) = map(max, *cells_inside)

    def is_lit(pos):
        (h, v) = pos
        if hmin <= h <= hmax and vmin <= v <= vmax:
            return pos in cells_inside
        return cell_outside

    new_image = set()
    for pos in itertools.product(range(hmin-1, hmax+2), range(vmin-1, vmax+2)):
        bin_index = ''.join("1" if is_lit(n) else "0" for n in neighbors(pos))

        if algorithm[int(bin_index, 2)]:
            new_image.add(pos)

    new_cell_outside = algorithm[-1] if cell_outside else algorithm[0]

    return (new_image, new_cell_outside)


def enhance_multiple(algorithm, image, steps):
    cur = image
    for _ in range(steps):
        cur = enhance(algorithm, cur)

    res, cell_outside = cur
    assert not cell_outside
    return len(res)


def main():
    input_file = "input"
    if (len(sys.argv) > 1):
        input_file = sys.argv[1]

    groups = aocutils.input.read_groups(input_file)
    algorithm = [ch == "#" for ch in groups[0][0]]
    image_data = groups[1]

    image = set()
    for v, row in enumerate(image_data):
        for h, cell in enumerate(row):
            if cell == "#":
                image.add((h, v))

    assert len(algorithm) == 2**9

    print(enhance_multiple(algorithm, (image, False), 2))
    print(enhance_multiple(algorithm, (image, False), 50))


main()

#5258
