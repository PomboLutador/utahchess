import pytest

from utahchess.board import Board
from utahchess.en_passant import EnPassantMove, get_en_passant_moves
from utahchess.move_validation import RegularMove


def test_right_side_passant_scenario_for_black():
    # given
    board_before_moving_piece = f"""oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-bc-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-bp-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-wp-oo-oo-oo-oo-oo
            oo-oo-oo-oo-wc-oo-oo-oo"""
    board_before_moving_piece = Board(board_string=board_before_moving_piece)
    board_after_moving_piece = board_before_moving_piece.move_piece(
        from_position=(2, 6), to_position=(2, 4)
    )
    last_move = RegularMove(
        piece_moves=(((2, 6), (2, 4)),),
        moving_pieces=(board_before_moving_piece[2, 6],),
        is_capturing_move=False,
    )

    # when
    actual = tuple(
        get_en_passant_moves(board=board_after_moving_piece, last_move=last_move)
    )

    # then
    expected = (
        EnPassantMove(
            piece_moves=(((3, 4), (2, 5)),),
            moving_pieces=(board_after_moving_piece[3, 4],),
        ),
    )
    assert expected == actual
