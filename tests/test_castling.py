from utahchess.board import Board
from utahchess.castling import CastlingMove, get_castling_moves


def test_castling_top_left():
    # when
    board_string = f"""br-oo-oo-oo-bc-bb-bk-br
            bp-bp-bp-bp-bq-bp-bp-bp
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-wp-oo
            oo-oo-oo-oo-oo-wp-oo-oo
            wp-wp-wp-wp-wp-oo-oo-wp
            wr-wk-wb-wq-wc-wb-wk-wr"""
    board = Board(board_string=board_string)
    expected_piece_moves = (
        ((0, 0), (3, 0)),
        ((4, 0), (2, 0)),
    )
    expected = (
        CastlingMove(
            piece_moves=expected_piece_moves, moving_pieces=(board[0, 0], board[4, 0])
        ),
    )

    # then
    actual = tuple(get_castling_moves(board=board, current_player="black"))
    assert expected == actual


def test_castling_top_right():
    # when
    board_string = f"""br-bk-bb-oo-bc-oo-oo-br
            bp-bp-bp-bp-bq-bp-bp-bp
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-wp-oo
            oo-oo-oo-oo-oo-wp-oo-oo
            wp-wp-wp-wp-wp-oo-oo-wp
            wr-wk-wb-wq-wc-wb-wk-wr"""
    board = Board(board_string=board_string)
    expected_piece_moves = (
        ((7, 0), (5, 0)),
        ((4, 0), (6, 0)),
    )
    expected = (
        CastlingMove(
            piece_moves=expected_piece_moves, moving_pieces=(board[7, 0], board[4, 0])
        ),
    )

    # then
    actual = tuple(get_castling_moves(board=board, current_player="black"))
    assert expected == actual


def test_castling_bottom_left():
    # when
    board_string = f"""br-bk-bb-oo-bc-bb-bk-br
            bp-bp-bp-bp-bq-bp-bp-bp
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-wp-oo
            oo-oo-oo-oo-oo-wp-oo-oo
            wp-wp-wp-wp-wp-oo-oo-wp
            wr-oo-oo-oo-wc-wb-wk-wr"""
    board = Board(board_string=board_string)
    expected_piece_moves = (
        ((0, 7), (3, 7)),
        ((4, 7), (2, 7)),
    )
    expected = (
        CastlingMove(
            piece_moves=expected_piece_moves, moving_pieces=(board[0, 7], board[4, 7])
        ),
    )

    # then
    actual = tuple(get_castling_moves(board=board, current_player=("white")))
    assert expected == actual


def test_castling_bottom_right():
    # when
    board_string = f"""br-bk-bb-oo-bc-bb-bk-br
            bp-bp-bp-bp-bq-bp-bp-bp
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-wp-oo
            oo-oo-oo-oo-oo-wp-oo-oo
            wp-wp-wp-wp-wp-oo-oo-wp
            wr-wk-wb-wq-wc-oo-oo-wr"""
    board = Board(board_string=board_string)

    expected_piece_moves = (
        ((7, 7), (5, 7)),
        ((4, 7), (6, 7)),
    )
    expected = (
        CastlingMove(
            piece_moves=expected_piece_moves, moving_pieces=(board[7, 7], board[4, 7])
        ),
    )

    # then
    actual = tuple(get_castling_moves(board=board, current_player=("white")))
    assert expected == actual
