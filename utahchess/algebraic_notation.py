from __future__ import annotations

from utahchess.board import Board
from utahchess.move import (
    EN_PASSANT_MOVE,
    LONG_CASTLING,
    SHORT_CASTLING,
    Move,
    make_move,
)
from utahchess.move_validation import is_check, is_checkmate
from utahchess.utils import x_index_to_file, y_index_to_rank


def get_algebraic_identifer(move: Move, board: Board, **kwargs):
    if move.type in (LONG_CASTLING, SHORT_CASTLING):
        return _get_castling_identifer(move=move)
    check_or_checkmate_identifer = _get_check_or_checkmate_identifier(
        board=board,
        move=move,
        current_player=move.moving_pieces[0].color,
    )
    try:
        rank = kwargs["rank"]
    except KeyError:
        rank = ""
    try:
        file = kwargs["file"]
    except KeyError:
        file = ""

    return (
        f"{_get_moving_piece_signifier(move=move)}{rank}{file}"
        f"{_get_capturing_flag(move=move)}{_get_destination_tile(move=move)}"
        f"{_get_en_passant_identifier(move=move)}{check_or_checkmate_identifer}"
    )


def _get_moving_piece_signifier(move: Move) -> str:
    piece = move.moving_pieces[0]
    if piece.piece_type == "Pawn":
        return ""
    elif piece.piece_type == "King":
        return "K"
    elif piece.piece_type == "Bishop":
        return "B"
    elif piece.piece_type == "Queen":
        return "Q"
    elif piece.piece_type == "Knight":
        return "N"
    elif piece.piece_type == "Rook":
        return "R"
    raise Exception(f"Unrecognized piece type: {piece.piece_type}")


def _get_destination_tile(move: Move) -> str:
    x, y = move.piece_moves[0][1]
    return f"{x_index_to_file(x=x)}{y_index_to_rank(y=y)}"


def _get_capturing_flag(move: Move) -> str:
    return "x" if move.is_capturing_move else ""


def _get_castling_identifer(move: Move) -> str:
    if move.type == SHORT_CASTLING:
        return "O-O"
    elif move.type == LONG_CASTLING:
        return "O-O-O"
    else:
        return ""


def _get_en_passant_identifier(move: Move) -> str:
    if move.type == EN_PASSANT_MOVE:
        return " e.p."
    return ""


def _get_check_or_checkmate_identifier(
    board: Board, move: Move, current_player: str
) -> str:

    if is_checkmate(
        board=make_move(board=board, move=move),
        current_player=_get_opposite_player(current_player=current_player),
    ):
        return "#"
    elif is_check(
        board=make_move(board=board, move=move),
        current_player=_get_opposite_player(current_player=current_player),
    ):
        return "+"
    else:
        return ""


def _get_opposite_player(current_player: str) -> str:
    return "black" if current_player == "white" else "white"
