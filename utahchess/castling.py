from __future__ import annotations

from utahchess.board import Board
from utahchess.move import Move
from utahchess.piece import Piece


class CastlingMove(Move):
    type = "Castling Move"

    def __init__(
        self,
        piece_moves: tuple[
            tuple[tuple[int, int], tuple[int, int]],
            tuple[tuple[int, int], tuple[int, int]],
        ],
        moving_pieces: tuple[Piece, Piece],
    ) -> None:
        self.piece_moves = piece_moves
        self.moving_pieces = moving_pieces

    def get_rook_piece_move(self) -> tuple[int, int]:
        pass

    def get_king_piece_move(self) -> tuple[int, int]:
        pass
