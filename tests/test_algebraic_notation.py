import pytest

from utahchess.algebraic_notation import get_algebraic_identifer
from utahchess.board import Board
from utahchess.castling import get_castling_moves
from utahchess.move import EN_PASSANT_MOVE, REGULAR_MOVE, Move


def test_get_algebraic_identifer_with_regular_move():
    # given
    board = Board()
    move = Move(
        type=REGULAR_MOVE,
        piece_moves=(((1, 1), (1, 3)),),
        moving_pieces=(board[(1, 1)],),
        is_capturing_move=False,
        allows_en_passant=True,
    )

    # when
    result = get_algebraic_identifer(move=move, board=board)

    # then
    assert result == "b5"


def test_get_algebraic_identifier_with_checkmate():
    # given
    board = Board(
        board_string=(
            f"""br-bn-bb-bq-bk-bb-bn-br
            bp-bp-bp-bp-oo-bp-bp-bp
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-wp-oo
            oo-oo-oo-oo-oo-wp-oo-oo
            wp-wp-wp-wp-wp-oo-oo-wp
            wr-wn-wb-wq-wk-wb-wn-wr"""
        )
    )
    move = Move(
        type=REGULAR_MOVE,
        piece_moves=(((3, 0), (7, 4)),),
        moving_pieces=(board[(3, 0)],),
        is_capturing_move=False,
        allows_en_passant=False,
    )

    # when
    result = get_algebraic_identifer(move=move, board=board)

    # then
    assert result == "Qh4#"


def test_get_algebraic_identifier_with_check():
    # given
    board = Board(
        board_string=(
            f"""br-bn-bb-bq-bk-bb-bn-br
            bp-bp-bp-bp-oo-bp-bp-bp
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-wp-oo
            oo-oo-oo-wp-oo-wp-oo-oo
            wp-wp-wp-oo-wp-oo-oo-wp
            wr-wn-wb-wq-wk-wb-wn-wr"""
        )
    )
    move = Move(
        type=REGULAR_MOVE,
        piece_moves=(((3, 0), (7, 4)),),
        moving_pieces=(board[(3, 0)],),
        is_capturing_move=False,
        allows_en_passant=False,
    )

    # when
    result = get_algebraic_identifer(move=move, board=board)

    # then
    assert result == "Qh4+"


def test_get_algebraic_identifier_with_rank_and_file():
    # given
    board = Board(
        board_string=(
            f"""oo-bk-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-wk-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            wr-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            bn-oo-oo-oo-oo-oo-oo-wr"""
        )
    )
    move_1 = Move(
        type=REGULAR_MOVE,
        piece_moves=(((0, 5), (0, 7)),),
        moving_pieces=(board[(0, 5)],),
        is_capturing_move=True,
        allows_en_passant=False,
    )
    move_2 = Move(
        type=REGULAR_MOVE,
        piece_moves=(((7, 7), (0, 7)),),
        moving_pieces=(board[(7, 7)],),
        is_capturing_move=True,
        allows_en_passant=False,
    )

    # when
    identifier_1_without_rank_or_file = get_algebraic_identifer(
        move=move_1, board=board
    )
    identifier_2_without_rank_or_file = get_algebraic_identifer(
        move=move_2, board=board
    )
    identifier_1 = get_algebraic_identifer(move=move_1, board=board, file="a")
    identifier_2 = get_algebraic_identifer(move=move_2, board=board, file="h")

    # then
    assert identifier_1_without_rank_or_file == identifier_2_without_rank_or_file
    assert identifier_1 == "Raxa1"
    assert identifier_2 == "Rhxa1"


def test_get_algebraic_identifer_with_en_passant_move():
    # given
    board = Board(
        board_string=f"""oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-bk-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            wp-bp-wp-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-wk-oo-oo-oo"""
    )
    move = Move(
        type=EN_PASSANT_MOVE,
        piece_moves=(((2, 3), (1, 2)),),
        moving_pieces=(board[2, 3],),
        pieces_to_delete=((1, 3),),
        is_capturing_move=True,
        allows_en_passant=False,
    )

    # when
    result = get_algebraic_identifer(move=move, board=board)

    # then
    assert result == "xb6 e.p."


@pytest.mark.parametrize(
    ("board_string", "current_player", "expected"),
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
            "black",
            "O-O-O",
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
            "black",
            "O-O",
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
            "white",
            "O-O-O",
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
            "white",
            "O-O",
        ),
    ],
)
def test_get_algebraic_identifer_with_castling_move(
    board_string, current_player, expected
):
    # given
    board = Board(board_string=board_string)
    castling_move = tuple(
        get_castling_moves(board=board, current_player=current_player)
    )[0]

    # when
    result = get_algebraic_identifer(move=castling_move, board=board)

    # then
    assert expected == result
