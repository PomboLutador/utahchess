from __future__ import annotations

import abc

from utahchess.piece import Piece


class Move(abc.ABC):
    move_type: str
    piece_moves: tuple[tuple[tuple[int, int], tuple[int, int]], ...]
    moving_pieces: tuple[Piece, ...]
    is_capturing_move: bool

    def get_algebraic_notation(self) -> str:
        pass
