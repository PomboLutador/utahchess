import string

FILE_POSSIBILITIES = "abcdefgh"
RANK_POSSIBILITIES = "87654321"


def x_index_to_file(x: int) -> str:
    return FILE_POSSIBILITIES[x]


def y_index_to_rank(y: int) -> str:
    return RANK_POSSIBILITIES[y]


def rank_to_y_index(rank: str) -> int:
    return 8 - int(rank)


def file_to_x_index(file: str) -> int:
    return string.ascii_lowercase.index(file)
