from utahchess import BLACK
from utahchess.board import Board
from utahchess.chess import is_stalemate
from utahchess.legal_moves import get_move_per_algebraic_identifier


def test_is_stalemate():
    # given
    board = Board(
        board_string=f"""bk-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-wr
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-wr-oo-oo-oo-oo-oo-wk"""
    )
    black_legal_moves = tuple(
        get_move_per_algebraic_identifier(
            board=board, current_player=BLACK, last_move=None
        ).keys()
    )

    # when & then
    assert is_stalemate(
        board=board,
        current_player=BLACK,
        legal_moves_for_current_player=black_legal_moves,
    )


def test_is_not_stalemate():
    # given
    board = Board(
        board_string=f"""bk-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-wr-oo-oo-oo-oo-oo-wk"""
    )
    black_legal_moves = tuple(
        get_move_per_algebraic_identifier(
            board=board, current_player=BLACK, last_move=None
        ).keys()
    )

    # when & then
    assert not is_stalemate(
        board=board,
        current_player=BLACK,
        legal_moves_for_current_player=black_legal_moves,
    )
