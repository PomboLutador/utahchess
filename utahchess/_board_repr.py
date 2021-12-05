from __future__ import annotations

from utahchess.piece import Optional, Piece
from utahchess.utils import x_index_to_file, y_index_to_rank


def representation(_board: tuple[tuple[Optional[Piece], ...], ...]):
    representation = ""
    row = "          "
    for i in range(8):
        row += f"     {x_index_to_file(i)}    "
    representation += row + "\n"
    for y_coord in range(8):
        row = "  "
        row += "--------  " * 9 + "\n"
        for x_coord in range(9):
            if x_coord == 0:
                row += f"    {y_index_to_rank(y_coord)}    | "
                continue
            else:
                x_coord -= 1
            piece = _board[x_coord][y_coord]
            if piece is None:
                row += "|       | "
                continue
            if piece.piece_type == "Pawn":
                if piece.color == "black":
                    row += f"|   \u265F   | "
                if piece.color == "white":
                    row += f"|   \u2659   | "
            if piece.piece_type == "Knight":
                if piece.color == "black":
                    row += f"|   \u265E   | "
                if piece.color == "white":
                    row += f"|   \u2658   | "
            if piece.piece_type == "Rook":
                if piece.color == "black":
                    row += f"|   \u265C   | "
                if piece.color == "white":
                    row += f"|   \u2656   | "
            if piece.piece_type == "Bishop":
                if piece.color == "black":
                    row += f"|   \u265D   | "
                if piece.color == "white":
                    row += f"|   \u2657   | "
            if piece.piece_type == "Queen":
                if piece.color == "black":
                    row += f"|   \u265B   | "
                if piece.color == "white":
                    row += f"|   \u2655   | "

            if piece.piece_type == "King":
                if piece.color == "black":
                    row += f"|   \u265A   | "
                if piece.color == "white":
                    row += f"|   \u2654   | "

        representation += row + "\n"
    representation + "  " + "--------  " * 9
    return representation
