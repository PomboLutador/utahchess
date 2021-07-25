import pytest

from utahchess.algebraic_notation import x_index_to_file, y_index_to_rank


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
