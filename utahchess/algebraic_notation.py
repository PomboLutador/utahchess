from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AlgebraicNotation:
    castling_identifier: str
    en_passant_identifer: str
    piece: str
    destination_tile: str
    capturing_flag: str

    def to_string(self) -> str:
        if self.castling_identifier:
            return self.castling_identifier
        return f"{self.piece}{self.capturing_flag}{self.destination_tile}{self.en_passant_identifer}"

    def __repr__(self) -> str:
        return self.to_string()

    def to_string_with_file(self, file: str) -> str:
        return f"{self.piece}{file}{self.capturing_flag}{self.destination_tile}{self.en_passant_identifer}"

    def to_string_with_rank(self, rank: str) -> str:
        return f"{self.piece}{rank}{self.capturing_flag}{self.destination_tile}{self.en_passant_identifer}"
