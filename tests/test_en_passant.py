import pytest

from utahchess.board import Board
from utahchess.en_passant import (
    EnPassantMove,
    get_en_passant_moves,
    make_en_passant_move,
)
from utahchess.move_validation import REGULAR_MOVE


def test_right_side_en_passant_scenario_for_black():
    # given
    board_before_moving_piece = f"""oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-bk-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-bp-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            wp-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-wk-oo-oo-oo"""
    board_before_moving_piece = Board(board_string=board_before_moving_piece)
    board_after_moving_piece = board_before_moving_piece.move_piece(
        from_position=(0, 6), to_position=(0, 4)
    )
    last_move = Move(
        type=REGULAR_MOVE,
        piece_moves=(((0, 6), (0, 4)),),
        moving_pieces=(board_before_moving_piece[0, 6],),
        is_capturing_move=False,
        allows_en_passant=True,
    )

    # when
    actual = tuple(
        get_en_passant_moves(board=board_after_moving_piece, last_move=last_move)
    )

    # then
    expected = (
        EnPassantMove(
            piece_moves=(((1, 4), (0, 5)),),
            moving_pieces=(board_after_moving_piece[1, 4],),
        ),
    )
    assert expected == actual


def test_left_side_en_passant_scenario_for_black():
    # given
    board_before_moving_piece = f"""oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-bk-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-bp-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-wp
            oo-oo-oo-oo-wk-oo-oo-oo"""
    board_before_moving_piece = Board(board_string=board_before_moving_piece)
    board_after_moving_piece = board_before_moving_piece.move_piece(
        from_position=(7, 6), to_position=(7, 4)
    )
    last_move = Move(
        type=REGULAR_MOVE,
        piece_moves=(((7, 6), (7, 4)),),
        moving_pieces=(board_before_moving_piece[7, 6],),
        is_capturing_move=False,
        allows_en_passant=True,
    )

    # when
    actual = tuple(
        get_en_passant_moves(board=board_after_moving_piece, last_move=last_move)
    )

    # then
    expected = (
        EnPassantMove(
            piece_moves=(((6, 4), (7, 5)),),
            moving_pieces=(board_after_moving_piece[6, 4],),
        ),
    )
    assert expected == actual


def test_right_side_en_passant_scenario_for_white():
    # given
    board_before_moving_piece = f"""oo-oo-oo-oo-oo-oo-oo-oo
            bp-oo-oo-oo-bk-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-wp-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-wk-oo-oo-oo"""
    board_before_moving_piece = Board(board_string=board_before_moving_piece)
    board_after_moving_piece = board_before_moving_piece.move_piece(
        from_position=(0, 1), to_position=(0, 3)
    )
    last_move = Move(
        type=REGULAR_MOVE,
        piece_moves=(((0, 1), (0, 3)),),
        moving_pieces=(board_before_moving_piece[0, 1],),
        is_capturing_move=False,
        allows_en_passant=True,
    )

    # when
    actual = tuple(
        get_en_passant_moves(board=board_after_moving_piece, last_move=last_move)
    )

    # then
    expected = (
        EnPassantMove(
            piece_moves=(((1, 3), (0, 2)),),
            moving_pieces=(board_after_moving_piece[1, 3],),
        ),
    )
    assert expected == actual


def test_left_side_en_passant_scenario_for_white():
    # given
    board_before_moving_piece = f"""oo-oo-oo-oo-oo-oo-oo-oo
            oo-bp-oo-oo-bk-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            wp-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-wk-oo-oo-oo"""
    board_before_moving_piece = Board(board_string=board_before_moving_piece)
    board_after_moving_piece = board_before_moving_piece.move_piece(
        from_position=(1, 1), to_position=(1, 3)
    )
    last_move = Move(
        type=REGULAR_MOVE,
        piece_moves=(((1, 1), (1, 3)),),
        moving_pieces=(board_before_moving_piece[1, 1],),
        is_capturing_move=False,
        allows_en_passant=True,
    )

    # when
    actual = tuple(
        get_en_passant_moves(board=board_after_moving_piece, last_move=last_move)
    )

    # then
    expected = (
        EnPassantMove(
            piece_moves=(((0, 3), (1, 2)),),
            moving_pieces=(board_after_moving_piece[0, 3],),
        ),
    )
    assert actual == expected


@pytest.mark.parametrize(
    (
        "board_string_before_moving_piece",
        "last_move_initial",
        "last_move_destination",
    ),
    [
        (
            f"""oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-bk-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-wp-oo-oo-oo-oo-oo
            oo-oo-oo-oo-wk-oo-oo-oo""",
            (2, 6),
            (2, 4),
        ),
        (
            f"""oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-bk-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-wp-oo-oo-oo-oo
            oo-oo-oo-oo-wk-oo-oo-oo""",
            (3, 6),
            (3, 4),
        ),
        (
            f"""oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-bk-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            wp-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-wk-oo-oo-oo""",
            (0, 6),
            (0, 4),
        ),
        (
            f"""oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-bk-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-wp
            oo-oo-oo-oo-wk-oo-oo-oo""",
            (7, 6),
            (7, 4),
        ),
        (
            f"""oo-oo-oo-oo-oo-oo-oo-oo
            bp-oo-oo-oo-bk-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-wk-oo-oo-oo""",
            (0, 1),
            (0, 3),
        ),
        (
            f"""oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-bk-oo-oo-bp
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-wk-oo-oo-oo""",
            (7, 1),
            (7, 3),
        ),
    ],
)
def test_last_move_allows_en_passant_but_no_pawn_nearby(
    board_string_before_moving_piece, last_move_initial, last_move_destination
):
    # given
    board_before_moving_piece = Board(board_string=board_string_before_moving_piece)
    board_after_moving_piece = board_before_moving_piece.move_piece(
        from_position=last_move_initial, to_position=last_move_destination
    )
    last_move = Move(
        type=REGULAR_MOVE,
        piece_moves=((last_move_initial, last_move_destination),),
        moving_pieces=(board_before_moving_piece[last_move_initial],),
        is_capturing_move=False,
        allows_en_passant=True,
    )

    # when
    actual = tuple(
        get_en_passant_moves(board=board_after_moving_piece, last_move=last_move)
    )

    # then
    expected = ()
    assert expected == actual


def test_get_en_passant_moves_would_leave_king_in_check_black():
    # given
    board_before_moving_piece = f"""oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-bk-oo-bp-wr-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-wp-oo-oo-oo-oo-oo
            oo-oo-oo-oo-wk-oo-oo-oo"""
    board_before_moving_piece = Board(board_string=board_before_moving_piece)
    board_after_moving_piece = board_before_moving_piece.move_piece(
        from_position=(2, 6), to_position=(2, 4)
    )
    last_move = Move(
        type=REGULAR_MOVE,
        piece_moves=(((2, 6), (2, 4)),),
        moving_pieces=(board_before_moving_piece[2, 6],),
        is_capturing_move=False,
        allows_en_passant=True,
    )

    # when
    actual = tuple(
        get_en_passant_moves(board=board_after_moving_piece, last_move=last_move)
    )

    # then
    expected = ()
    assert expected == actual


def test_get_en_passant_moves_would_leave_king_in_check_white():
    # given
    board_before_moving_piece = f"""oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-bp-oo-oo-oo-bk-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-br-oo-wp-wk-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-wk-oo-oo-oo"""
    board_before_moving_piece = Board(board_string=board_before_moving_piece)
    board_after_moving_piece = board_before_moving_piece.move_piece(
        from_position=(2, 1), to_position=(2, 3)
    )
    last_move = Move(
        type=REGULAR_MOVE,
        piece_moves=(((2, 1), (2, 3)),),
        moving_pieces=(board_before_moving_piece[2, 1],),
        is_capturing_move=False,
        allows_en_passant=True,
    )

    # when
    actual = tuple(
        get_en_passant_moves(board=board_after_moving_piece, last_move=last_move)
    )

    # then
    expected = ()
    assert expected == actual


def test_both_sides_en_passant_scenario_for_white():
    # given
    board_before_moving_piece = f"""oo-oo-oo-oo-oo-oo-oo-oo
            oo-bp-oo-oo-bk-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            wp-oo-wp-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-wk-oo-oo-oo"""
    board_before_moving_piece = Board(board_string=board_before_moving_piece)
    board_after_moving_piece = board_before_moving_piece.move_piece(
        from_position=(1, 1), to_position=(1, 3)
    )
    last_move = Move(
        type=REGULAR_MOVE,
        piece_moves=(((1, 1), (1, 3)),),
        moving_pieces=(board_before_moving_piece[1, 1],),
        is_capturing_move=False,
        allows_en_passant=True,
    )

    # when
    actual = tuple(
        get_en_passant_moves(board=board_after_moving_piece, last_move=last_move)
    )

    # then
    expected = (
        EnPassantMove(
            piece_moves=(((2, 3), (1, 2)),),
            moving_pieces=(board_after_moving_piece[2, 3],),
        ),
        EnPassantMove(
            piece_moves=(((0, 3), (1, 2)),),
            moving_pieces=(board_after_moving_piece[0, 3],),
        ),
    )
    assert expected == actual


def test_both_sides_en_passant_scenario_for_black():
    # given
    board_before_moving_piece = f"""oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-bk-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            bp-oo-bp-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-wp-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-wk-oo-oo-oo"""
    board_before_moving_piece = Board(board_string=board_before_moving_piece)
    board_after_moving_piece = board_before_moving_piece.move_piece(
        from_position=(1, 6), to_position=(1, 4)
    )
    last_move = Move(
        type=REGULAR_MOVE,
        piece_moves=(((1, 6), (1, 4)),),
        moving_pieces=(board_before_moving_piece[1, 6],),
        is_capturing_move=False,
        allows_en_passant=True,
    )

    # when
    actual = tuple(
        get_en_passant_moves(board=board_after_moving_piece, last_move=last_move)
    )

    # then
    expected = (
        EnPassantMove(
            piece_moves=(((2, 4), (1, 5)),),
            moving_pieces=(board_after_moving_piece[2, 4],),
        ),
        EnPassantMove(
            piece_moves=(((0, 4), (1, 5)),),
            moving_pieces=(board_after_moving_piece[0, 4],),
        ),
    )
    assert expected == actual


@pytest.mark.parametrize(
    ("intial_board", "expected_board", "en_passant_from", "en_passant_to"),
    [
        (
            Board(
                board_string=f"""oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-bk-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            bp-wp-bp-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-wk-oo-oo-oo"""
            ),
            Board(
                board_string=f"""oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-bk-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            bp-oo-oo-oo-oo-oo-oo-oo
            oo-bp-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-wk-oo-oo-oo"""
            ),
            (2, 4),
            (1, 5),
        ),
        (
            Board(
                board_string=f"""oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-bk-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            bp-wp-bp-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-wk-oo-oo-oo"""
            ),
            Board(
                board_string=f"""oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-bk-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-bp-oo-oo-oo-oo-oo
            oo-bp-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-wk-oo-oo-oo"""
            ),
            (0, 4),
            (1, 5),
        ),
        (
            Board(
                board_string=f"""oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-bk-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            wp-bp-wp-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-wk-oo-oo-oo"""
            ),
            Board(
                board_string=f"""oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-bk-oo-oo-oo
            oo-wp-oo-oo-oo-oo-oo-oo
            wp-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-wk-oo-oo-oo"""
            ),
            (2, 3),
            (1, 2),
        ),
        (
            Board(
                board_string=f"""oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-bk-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            wp-bp-wp-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-wk-oo-oo-oo"""
            ),
            Board(
                board_string=f"""oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-bk-oo-oo-oo
            oo-wp-oo-oo-oo-oo-oo-oo
            oo-oo-wp-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-wk-oo-oo-oo"""
            ),
            (0, 3),
            (1, 2),
        ),
    ],
)
def test_make_en_passant_move(
    intial_board, expected_board, en_passant_from, en_passant_to
):

    # given
    en_passant_move = EnPassantMove(
        piece_moves=((en_passant_from, en_passant_to),),
        moving_pieces=(intial_board[en_passant_from],),
    )

    # when
    actual = make_en_passant_move(
        board=intial_board,
        move=en_passant_move,
    )
    assert expected_board == actual
