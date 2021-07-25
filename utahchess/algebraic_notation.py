from __future__ import annotations

from utahchess.board import Board
from utahchess.move import Move

FILE_POSSIBILITIES = "abcdefgh"
RANK_POSSIBILITIES = "87654321"


def x_index_to_file(x: int) -> str:
    return FILE_POSSIBILITIES[x]


def y_index_to_rank(y: int) -> str:
    return RANK_POSSIBILITIES[y]
