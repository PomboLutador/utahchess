import pytest

from utahchess.board import Board
from utahchess.move_candidates import get_pawn_move_candidates, get_rook_move_candidates


@pytest.mark.parametrize(("y_position", "movement_direction"), [(1, 1), (6, -1)])
@pytest.mark.parametrize(("x_position"), [0, 1, 2, 3, 4, 5, 6, 7])
def test_get_pawn_move_candidates_in_starting_position(
    x_position, y_position, movement_direction
):
    # given
    board = Board()
    # when
    result = tuple(
        get_pawn_move_candidates(board=board, pawn_position=(x_position, y_position))
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
        get_pawn_move_candidates(board=board, pawn_position=(x_position, y_position))
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
            board=initial_board_with_only_rooks, rook_position=rook_position
        )
    )
    # then
    assert sorted(result) == sorted(expected)
