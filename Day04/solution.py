import aocutils.input
import aocutils.parsing
import sys
from collections import defaultdict, namedtuple


def get_number_to_cell_map(boards):
    number_to_cells = defaultdict(list)

    for b_i, board in enumerate(boards):
        for r_i, row in enumerate(board):
            for c_i, cell in enumerate(row):
                number_to_cells[cell].append((b_i, r_i, c_i))

    return number_to_cells


WinningBoard = namedtuple('WinningBoard', ['last_num', 'board', 'checked'])

def get_winning_boards(numbers, boards):
    checked = [set() for _ in boards]
    is_won = [False for _ in boards]
    number_to_cells = get_number_to_cell_map(boards)

    def check(number):
        for (b_i, r_i, c_i) in number_to_cells[number]:
            if is_won[b_i]:
                continue

            checked[b_i].add((r_i, c_i))

            is_winning = all((r_i, i) in checked[b_i] for i in range(5)) or \
                all((i, c_i) in checked[b_i] for i in range(5))

            if is_winning:
                is_won[b_i] = True
                yield b_i

    for cur in numbers:
        for won_index in check(cur):
            yield WinningBoard(cur, boards[won_index], checked[won_index])


def sum_unchecked(board, checked):
    return sum(cell
               for r_i, row in enumerate(board)
               for c_i, cell in enumerate(row)
               if (r_i, c_i) not in checked)


def get_score(winning_board):
    return winning_board.last_num * \
        sum_unchecked(winning_board.board, winning_board.checked)


def main():
    input_file = "input"
    if (len(sys.argv) > 1):
        input_file = sys.argv[1]

    data = aocutils.input.read_groups(input_file)

    numbers = list(map(int, data[0][0].split(",")))
    table = [[list(map(int, aocutils.parsing.break_words(line)))
              for line in table]
             for table in data[1:]]

    first, *_, last = get_winning_boards(numbers, table)

    print(get_score(first))
    print(get_score(last))


main()
