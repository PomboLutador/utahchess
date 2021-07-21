import pytest

from utahchess.board import Board
from utahchess.move_candidates import (
    get_bishop_move_candidates,
    get_king_move_candidates,
    get_pawn_move_candidates,
    get_queen_move_candidates,
    get_rook_move_candidates,
)


@pytest.mark.parametrize(("y_position", "movement_direction"), [(1, 1), (6, -1)])
@pytest.mark.parametrize(("x_position"), [0, 1, 2, 3, 4, 5, 6, 7])
def test_get_pawn_move_candidates_in_starting_position(
    x_position, y_position, movement_direction
):
    # given
    board = Board()
    # when
    result = tuple(
        get_pawn_move_candidates(board=board, position=(x_position, y_position))
    )

    # then
    expected = (
        ((x_position, y_position), (x_position, y_position + movement_direction)),
        ((x_position, y_position), (x_position, y_position + 2 * movement_direction)),
    )
    assert result == expected


@pytest.mark.parametrize(("y_position", "movement_direction"), [(1, 1), (6, -1)])
@pytest.mark.parametrize(("x_position"), [0, 1, 2, 3, 4, 5, 6, 7])
def test_get_knight_move_candidates_in_starting_position(
    x_position, y_position, movement_direction
):
    # given
    board = Board()
    # when
    result = tuple(
        get_pawn_move_candidates(board=board, position=(x_position, y_position))
    )

    # then
    expected = (
        ((x_position, y_position), (x_position, y_position + movement_direction)),
        ((x_position, y_position), (x_position, y_position + 2 * movement_direction)),
    )
    assert result == expected


@pytest.mark.parametrize(
    ("rook_position", "expected"),
    [
        (
            (0, 0),
            (
                ((0, 0), (1, 0)),
                ((0, 0), (2, 0)),
                ((0, 0), (3, 0)),
                ((0, 0), (4, 0)),
                ((0, 0), (6, 0)),
                ((0, 0), (0, 1)),
                ((0, 0), (0, 2)),
                ((0, 0), (0, 3)),
                ((0, 0), (0, 4)),
                ((0, 0), (5, 0)),
                ((0, 0), (0, 5)),
                ((0, 0), (0, 6)),
                ((0, 0), (0, 7)),
            ),
        ),
        (
            (7, 0),
            (
                ((7, 0), (1, 0)),
                ((7, 0), (2, 0)),
                ((7, 0), (3, 0)),
                ((7, 0), (4, 0)),
                ((7, 0), (5, 0)),
                ((7, 0), (6, 0)),
                ((7, 0), (7, 1)),
                ((7, 0), (7, 2)),
                ((7, 0), (7, 3)),
                ((7, 0), (7, 4)),
                ((7, 0), (7, 5)),
                ((7, 0), (7, 6)),
                ((7, 0), (7, 7)),
            ),
        ),
        (
            (7, 7),
            (
                ((7, 7), (6, 7)),
                ((7, 7), (5, 7)),
                ((7, 7), (4, 7)),
                ((7, 7), (3, 7)),
                ((7, 7), (2, 7)),
                ((7, 7), (1, 7)),
                ((7, 7), (7, 6)),
                ((7, 7), (7, 5)),
                ((7, 7), (7, 4)),
                ((7, 7), (7, 3)),
                ((7, 7), (7, 2)),
                ((7, 7), (7, 1)),
                ((7, 7), (7, 0)),
            ),
        ),
        (
            (0, 7),
            (
                ((0, 7), (6, 7)),
                ((0, 7), (5, 7)),
                ((0, 7), (4, 7)),
                ((0, 7), (3, 7)),
                ((0, 7), (2, 7)),
                ((0, 7), (1, 7)),
                ((0, 7), (0, 6)),
                ((0, 7), (0, 5)),
                ((0, 7), (0, 4)),
                ((0, 7), (0, 3)),
                ((0, 7), (0, 2)),
                ((0, 7), (0, 1)),
                ((0, 7), (0, 0)),
            ),
        ),
    ],
)
def test_get_rook_move_candidates_on_board_with_only_rooks_in_starting_position(
    initial_board_with_only_rooks, rook_position, expected
):
    # when
    result = tuple(
        get_rook_move_candidates(
            board=initial_board_with_only_rooks, position=rook_position
        )
    )
    # then
    assert sorted(result) == sorted(expected)


@pytest.mark.parametrize(
    ("bishop_position", "expected"),
    [
        (
            (2, 0),
            (
                ((2, 0), (3, 1)),
                ((2, 0), (4, 2)),
                ((2, 0), (5, 3)),
                ((2, 0), (6, 4)),
                ((2, 0), (7, 5)),
                ((2, 0), (1, 1)),
                ((2, 0), (0, 2)),
            ),
        ),
        (
            (5, 0),
            (
                ((5, 0), (6, 1)),
                ((5, 0), (7, 2)),
                ((5, 0), (4, 1)),
                ((5, 0), (3, 2)),
                ((5, 0), (2, 3)),
                ((5, 0), (1, 4)),
                ((5, 0), (0, 5)),
            ),
        ),
        (
            (2, 7),
            (
                ((2, 7), (3, 6)),
                ((2, 7), (4, 5)),
                ((2, 7), (5, 4)),
                ((2, 7), (6, 3)),
                ((2, 7), (7, 2)),
                ((2, 7), (1, 6)),
                ((2, 7), (0, 5)),
            ),
        ),
        (
            (5, 7),
            (
                ((5, 7), (4, 6)),
                ((5, 7), (3, 5)),
                ((5, 7), (2, 4)),
                ((5, 7), (1, 3)),
                ((5, 7), (0, 2)),
                ((5, 7), (6, 6)),
                ((5, 7), (7, 5)),
            ),
        ),
    ],
)
def test_get_bishop_move_candidates_on_board_with_only_bishops_in_starting_position(
    initial_board_with_only_bishops, bishop_position, expected
):
    # when
    result = tuple(
        get_bishop_move_candidates(
            board=initial_board_with_only_bishops, position=bishop_position
        )
    )

    # then
    assert sorted(result) == sorted(expected)


@pytest.mark.parametrize(
    ("queen_position", "expected"),
    [
        (
            (3, 0),
            (
                # diagonal moves
                ((3, 0), (4, 1)),
                ((3, 0), (5, 2)),
                ((3, 0), (6, 3)),
                ((3, 0), (7, 4)),
                ((3, 0), (2, 1)),
                ((3, 0), (1, 2)),
                ((3, 0), (0, 3)),
                # vertical moves
                ((3, 0), (3, 1)),
                ((3, 0), (3, 2)),
                ((3, 0), (3, 3)),
                ((3, 0), (3, 4)),
                ((3, 0), (3, 5)),
                ((3, 0), (3, 6)),
                ((3, 0), (3, 7)),
                # horizontal moves
                ((3, 0), (0, 0)),
                ((3, 0), (1, 0)),
                ((3, 0), (2, 0)),
                ((3, 0), (4, 0)),
                ((3, 0), (5, 0)),
                ((3, 0), (6, 0)),
                ((3, 0), (7, 0)),
            ),
        ),
        (
            (3, 7),
            (
                # diagonal moves
                ((3, 7), (4, 6)),
                ((3, 7), (5, 5)),
                ((3, 7), (6, 4)),
                ((3, 7), (7, 3)),
                ((3, 7), (2, 6)),
                ((3, 7), (1, 5)),
                ((3, 7), (0, 4)),
                # vertical moves
                ((3, 7), (3, 6)),
                ((3, 7), (3, 5)),
                ((3, 7), (3, 4)),
                ((3, 7), (3, 3)),
                ((3, 7), (3, 2)),
                ((3, 7), (3, 1)),
                ((3, 7), (3, 0)),
                # horizontal moves
                ((3, 7), (0, 7)),
                ((3, 7), (1, 7)),
                ((3, 7), (2, 7)),
                ((3, 7), (4, 7)),
                ((3, 7), (5, 7)),
                ((3, 7), (6, 7)),
                ((3, 7), (7, 7)),
            ),
        ),
    ],
)
def test_get_queen_move_candidates_on_board_with_only_queens_in_starting_position(
    initial_board_with_only_queens, queen_position, expected
):
    # when
    result = tuple(
        get_queen_move_candidates(
            board=initial_board_with_only_queens, position=queen_position
        )
    )

    # then
    assert sorted(result) == sorted(expected)


@pytest.mark.parametrize(
    ("king_position", "expected"),
    [
        (
            (4, 0),
            (
                ((4, 0), (5, 1)),
                ((4, 0), (5, 0)),
                ((4, 0), (4, 1)),
                ((4, 0), (3, 1)),
                ((4, 0), (3, 0)),
            ),
        ),
        (
            (4, 7),
            (
                ((4, 7), (5, 6)),
                ((4, 7), (4, 6)),
                ((4, 7), (3, 7)),
                ((4, 7), (5, 7)),
                ((4, 7), (3, 6)),
            ),
        ),
    ],
)
def test_get_king_move_candidates_on_board_with_only_kings_in_starting_position(
    initial_board_with_only_kings, king_position, expected
):
    # when
    result = tuple(
        get_king_move_candidates(
            board=initial_board_with_only_kings, position=king_position
        )
    )
    # then
    assert sorted(result) == sorted(expected)
