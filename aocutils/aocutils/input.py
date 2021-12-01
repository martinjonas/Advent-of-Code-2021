from typing import List


def read_lines(filename: str) -> List[str]:
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def read_numbers(filename: str) -> List[int]:
    with open(filename) as f:
        return [int(part) for part in f.read().split()]


def read_lines_words(filename: str) -> List[List[str]]:
    with open(filename) as f:
        return [list(line.strip().split()) for line in f.readlines()]


def read_lines_numbers(filename: str) -> List[List[int]]:
    with open(filename) as f:
        return [list(map(lambda x: int(x), line.strip().split()))
                for line
                in f.readlines()]
