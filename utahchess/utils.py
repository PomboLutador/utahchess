import string
from typing import Optional

from utahchess.piece import Piece

FILE_POSSIBILITIES = "abcdefgh"
RANK_POSSIBILITIES = "87654321"


def x_index_to_file(x: int) -> str:
    """Get file corresponding to an x index."""
    return FILE_POSSIBILITIES[x]


def y_index_to_rank(y: int) -> str:
    """Get rank corresponding to a y index."""
    return RANK_POSSIBILITIES[y]


def rank_to_y_index(rank: str) -> int:
    """Get y index correpsonding to a rank."""
    return 8 - int(rank)


def file_to_x_index(file: str) -> int:
    """Get x index correpsonding to a file."""
    return string.ascii_lowercase.index(file)


def get_unicode_character(piece: Optional[Piece]) -> str:
    """Get unicode character representing a piece."""
    if piece is None:
        return "|       | "
    elif piece.piece_type == "Pawn":
        if piece.color == "black":
            return f"|   \u265F   | "
        if piece.color == "white":
            return f"|   \u2659   | "
    elif piece.piece_type == "Knight":
        if piece.color == "black":
            return f"|   \u265E   | "
        if piece.color == "white":
            return f"|   \u2658   | "
    elif piece.piece_type == "Rook":
        if piece.color == "black":
            return f"|   \u265C   | "
        if piece.color == "white":
            return f"|   \u2656   | "
    elif piece.piece_type == "Bishop":
        if piece.color == "black":
            return f"|   \u265D   | "
        if piece.color == "white":
            return f"|   \u2657   | "
    elif piece.piece_type == "Queen":
        if piece.color == "black":
            return f"|   \u265B   | "
        if piece.color == "white":
            return f"|   \u2655   | "
    elif piece.piece_type == "King":
        if piece.color == "black":
            return f"|   \u265A   | "
        if piece.color == "white":
            return f"|   \u2654   | "
    raise Exception(f"Could not determine piece {piece}")
