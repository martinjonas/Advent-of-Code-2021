import aocutils.input
import aocutils.parsing
import sys


def neighbors(h, v):
    return ((nh, nv) for nv in range(v-1, v+2) for nh in range(h-1, h+2))


def enhance(algorithm, image):
    (cells_inside, cell_outside) = image
    hmin = min(h for h, _ in cells_inside)
    hmax = max(h for h, _ in cells_inside)
    vmin = min(v for _, v in cells_inside)
    vmax = max(v for _, v in cells_inside)

    new_image = set()
    for h in range(hmin-1, hmax+2):
        for v in range(vmin-1, vmax+2):
            index = int(
                ''.join("1" if (nh, nv) in cells_inside \
                        or (cell_outside and (nh < hmin or nh > hmax or nv < vmin or nv > vmax))
                        else "0" for (nh, nv) in neighbors(h, v)),
                2)

            if algorithm[index]:
                new_image.add((h, v))

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

    print(enhance_multiple(algorithm, (image, False), 2))
    print(enhance_multiple(algorithm, (image, False), 50))


main()

#5258
