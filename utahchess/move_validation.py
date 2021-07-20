from __future__ import annotations

from typing import Generator

from utahchess.board import Board
from utahchess.move import Move
from utahchess.piece import Piece


class RegularMove(Move):
    type = "Regular Move"

    def __init__(
        self,
        piece_moves: tuple[tuple[int, int], tuple[int, int]],
        moving_pieces: tuple[Piece],
    ) -> None:
        self.piece_moves = piece_moves
        self.moving_pieces = moving_pieces


def get_all_move_candidates(
    board: Board,
) -> Generator[tuple[tuple[int, int], tuple[int, int]], None, None]:
    pass


def is_check(board: Board) -> bool:
    pass


def is_checkmate(board: Board) -> bool:
    pass


def validate_move_candidates(
    move_candidates: Generator[tuple[tuple[int, int], tuple[int, int]], None, None]
) -> Generator[RegularMove, None, None]:
    pass
