from __future__ import annotations

from dataclasses import dataclass

from utahchess.piece import Piece


@dataclass(frozen=True)
class Move:
    type: str
    piece_moves: tuple[tuple[tuple[int, int], tuple[int, int]], ...]
    moving_pieces: tuple[Piece, ...]
    is_capturing_move: bool
    allows_en_passant: bool
    pieces_to_delete: tuple[tuple[int, int], ...] = ()
