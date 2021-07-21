from utahchess.board import Board
from utahchess.move_validation import is_check, is_checkmate


def test_fools_mate():
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


def test_friendly_piece_can_save_king():
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


def test_friendly_piece_can_save_king_two():
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


def test_another_scenario():
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
