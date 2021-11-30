from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import Generator, Optional


class Piece(abc.ABC):
    piece_type: str
    position: tuple[int, int]
    color: str
    is_in_start_position: bool


@dataclass(frozen=True)
class Pawn(Piece):
    piece_type = "Pawn"
    position: tuple[int, int]
    color: str
    is_in_start_position: bool

    def to_string(self) -> str:
        return f"{'b' if self.color == 'black' else 'w'}p"


@dataclass(frozen=True)
class Knight(Piece):
    piece_type = "Knight"
    position: tuple[int, int]
    color: str
    is_in_start_position: bool

    def to_string(self) -> str:
        return f"{'b' if self.color == 'black' else 'w'}n"


@dataclass(frozen=True)
class Rook(Piece):
    piece_type = "Rook"
    position: tuple[int, int]
    color: str
    is_in_start_position: bool

    def to_string(self) -> str:
        return f"{'b' if self.color == 'black' else 'w'}r"


@dataclass(frozen=True)
class Bishop(Piece):
    piece_type = "Bishop"
    position: tuple[int, int]
    color: str
    is_in_start_position: bool

    def to_string(self) -> str:
        return f"{'b' if self.color == 'black' else 'w'}b"


@dataclass(frozen=True)
class Queen(Piece):
    piece_type = "Queen"
    position: tuple[int, int]
    color: str
    is_in_start_position: bool

    def to_string(self) -> str:
        return f"{'b' if self.color == 'black' else 'w'}q"


@dataclass(frozen=True)
class King(Piece):
    piece_type = "King"
    position: tuple[int, int]
    color: str
    is_in_start_position: bool

    def to_string(self) -> str:
        return f"{'b' if self.color == 'black' else 'w'}k"


INITIAL_BLACK_PAWNS = tuple(
    Pawn(position=indices, color="black", is_in_start_position=True)
    for indices in ((x_coord, 1) for x_coord in range(8))
)
INITIAL_WHITE_PAWNS = tuple(
    Pawn(position=indices, color="white", is_in_start_position=True)
    for indices in ((x_coord, 6) for x_coord in range(8))
)
INITIAL_KNIGHTS = tuple(
    Knight(position=indices, color="black", is_in_start_position=True)
    for indices in ((1, 0), (6, 0))
) + tuple(
    Knight(position=indices, color="white", is_in_start_position=True)
    for indices in ((1, 7), (6, 7))
)
INITIAL_ROOKS = tuple(
    Rook(position=indices, color="black", is_in_start_position=True)
    for indices in ((0, 0), (7, 0))
) + tuple(
    Rook(position=indices, color="white", is_in_start_position=True)
    for indices in ((0, 7), (7, 7))
)
INITIAL_BISHOPS = tuple(
    Bishop(position=indices, color="black", is_in_start_position=True)
    for indices in ((2, 0), (5, 0))
) + tuple(
    Bishop(position=indices, color="white", is_in_start_position=True)
    for indices in ((2, 7), (5, 7))
)
INITIAL_QUEENS = (
    Queen(position=(3, 0), color="black", is_in_start_position=True),
    Queen(position=(3, 7), color="white", is_in_start_position=True),
)
INITIAL_KINGS = (
    King(position=(4, 0), color="black", is_in_start_position=True),
    King(position=(4, 7), color="white", is_in_start_position=True),
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


def create_piece_instance_from_string(
    position: tuple[int, int], string: str
) -> Optional[Piece]:
    """Convert a string to an instance of the Piece classes."""
    if string == "oo":
        return None
    color, class_identifier = string[0], string[1]
    color = "black" if color == "b" else "white"
    is_in_start_position = _get_is_in_start_position(
        position=position, class_identifier=class_identifier, color=color
    )
    if class_identifier == "p":
        return Pawn(position, color, is_in_start_position=is_in_start_position)
    if class_identifier == "r":
        return Rook(position, color, is_in_start_position=is_in_start_position)
    if class_identifier == "b":
        return Bishop(position, color, is_in_start_position=is_in_start_position)
    if class_identifier == "k":
        return King(position, color, is_in_start_position=is_in_start_position)
    if class_identifier == "n":
        return Knight(position, color, is_in_start_position=is_in_start_position)
    if class_identifier == "q":
        return Queen(position, color, is_in_start_position=is_in_start_position)
    raise Exception("Invalid string could not be converted to a Piece instance.")


def _get_is_in_start_position(
    position: tuple[int, int], class_identifier: str, color: str
) -> bool:
    if class_identifier == "p":
        return position in tuple(
            piece.position
            for piece in INITIAL_BLACK_PAWNS + INITIAL_WHITE_PAWNS
            if piece.color == color
        )
    if class_identifier == "r":
        return position in tuple(
            piece.position for piece in INITIAL_ROOKS if piece.color == color
        )
    if class_identifier == "n":
        return position in tuple(
            piece.position for piece in INITIAL_KNIGHTS if piece.color == color
        )
    if class_identifier == "b":
        return position in tuple(
            piece.position for piece in INITIAL_BISHOPS if piece.color == color
        )
    if class_identifier == "q":
        return position in tuple(
            piece.position for piece in INITIAL_QUEENS if piece.color == color
        )
    if class_identifier == "k":
        return position in tuple(
            piece.position for piece in INITIAL_KINGS if piece.color == color
        )
    raise Exception(
        f"Could not determine whether piece '{class_identifier}' of color "
        f"{color} in position {position} is in starting position."
    )
