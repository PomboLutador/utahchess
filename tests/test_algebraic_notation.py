import pytest

from utahchess.algebraic_notation import (
    file_to_x_index,
    get_algebraic_notation_mapping,
    rank_to_y_index,
    x_index_to_file,
    y_index_to_rank,
)
from utahchess.board import Board
from utahchess.move_validation import RegularMove, make_regular_move


@pytest.mark.parametrize(
    ("x_index", "expected_file"),
    [
        (0, "a"),
        (1, "b"),
        (2, "c"),
        (3, "d"),
        (4, "e"),
        (5, "f"),
        (6, "g"),
        (7, "h"),
    ],
)
def test_x_index_to_file(x_index, expected_file):
    # when
    result = x_index_to_file(x=x_index)

    # then
    assert result == expected_file


@pytest.mark.parametrize(
    ("y_index", "expected_rank"),
    [
        (0, "8"),
        (1, "7"),
        (2, "6"),
        (3, "5"),
        (4, "4"),
        (5, "3"),
        (6, "2"),
        (7, "1"),
    ],
)
def test_y_index_to_rank(y_index, expected_rank):
    # when
    result = y_index_to_rank(y=y_index)

    # then
    assert result == expected_rank


@pytest.mark.parametrize(
    ("rank", "expected_y_index"),
    [
        ("8", 0),
        ("7", 1),
        ("6", 2),
        ("5", 3),
        ("4", 4),
        ("3", 5),
        ("2", 6),
        ("1", 7),
    ],
)
def test_rank_to_y_index(rank, expected_y_index):
    # when
    result = rank_to_y_index(rank=rank)

    # then
    assert result == expected_y_index


@pytest.mark.parametrize(
    ("file", "expected_x_index"),
    [
        ("a", 0),
        ("b", 1),
        ("c", 2),
        ("d", 3),
        ("e", 4),
        ("f", 5),
        ("g", 6),
        ("h", 7),
    ],
)
def test_file_to_x_index(file, expected_x_index):
    # when
    result = file_to_x_index(file=file)

    # then
    assert result == expected_x_index


@pytest.mark.parametrize(
    ("board_string", "expected_legal_moves_in_algebraic_notation", "current_player"),
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
                "Ra1",
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
def test_get_algebraic_notation_mapping(
    board_string, expected_legal_moves_in_algebraic_notation, current_player
):
    # given
    board = Board(board_string=board_string)

    # when
    result = tuple(
        get_algebraic_notation_mapping(
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
def test_get_algebraic_notation_mapping_with_last_move_for_en_passant(
    board_string, expected_legal_moves_in_algebraic_notation, current_player, pawn_move
):
    # given
    board = Board(board_string=board_string)
    move_to_make = RegularMove(
        piece_moves=pawn_move,
        moving_pieces=(board[pawn_move[0][0]],),
        is_capturing_move=False,
        allows_en_passant=True,
    )
    board_after_move = make_regular_move(board=board, move=move_to_make)

    # when
    result = tuple(
        get_algebraic_notation_mapping(
            board=board_after_move,
            current_player=current_player,
            last_move=move_to_make,
        ).keys()
    )

    # then
    assert len(result) == len(expected_legal_moves_in_algebraic_notation)
    assert set(expected_legal_moves_in_algebraic_notation) == set(result)
