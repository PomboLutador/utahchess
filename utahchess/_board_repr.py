from __future__ import annotations

from utahchess.piece import Piece


def representation(_board: tuple[tuple[Piece, ...], ...]):
    representation = ""
    row = "          "
    for i in range(8):
        row += f"     {i}    "
    representation += row + "\n"
    for y_coord in range(8):
        row = "  "
        row += "--------  " * 9 + "\n"
        for x_coord in range(9):
            if x_coord == 0:
                row += f"    {y_coord}    | "
                continue
            else:
                x_coord -= 1
            if _board[x_coord][y_coord] is None:
                row += "|       | "
                continue
            if _board[x_coord][y_coord].piece_type == "Pawn":
                if _board[x_coord][y_coord].color == "black":
                    row += f"|   \u265F   | "
                if _board[x_coord][y_coord].color == "white":
                    row += f"|   \u2659   | "
            if _board[x_coord][y_coord].piece_type == "Knight":
                if _board[x_coord][y_coord].color == "black":
                    row += f"|   \u265E   | "
                if _board[x_coord][y_coord].color == "white":
                    row += f"|   \u2658   | "
            if _board[x_coord][y_coord].piece_type == "Rook":
                if _board[x_coord][y_coord].color == "black":
                    row += f"|   \u265C   | "
                if _board[x_coord][y_coord].color == "white":
                    row += f"|   \u2656   | "
            if _board[x_coord][y_coord].piece_type == "Bishop":
                if _board[x_coord][y_coord].color == "black":
                    row += f"|   \u265D   | "
                if _board[x_coord][y_coord].color == "white":
                    row += f"|   \u2657   | "
            if _board[x_coord][y_coord].piece_type == "Queen":
                if _board[x_coord][y_coord].color == "black":
                    row += f"|   \u265B   | "
                if _board[x_coord][y_coord].color == "white":
                    row += f"|   \u2655   | "

            if _board[x_coord][y_coord].piece_type == "King":
                if _board[x_coord][y_coord].color == "black":
                    row += f"|   \u265A   | "
                if _board[x_coord][y_coord].color == "white":
                    row += f"|   \u2654   | "

        representation += row + "\n"
    representation + "  " + "--------  " * 9
    return representation
