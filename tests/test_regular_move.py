from utahchess import BLACK, WHITE
from utahchess.board import Board
from utahchess.regular_move import get_regular_moves


def test_get_regular_moves(
    initial_board_with_only_rooks,
    initial_board_with_only_bishops,
    initial_board_with_only_queens,
    initial_board_with_only_kings,
):
    # when and then
    board = Board()
    for current_player in (WHITE, BLACK):
        get_regular_moves(board=board, current_player=current_player)
        get_regular_moves(
            board=initial_board_with_only_rooks, current_player=current_player
        )
        get_regular_moves(
            board=initial_board_with_only_bishops, current_player=current_player
        )
        get_regular_moves(
            board=initial_board_with_only_queens, current_player=current_player
        )
        get_regular_moves(
            board=initial_board_with_only_kings, current_player=current_player
        )
