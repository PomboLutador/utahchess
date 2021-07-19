from __future__ import annotations

import abc
from dataclasses import dataclass
from itertools import chain
from typing import TYPE_CHECKING, Generator

if TYPE_CHECKING:
    from utahchess.board import Board, is_edible, is_occupied

from utahchess.tile_movement_utils import apply_movement_vector, is_in_bounds


class Piece(abc.ABC):
    piece_type: str
    position: tuple[int, int]
    color: str
    is_in_start_position: bool


@dataclass
class Pawn(Piece):
    piece_type = "Pawn"
    position: tuple[int, int]
    color: str
    is_in_start_position: bool

    def __init__(
        self, position: tuple[int, int], color: str, is_in_start_position: bool = True
    ) -> None:
        self.position = position
        self.color = color
        self.is_in_start_position = is_in_start_position


@dataclass
class Knight(Piece):
    piece_type = "Knight"
    position: tuple[int, int]
    color: str
    is_in_start_position: bool

    def __init__(
        self, position: tuple[int, int], color: str, is_in_start_position: bool = True
    ) -> None:
        self.position = position
        self.color = color
        self.is_in_start_position = is_in_start_position


@dataclass
class Rook(Piece):
    piece_type = "Rook"
    position: tuple[int, int]
    color: str
    is_in_start_position: bool

    def __init__(
        self, position: tuple[int, int], color: str, is_in_start_position: bool = True
    ) -> None:
        self.position = position
        self.color = color
        self.is_in_start_position = is_in_start_position


@dataclass
class Bishop(Piece):
    piece_type = "Bishop"
    position: tuple[int, int]
    color: str
    is_in_start_position: bool

    def __init__(
        self, position: tuple[int, int], color: str, is_in_start_position: bool = True
    ) -> None:
        self.position = position
        self.color = color
        self.is_in_start_position = is_in_start_position


@dataclass
class Queen(Piece):
    piece_type = "Queen"
    position: tuple[int, int]
    color: str
    is_in_start_position: bool

    def __init__(
        self, position: tuple[int, int], color: str, is_in_start_position: bool = True
    ) -> None:
        self.position = position
        self.color = color
        self.is_in_start_position = is_in_start_position


@dataclass
class King(Piece):
    piece_type = "King"
    position: tuple[int, int]
    color: str
    is_in_start_position: bool

    def __init__(
        self, position: tuple[int, int], color: str, is_in_start_position: bool = True
    ) -> None:
        self.position = position
        self.color = color
        self.is_in_start_position = is_in_start_position


INITIAL_BLACK_PAWNS = tuple(
    Pawn(position=indices, color="black")
    for indices in ((x_coord, 1) for x_coord in range(8))
)
INITIAL_WHITE_PAWNS = tuple(
    Pawn(position=indices, color="white")
    for indices in ((x_coord, 6) for x_coord in range(8))
)
INITIAL_KNIGHTS = tuple(
    Knight(position=indices, color="black") for indices in ((1, 0), (6, 0))
) + tuple(Knight(position=indices, color="white") for indices in ((1, 7), (6, 7)))
INITIAL_ROOKS = tuple(
    Rook(position=indices, color="black") for indices in ((0, 0), (7, 0))
) + tuple(Rook(position=indices, color="white") for indices in ((0, 7), (7, 7)))
INITIAL_BISHOPS = tuple(
    Bishop(position=indices, color="black") for indices in ((2, 0), (5, 0))
) + tuple(Bishop(position=indices, color="white") for indices in ((2, 7), (5, 7)))
INITIAL_QUEENS = (
    Queen(position=(3, 0), color="black"),
    Queen(position=(3, 7), color="white"),
)
INITIAL_KINGS = (
    King(position=(4, 0), color="black"),
    King(position=(4, 7), color="white"),
)


def get_initial_pieces() -> Generator[Piece, None, None]:

    for piece in (
        INITIAL_BLACK_PAWNS
        + INITIAL_WHITE_PAWNS
        + INITIAL_BISHOPS
        + INITIAL_KINGS
        + INITIAL_KNIGHTS
        + INITIAL_QUEENS
        + INITIAL_ROOKS
    ):
        yield piece


if __name__ == "__main__":
    p = Pawn((0, 0), "white")
    p2 = Pawn((0, 0), "black")
    print(p == p2)
