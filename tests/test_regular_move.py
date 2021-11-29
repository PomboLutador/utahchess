from utahchess.board import Board
from utahchess.regular_move import get_regular_moves


def test_get_regular_moves():
    # when and then
    board = Board()
    get_regular_moves(board=board, current_player="black")
    get_regular_moves(board=board, current_player="white")
