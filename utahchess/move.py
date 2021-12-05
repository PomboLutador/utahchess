from __future__ import annotations

from dataclasses import dataclass

from utahchess.piece import Piece

SHORT_CASTLING = "Short Castling Move"
LONG_CASTLING = "Long Castling Move"
EN_PASSANT_MOVE = "En Passant Move"
REGULAR_MOVE = "Regular Move"


@dataclass(frozen=True)
class Move:
    type: str
    piece_moves: tuple[tuple[tuple[int, int], tuple[int, int]], ...]
    moving_pieces: tuple[Piece, ...]
    is_capturing_move: bool
    allows_en_passant: bool
    pieces_to_delete: tuple[tuple[int, int], ...] = ()

    # def to_string(self, **kwargs) -> str:
    #     pass

    # def to_string(self) -> str:
    #     if self.type:
    #         return self.castling_identifier
    #     return (
    #         f"{self.piece}{self.capturing_flag}{self.destination_tile}"
    #         f"{self.en_passant_identifer}{self.check_or_checkmate_flag}"
    #     )
