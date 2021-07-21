import pytest

from utahchess.board import Board
from utahchess.castling import CastlingMove, get_castling_moves


@pytest.mark.parametrize(
    (
        "board_string",
        "rook_from_position",
        "rook_to_position",
        "king_from_position",
        "king_to_position",
        "current_player",
    ),
    [
        (
            f"""br-oo-oo-oo-bc-bb-bk-br
            bp-bp-bp-bp-bq-bp-bp-bp
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-wp-oo
            oo-oo-oo-oo-oo-wp-oo-oo
            wp-wp-wp-wp-wp-oo-oo-wp
            wr-wk-wb-wq-wc-wb-wk-wr""",
            (0, 0),
            (3, 0),
            (4, 0),
            (2, 0),
            "black",
        ),
        (
            f"""br-bk-bb-oo-bc-oo-oo-br
            bp-bp-bp-bp-bq-bp-bp-bp
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-wp-oo
            oo-oo-oo-oo-oo-wp-oo-oo
            wp-wp-wp-wp-wp-oo-oo-wp
            wr-wk-wb-wq-wc-wb-wk-wr""",
            (7, 0),
            (5, 0),
            (4, 0),
            (6, 0),
            "black",
        ),
        (
            f"""br-bk-bb-oo-bc-bb-bk-br
            bp-bp-bp-bp-bq-bp-bp-bp
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-wp-oo
            oo-oo-oo-oo-oo-wp-oo-oo
            wp-wp-wp-wp-wp-oo-oo-wp
            wr-oo-oo-oo-wc-wb-wk-wr""",
            (0, 7),
            (3, 7),
            (4, 7),
            (2, 7),
            "white",
        ),
        (
            f"""br-bk-bb-oo-bc-bb-bk-br
            bp-bp-bp-bp-bq-bp-bp-bp
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-wp-oo
            oo-oo-oo-oo-oo-wp-oo-oo
            wp-wp-wp-wp-wp-oo-oo-wp
            wr-wk-wb-wq-wc-oo-oo-wr""",
            (7, 7),
            (5, 7),
            (4, 7),
            (6, 7),
            "white",
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
):
    # when
    board = Board(board_string=board_string)
    expected_piece_moves = (
        (rook_from_position, rook_to_position),
        (king_from_position, king_to_position),
    )
    expected = (
        CastlingMove(
            piece_moves=expected_piece_moves,
            moving_pieces=(board[rook_from_position], board[king_from_position]),
        ),
    )

    # then
    actual = tuple(get_castling_moves(board=board, current_player=current_player))
    assert expected == actual
