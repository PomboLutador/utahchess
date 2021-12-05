import pytest

from utahchess.utils import (
    file_to_x_index,
    rank_to_y_index,
    x_index_to_file,
    y_index_to_rank,
)


@pytest.mark.parametrize(
    ("x_index", "expected_file"),
    [
        (0, "a"),
        (1, "b"),
        (2, "c"),
        (3, "d"),
        (4, "e"),
        (5, "f"),
        (6, "g"),
        (7, "h"),
    ],
)
def test_x_index_to_file(x_index, expected_file):
    # when
    result = x_index_to_file(x=x_index)

    # then
    assert result == expected_file


@pytest.mark.parametrize(
    ("y_index", "expected_rank"),
    [
        (0, "8"),
        (1, "7"),
        (2, "6"),
        (3, "5"),
        (4, "4"),
        (5, "3"),
        (6, "2"),
        (7, "1"),
    ],
)
def test_y_index_to_rank(y_index, expected_rank):
    # when
    result = y_index_to_rank(y=y_index)

    # then
    assert result == expected_rank


@pytest.mark.parametrize(
    ("rank", "expected_y_index"),
    [
        ("8", 0),
        ("7", 1),
        ("6", 2),
        ("5", 3),
        ("4", 4),
        ("3", 5),
        ("2", 6),
        ("1", 7),
    ],
)
def test_rank_to_y_index(rank, expected_y_index):
    # when
    result = rank_to_y_index(rank=rank)

    # then
    assert result == expected_y_index


@pytest.mark.parametrize(
    ("file", "expected_x_index"),
    [
        ("a", 0),
        ("b", 1),
        ("c", 2),
        ("d", 3),
        ("e", 4),
        ("f", 5),
        ("g", 6),
        ("h", 7),
    ],
)
def test_file_to_x_index(file, expected_x_index):
    # when
    result = file_to_x_index(file=file)

    # then
    assert result == expected_x_index
