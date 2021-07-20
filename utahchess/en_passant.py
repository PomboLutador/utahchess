from __future__ import annotations

from typing import Generator

from utahchess.board import Board
from utahchess.move import Move
from utahchess.piece import Piece


class EnPassantMove(Move):
    type = "En Passant Move"

    def __init__(
        self,
        piece_moves: tuple[tuple[int, int], tuple[int, int]],
        moving_pieces: tuple[Piece],
    ) -> None:
        self.piece_moves = piece_moves
        self.moving_pieces = moving_pieces

    def get_position_of_piece_to_remove(self) -> tuple[int, int]:
        pass


def get_en_passant_moves(board: Board) -> Generator[EnPassantMove, None, None]:
    pass


def complete_en_passant_move(board: Board, en_passant_move: EnPassantMove) -> Board:
    """Completes the capturing part of the en passant move."""
    pass
