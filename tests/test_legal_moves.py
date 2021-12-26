import pytest

from utahchess.board import Board
from utahchess.legal_moves import get_move_per_algebraic_identifier, is_checkmate
from utahchess.move import REGULAR_MOVE, Move, make_move


@pytest.mark.parametrize(
    (
        "board_string",
        "expected_legal_moves_in_algebraic_notation",
        "current_player",
    ),
    [
        (
            f"""bk-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-wk""",
            ("Kb7", "Kb8", "Ka7"),
            "black",
        ),
        (
            f"""bk-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-wk""",
            ("Kg2", "Kg1", "Kh2"),
            "white",
        ),
        (
            f"""bk-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-br-oo-oo-oo-wp-oo-wk""",
            ("Kg2", "Kg1", "Kh2"),
            "white",
        ),
        (
            f"""bk-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            bb-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            wr-oo-oo-oo-oo-wp-oo-wk""",
            ("Kb7", "Kb8", "Ka7"),
            "black",
        ),
        (
            f"""br-oo-oo-oo-bk-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-wk""",
            (
                "Kf8",
                "Kf7",
                "Kd7",
                "Ke7",
                "Kd8",
                "O-O-O",
                "Ra1+",
                "Ra2",
                "Ra3",
                "Ra4",
                "Ra5",
                "Ra6",
                "Ra7",
                "Rb8",
                "Rc8",
                "Rd8",
            ),
            "black",
        ),
        (
            f"""bk-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            bb-oo-oo-oo-oo-oo-oo-bn
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-bn
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            wr-oo-oo-oo-oo-wp-oo-wk""",
            (
                "Kb7",
                "Kb8",
                "Ka7",
                "N6f5",
                "N4f5",
                "Ng8",
                "Nf7",
                "Ng4",
                "Nf3",
                "Ng6",
                "Ng2",
            ),
            "black",
        ),
        (
            f"""bk-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            bb-oo-oo-oo-oo-bn-oo-bn
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            wr-oo-oo-oo-oo-wp-oo-wk""",
            (
                "Kb7",
                "Kb8",
                "Ka7",
                "Nfg8",
                "Nhg8",
                "Nfg4",
                "Nhg4",
                "Nh5",
                "Nf5",
                "Nf7",
                "Ne8",
                "Ne4",
                "Nd7",
                "Nd5",
                "Nh7",
            ),
            "black",
        ),
    ],
)
def test_get_move_per_algebraic_identifier(
    board_string, expected_legal_moves_in_algebraic_notation, current_player
):
    # given
    board = Board(board_string=board_string)

    # when
    result = tuple(
        get_move_per_algebraic_identifier(
            board=board, current_player=current_player, last_move=None
        ).keys()
    )

    # then
    assert len(expected_legal_moves_in_algebraic_notation) == len(result)
    assert set(expected_legal_moves_in_algebraic_notation) == set(result)


@pytest.mark.parametrize(
    (
        "board_string",
        "expected_legal_moves_in_algebraic_notation",
        "current_player",
        "pawn_move",
    ),
    [
        (
            f"""bk-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-wp-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-wk""",
            (
                "Kb7",
                "Kb8",
                "Ka7",
                "e3",
                "xd3 e.p.",
            ),
            "black",
            (
                (
                    (3, 6),
                    (3, 4),
                ),
            ),
        ),
        (
            f"""bk-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-wp-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-wk""",
            (
                "Kg2",
                "Kg1",
                "Kh2",
                "d6",
                "xe6 e.p.",
            ),
            "white",
            (
                (
                    (4, 1),
                    (4, 3),
                ),
            ),
        ),
    ],
)
def test_get_move_per_algebraic_identifier_with_last_move_for_en_passant(
    board_string,
    expected_legal_moves_in_algebraic_notation,
    current_player,
    pawn_move,
):
    # given
    board = Board(board_string=board_string)
    move_to_make = Move(
        type=REGULAR_MOVE,
        piece_moves=pawn_move,
        moving_pieces=(board[pawn_move[0][0]],),
        is_capturing_move=False,
        allows_en_passant=True,
    )
    board_after_move = make_move(board=board, move=move_to_make)

    # when
    result = tuple(
        get_move_per_algebraic_identifier(
            board=board_after_move,
            current_player=current_player,
            last_move=move_to_make,
        ).keys()
    )

    # then
    assert len(result) == len(expected_legal_moves_in_algebraic_notation)
    assert set(expected_legal_moves_in_algebraic_notation) == set(result)


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
