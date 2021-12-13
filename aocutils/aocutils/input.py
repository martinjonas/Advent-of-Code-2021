from typing import List


def read_lines(filename: str) -> List[str]:
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def read_numbers(filename: str) -> List[int]:
    with open(filename) as f:
        return [int(part) for part in f.read().split()]


def read_groups(filename: str) -> List[List[str]]:
    current: List[str] = []
    result: List[List[str]] = []

    with open(filename) as f:
        for line in f.readlines():
            line = line.strip()
            if line == "":
                result.append(current)
                current = []
            else:
                current.append(line)

    result.append(current)
    return result


def read_lines_words(filename: str) -> List[List[str]]:
    with open(filename) as f:
        return [list(line.strip().split()) for line in f.readlines()]


def read_lines_numbers(filename: str) -> List[List[int]]:
    with open(filename) as f:
        return [list(map(lambda x: int(x), line.strip().split()))
                for line
                in f.readlines()]
