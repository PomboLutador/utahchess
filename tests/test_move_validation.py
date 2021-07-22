from utahchess.board import Board
from utahchess.move_candidates import get_king_move_candidates, get_pawn_move_candidates
from utahchess.move_validation import (
    RegularMove,
    is_check,
    is_checkmate,
    validate_move_candidates,
)


def test_is_checkmate_fools_mate():
    # when
    board_string = f"""br-bk-bb-oo-bc-bb-bk-br
            bp-bp-bp-bp-oo-bp-bp-bp
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-wp-bq
            oo-oo-oo-oo-oo-wp-oo-oo
            wp-wp-wp-wp-wp-oo-oo-wp
            wr-wk-wb-wq-wc-wb-wk-wr"""
    board = Board(board_string=board_string)

    # then
    assert is_checkmate(board=board, current_player="white")


def test_is_checkmate_friendly_piece_can_save_king():
    # when
    board_string = f"""br-oo-wq-bq-bc-bb-oo-br
            bp-bp-oo-oo-oo-oo-oo-oo
            bb-oo-oo-oo-oo-bp-oo-oo
            wp-oo-wb-oo-oo-oo-oo-wb
            oo-oo-oo-oo-oo-oo-oo-oo
            wk-oo-oo-oo-oo-oo-oo-oo
            oo-wp-wc-oo-oo-oo-wp-oo
            oo-wr-oo-bk-oo-oo-wk-wr"""
    board = Board(board_string=board_string)

    # then
    assert not is_checkmate(board=board, current_player="black")


def test_is_checkmate_friendly_piece_can_save_king_two():
    # when
    board_string = f"""br-oo-oo-oo-oo-bb-oo-br
            bp-bp-oo-bb-oo-oo-bp-bp
            bk-oo-oo-bp-oo-bc-oo-oo
            oo-wb-oo-oo-bp-oo-oo-oo
            oo-oo-wp-oo-wp-wp-bk-oo
            wp-oo-wp-oo-oo-oo-oo-oo
            oo-wb-oo-oo-oo-bq-wp-wp
            wr-wk-oo-oo-oo-wq-wc-wr"""
    board = Board(board_string=board_string)

    # then
    assert not is_checkmate(board=board, current_player="white")


def test_is_checkmate_another_scenario():
    # when
    board_string = f"""br-oo-oo-wq-oo-bc-oo-br
            oo-oo-oo-oo-bk-oo-bp-oo
            oo-wb-oo-oo-wp-bp-oo-oo
            oo-bp-oo-oo-oo-wp-wk-oo
            bq-wp-oo-oo-wp-oo-oo-bp
            bb-oo-wp-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-wk-oo-wb-oo-wk-oo-wr"""
    board = Board(board_string=board_string)

    # then
    assert not is_checkmate(board=board, current_player="black")


def test_validate_move_candidates_restricted_king():
    # when
    board_string = f"""oo-bk-bb-oo-oo-bb-oo-oo
            oo-oo-oo-oo-bk-oo-oo-br
            oo-oo-bp-oo-oo-oo-bk-oo
            oo-oo-bp-oo-bp-oo-oo-bp
            oo-oo-oo-wq-wk-bp-oo-wp
            wb-oo-oo-wp-oo-oo-oo-oo
            br-oo-oo-oo-oo-oo-oo-wc
            oo-oo-oo-oo-oo-wb-oo-wr"""
    board = Board(board_string=board_string)
    move_candidates = get_king_move_candidates(board=board, position=(7, 6))
    result = tuple(
        validate_move_candidates(board=board, move_candidates=move_candidates)
    )

    # then
    assert result == (
        RegularMove(
            piece_moves=(((7, 6), (6, 7)),),
            moving_pieces=(board[7, 6],),
            is_capturing_move=False,
        ),
    )


def test_validate_move_candidates_pawn_cant_move():
    # when
    board_string = f"""oo-bk-bb-oo-oo-bb-oo-oo
            bc-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-br-oo-wp-wc
            oo-oo-oo-oo-oo-oo-oo-oo"""
    board = Board(board_string=board_string)
    move_candidates = get_pawn_move_candidates(board=board, position=(6, 6))
    result = tuple(
        validate_move_candidates(board=board, move_candidates=move_candidates)
    )

    # then
    assert result == ()
