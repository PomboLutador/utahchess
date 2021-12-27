import pytest

from utahchess import BLACK, WHITE
from utahchess.board import Board
from utahchess.castling import get_castling_moves
from utahchess.move import LONG_CASTLING, SHORT_CASTLING, Move, make_move


@pytest.mark.parametrize(
    (
        "board_string",
        "rook_from_position",
        "rook_to_position",
        "king_from_position",
        "king_to_position",
        "current_player",
        "castling_type",
    ),
    [
        (
            f"""br-oo-oo-oo-bk-bb-bn-br
            bp-bp-bp-bp-bq-bp-bp-bp
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-wp-oo
            oo-oo-oo-oo-oo-wp-oo-oo
            wp-wp-wp-wp-wp-oo-oo-wp
            wr-wn-wb-wq-wn-wb-wn-wr""",
            (0, 0),
            (3, 0),
            (4, 0),
            (2, 0),
            BLACK,
            LONG_CASTLING,
        ),
        (
            f"""br-bn-bb-oo-bk-oo-oo-br
            bp-bp-bp-bp-bq-bp-bp-bp
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-wp-oo
            oo-oo-oo-oo-oo-wp-oo-oo
            wp-wp-wp-wp-wp-oo-oo-wp
            wr-wn-wb-wq-wk-wb-wn-wr""",
            (7, 0),
            (5, 0),
            (4, 0),
            (6, 0),
            BLACK,
            SHORT_CASTLING,
        ),
        (
            f"""br-bn-bb-oo-bk-bb-bn-br
            bp-bp-bp-bp-bq-bp-bp-bp
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-wp-oo
            oo-oo-oo-oo-oo-wp-oo-oo
            wp-wp-wp-wp-wp-oo-oo-wp
            wr-oo-oo-oo-wk-wb-wn-wr""",
            (0, 7),
            (3, 7),
            (4, 7),
            (2, 7),
            WHITE,
            LONG_CASTLING,
        ),
        (
            f"""br-bn-bb-oo-bk-bb-bn-br
            bp-bp-bp-bp-bq-bp-bp-bp
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-wp-oo
            oo-oo-oo-oo-oo-wp-oo-oo
            wp-wp-wp-wp-wp-oo-oo-wp
            wr-wn-wb-wq-wk-oo-oo-wr""",
            (7, 7),
            (5, 7),
            (4, 7),
            (6, 7),
            WHITE,
            SHORT_CASTLING,
        ),
    ],
)
def test_castling_in_corners(
    board_string,
    rook_from_position,
    rook_to_position,
    king_from_position,
    king_to_position,
    current_player,
    castling_type,
):
    # when
    board = Board(board_string=board_string)
    expected_piece_moves = (
        (king_from_position, king_to_position),
        (rook_from_position, rook_to_position),
    )
    expected = (
        Move(
            type=castling_type,
            piece_moves=expected_piece_moves,
            moving_pieces=(
                board[king_from_position],
                board[rook_from_position],
            ),
            is_capturing_move=False,
            allows_en_passant=False,
        ),
    )

    # then
    actual = tuple(get_castling_moves(board=board, current_player=current_player))
    assert expected == actual


@pytest.mark.parametrize(
    (
        "board_string",
        "rook_position_left",
        "rook_position_right",
        "king_position",
        "current_player",
    ),
    [
        (
            f"""br-bn-bb-oo-bk-bb-bn-br
            bp-bp-bp-bp-bq-bp-bp-bp
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-wp-oo
            oo-oo-oo-oo-oo-wp-oo-oo
            wp-wp-wp-wp-wp-oo-oo-wp
            wr-oo-oo-oo-wk-oo-oo-wr""",
            (0, 7),
            (7, 7),
            (4, 7),
            WHITE,
        ),
        (
            f"""br-oo-oo-oo-bk-oo-oo-br
            bp-bp-bp-bp-bq-bp-bp-bp
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-wp-oo
            oo-oo-oo-oo-oo-wp-oo-oo
            wp-wp-wp-wp-wp-oo-oo-wp
            wr-oo-oo-oo-wk-oo-oo-wr""",
            (0, 0),
            (7, 0),
            (4, 0),
            BLACK,
        ),
    ],
)
def test_castling_both_sides(
    board_string,
    rook_position_left,
    rook_position_right,
    king_position,
    current_player,
):
    # when
    board = Board(board_string=board_string)
    expected_piece_moves_right = (
        (king_position, (king_position[0] + 2, king_position[1])),
        (
            rook_position_right,
            (rook_position_right[0] - 2, rook_position_right[1]),
        ),
    )
    expected_piece_moves_left = (
        (king_position, (king_position[0] - 2, king_position[1])),
        (
            rook_position_left,
            (rook_position_left[0] + 3, rook_position_left[1]),
        ),
    )
    expected = (
        Move(
            type=SHORT_CASTLING,
            piece_moves=expected_piece_moves_right,
            moving_pieces=(board[king_position], board[rook_position_right]),
            is_capturing_move=False,
            allows_en_passant=False,
        ),
        Move(
            type=LONG_CASTLING,
            piece_moves=expected_piece_moves_left,
            moving_pieces=(board[king_position], board[rook_position_left]),
            is_capturing_move=False,
            allows_en_passant=False,
        ),
    )

    # then
    actual = tuple(get_castling_moves(board=board, current_player=current_player))
    assert expected == actual


def test_no_rook_for_castling_bottom():
    # when
    board_string = f"""br-bn-bb-oo-bk-bb-bn-br
            bp-bp-bp-bp-bq-bp-bp-bp
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-wp-oo
            oo-oo-oo-oo-oo-wp-oo-oo
            wp-wp-wp-wp-wp-oo-oo-wp
            oo-oo-oo-oo-wk-oo-oo-oo"""
    board = Board(board_string=board_string)
    expected = ()

    # then
    actual = tuple(get_castling_moves(board=board, current_player=WHITE))
    assert expected == actual


def test_no_rook_for_castling_top():
    # when
    board_string = f"""oo-oo-oo-oo-bk-oo-oo-oo
            bp-bp-bp-bp-bq-bp-bp-bp
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-wp-oo
            oo-oo-oo-oo-oo-wp-oo-oo
            wp-wp-wp-wp-wp-oo-oo-wp
            oo-oo-oo-oo-wk-oo-oo-oo"""
    board = Board(board_string=board_string)
    expected = ()

    # then
    actual = tuple(get_castling_moves(board=board, current_player=BLACK))
    assert expected == actual


def test_black_cant_castle_through_check():
    # when
    board_string = f"""br-oo-oo-oo-bk-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-wq-wk-oo-oo-oo"""
    board = Board(board_string=board_string)
    expected = ()

    # then
    actual = tuple(get_castling_moves(board=board, current_player=BLACK))
    assert expected == actual


def test_black_cant_castle_into_check():
    # when
    board_string = f"""br-oo-oo-oo-bk-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-wq-wk-oo-oo-oo-oo"""
    board = Board(board_string=board_string)
    expected = ()

    # then
    actual = tuple(get_castling_moves(board=board, current_player=BLACK))
    assert expected == actual


def test_black_cant_castle_out_of_check():
    # when
    board_string = f"""br-oo-oo-oo-bk-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-wk-wq-oo-oo-oo"""
    board = Board(board_string=board_string)
    expected = ()

    # then
    actual = tuple(get_castling_moves(board=board, current_player=BLACK))
    assert expected == actual


@pytest.mark.parametrize(
    (
        "board_string",
        "rook_position",
        "king_position",
        "expected_board_after_move",
    ),
    [
        (
            f"""br-bn-bb-oo-bk-bb-bn-br
            bp-bp-bp-bp-bq-bp-bp-bp
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-wp-oo
            oo-oo-oo-oo-oo-wp-oo-oo
            wp-wp-wp-wp-wp-oo-oo-wp
            wr-oo-oo-oo-wk-oo-oo-wr""",
            (0, 7),
            (4, 7),
            f"""br-bn-bb-oo-bk-bb-bn-br
            bp-bp-bp-bp-bq-bp-bp-bp
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-wp-oo
            oo-oo-oo-oo-oo-wp-oo-oo
            wp-wp-wp-wp-wp-oo-oo-wp
            oo-oo-wk-wr-oo-oo-oo-wr""",
        ),
    ],
)
def test_make_castling_move(
    board_string, rook_position, king_position, expected_board_after_move
):
    # when
    board = Board(board_string=board_string)
    expected_piece_moves_left = (
        (king_position, (king_position[0] - 2, king_position[1])),
        (rook_position, (rook_position[0] + 3, rook_position[1])),
    )
    castling_move = Move(
        type=LONG_CASTLING,
        piece_moves=expected_piece_moves_left,
        moving_pieces=(board[king_position], board[rook_position]),
        is_capturing_move=False,
        allows_en_passant=False,
    )

    # when
    actual = make_move(board=board, move=castling_move)

    # then
    assert Board(board_string=expected_board_after_move) == actual
