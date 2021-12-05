import pytest

from utahchess.board import Board
from utahchess.legal_moves import make_move
from utahchess.move import REGULAR_MOVE, Move
from utahchess.move_candidates import get_king_move_candidates, get_pawn_move_candidates
from utahchess.move_validation import is_checkmate, is_valid_move


def test_is_checkmate_fools_mate():
    # when
    board_string = f"""br-bn-bb-oo-bk-bb-bn-br
            bp-bp-bp-bp-oo-bp-bp-bp
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-wp-bq
            oo-oo-oo-oo-oo-wp-oo-oo
            wp-wp-wp-wp-wp-oo-oo-wp
            wr-wn-wb-wq-wk-wb-wn-wr"""
    board = Board(board_string=board_string)

    # then
    assert is_checkmate(board=board, current_player="white")


def test_is_checkmate_friendly_piece_can_save_king():
    # when
    board_string = f"""br-oo-wq-bq-bk-bb-oo-br
            bp-bp-oo-oo-oo-oo-oo-oo
            bb-oo-oo-oo-oo-bp-oo-oo
            wp-oo-wb-oo-oo-oo-oo-wb
            oo-oo-oo-oo-oo-oo-oo-oo
            wn-oo-oo-oo-oo-oo-oo-oo
            oo-wp-wk-oo-oo-oo-wp-oo
            oo-wr-oo-bn-oo-oo-wn-wr"""
    board = Board(board_string=board_string)

    # then
    assert not is_checkmate(board=board, current_player="black")


def test_is_checkmate_friendly_piece_can_save_king_two():
    # when
    board_string = f"""br-oo-oo-oo-oo-bb-oo-br
            bp-bp-oo-bb-oo-oo-bp-bp
            bn-oo-oo-bp-oo-bk-oo-oo
            oo-wb-oo-oo-bp-oo-oo-oo
            oo-oo-wp-oo-wp-wp-bn-oo
            wp-oo-wp-oo-oo-oo-oo-oo
            oo-wb-oo-oo-oo-bq-wp-wp
            wr-wn-oo-oo-oo-wq-wk-wr"""
    board = Board(board_string=board_string)

    # then
    assert not is_checkmate(board=board, current_player="white")


def test_is_checkmate_another_scenario():
    # when
    board_string = f"""br-oo-oo-wq-oo-bk-oo-br
            oo-oo-oo-oo-bn-oo-bp-oo
            oo-wb-oo-oo-wp-bp-oo-oo
            oo-bp-oo-oo-oo-wp-wn-oo
            bq-wp-oo-oo-wp-oo-oo-bp
            bb-oo-wp-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-wn-oo-wb-oo-wn-oo-wr"""
    board = Board(board_string=board_string)

    # then
    assert not is_checkmate(board=board, current_player="black")


def test_is_valid_move_restricted_king():
    # when
    board_string = f"""oo-bn-bb-oo-oo-bb-oo-oo
            oo-oo-oo-oo-bn-oo-oo-br
            oo-oo-bp-oo-oo-oo-bn-oo
            oo-oo-bp-oo-bp-oo-oo-bp
            oo-oo-oo-wq-wn-bp-oo-wp
            wb-oo-oo-wp-oo-oo-oo-oo
            br-oo-oo-oo-oo-oo-oo-wk
            oo-oo-oo-oo-oo-wb-oo-wr"""
    board = Board(board_string=board_string)

    invalid_king_destinations = ((6, 6), (6, 5), (7, 5))
    invalid_king_moves = tuple(
        Move(
            type=REGULAR_MOVE,
            piece_moves=(((7, 6), invalid_king_destination),),
            moving_pieces=(board[7, 6],),
            is_capturing_move=False,
            allows_en_passant=False,
        )
        for invalid_king_destination in invalid_king_destinations
    )

    valid_king_destinations = ((6, 7),)
    valid_king_moves = tuple(
        Move(
            type=REGULAR_MOVE,
            piece_moves=(((7, 6), valid_king_destination),),
            moving_pieces=(board[7, 6],),
            is_capturing_move=False,
            allows_en_passant=False,
        )
        for valid_king_destination in valid_king_destinations
    )

    # then
    assert all(not is_valid_move(board=board, move=move) for move in invalid_king_moves)
    assert all(is_valid_move(board=board, move=move) for move in valid_king_moves)
    assert (
        len(
            tuple(
                get_king_move_candidates(
                    board=board,
                    position=(7, 6),
                )
            )
        )
        == 4
    )


def test_is_valid_move_pawn_cant_move():
    # when
    board_string = f"""oo-bn-bb-oo-oo-bb-oo-oo
            bk-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-br-oo-wp-wk
            oo-oo-oo-oo-oo-oo-oo-oo"""
    board = Board(board_string=board_string)
    move_candidates = get_pawn_move_candidates(board=board, position=(6, 6))

    # then
    assert all(
        tuple(
            not is_valid_move(
                board=board,
                move=Move(
                    type=REGULAR_MOVE,
                    piece_moves=(move_candidate,),
                    moving_pieces=(board[(6, 6)],),
                    allows_en_passant=False,
                    is_capturing_move=False,
                ),
            )
            for move_candidate in move_candidates
        )
    )


@pytest.mark.parametrize(
    ("board", "from_move", "to_move", "expected"),
    [
        (
            Board(
                board_string=f"""bk-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-wp-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-wk""",
            ),
            (7, 7),
            (7, 6),
            Board(
                board_string=f"""bk-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-wp-oo-oo-oo-wk
            oo-oo-oo-oo-oo-oo-oo-oo""",
            ),
        ),
        (
            Board(
                board_string=f"""bk-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-wp-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-wk""",
            ),
            (4, 4),
            (4, 5),
            Board(
                board_string=f"""bk-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-wp-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-wk""",
            ),
        ),
    ],
)
def test_make_regular_move(board, from_move, to_move, expected):
    # given
    regular_move = Move(
        type=REGULAR_MOVE,
        piece_moves=((from_move, to_move),),
        moving_pieces=board[from_move],
        is_capturing_move=False,
        allows_en_passant=False,
    )

    # when
    result = make_move(board=board, move=regular_move)

    # then
    assert result == expected
