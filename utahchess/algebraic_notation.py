from __future__ import annotations

from dataclasses import dataclass

from utahchess.board import Board
from utahchess.move import Move, make_move
from utahchess.move_validation import is_check, is_checkmate
from utahchess.utils import (
    file_to_x_index,
    rank_to_y_index,
    x_index_to_file,
    y_index_to_rank,
)

# def _get_moving_piece_signifier(move: Move) -> str:
#     piece = move.moving_pieces[0]
#     if piece.piece_type == "Pawn":
#         return ""
#     elif piece.piece_type == "King":
#         return "K"
#     elif piece.piece_type == "Bishop":
#         return "B"
#     elif piece.piece_type == "Queen":
#         return "Q"
#     elif piece.piece_type == "Knight":
#         return "N"
#     elif piece.piece_type == "Rook":
#         return "R"
#     raise Exception(f"Unrecognized piece type: {piece.piece_type}")


# def _get_destination_tile(move: Move) -> str:
#     x, y = move.piece_moves[0][1]
#     return f"{x_index_to_file(x=x)}{y_index_to_rank(y=y)}"


# def _get_capturing_flag(move: Move) -> str:
#     return "x" if move.is_capturing_move else ""


# def _get_castling_identifer(move: Move) -> str:
#     if move.type == SHORT_CASTLING:
#         return "O-O"
#     elif move.type == LONG_CASTLING:
#         return "O-O-O"
#     else:
#         return ""


# def _get_en_passant_identifier(move: Move) -> str:
#     if move.type == EN_PASSANT_MOVE:
#         return " e.p."
#     return ""


# def _get_moving_piece_file(move: Move) -> str:
#     x_from, y_from = move.piece_moves[0][0]
#     return x_index_to_file(x=x_from)


# def _get_moving_piece_rank(move: Move) -> str:
#     x_from, y_from = move.piece_moves[0][0]
#     return y_index_to_rank(y=y_from)


# def _get_check_or_checkmate_identifier(
#     board: Board, move: Move, current_player: str
# ) -> str:

#     if is_checkmate(
#         board=make_move(board=board, move=move),
#         current_player=_get_opposite_player(current_player=current_player),
#     ):
#         return "#"
#     elif is_check(
#         board=make_move(board=board, move=move),
#         current_player=_get_opposite_player(current_player=current_player),
#     ):
#         return "+"
#     else:
#         return ""


# def _get_opposite_player(current_player: str) -> str:
#     return "black" if current_player == "white" else "white"


@dataclass(frozen=True)
class AlgebraicNotation:
    castling_identifier: str
    en_passant_identifer: str
    piece: str
    destination_tile: str
    capturing_flag: str
    check_or_checkmate_flag: str

    def to_string(self) -> str:
        if self.castling_identifier:
            return self.castling_identifier
        return (
            f"{self.piece}{self.capturing_flag}{self.destination_tile}"
            f"{self.en_passant_identifer}{self.check_or_checkmate_flag}"
        )

    def __repr__(self) -> str:
        return self.to_string()

    def to_string_with_file(self, file: str) -> str:
        return (
            f"{self.piece}{file}{self.capturing_flag}{self.destination_tile}"
            f"{self.en_passant_identifer}{self.check_or_checkmate_flag}"
        )

    def to_string_with_rank(self, rank: str) -> str:
        return (
            f"{self.piece}{rank}{self.capturing_flag}{self.destination_tile}"
            f"{self.en_passant_identifer}{self.check_or_checkmate_flag}"
        )
