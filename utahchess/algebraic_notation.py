from __future__ import annotations

from utahchess.board import Board
from utahchess.move import EN_PASSANT_MOVE, LONG_CASTLING, SHORT_CASTLING, Move
from utahchess.utils import x_index_to_file, y_index_to_rank


def get_algebraic_identifer(move: Move, board: Board, **kwargs):
    """Get the algebraic identifier of a move given a board.

    For more information on algebraic notation of moves, see here:
    https://en.wikipedia.org/wiki/Algebraic_notation_(chess)

    For two moves on the same board the algebraic identifier can be ambiguous, meaning
    two moves can have the same identifier, if rank and file of the moving piece are
    not considered. Rank and file paramters as well as a check or checkmate flag can
    be passed via **kwargs.

    This function does thus not disambiguate a move's identifer. See
    "utahchess.legal_moves.get_move_per_algebraic_identifier" for that.

    Args:
        move: Move for which to get the algebraic identifier for.
        board: Board on which move is executed.
        **kwargs: Specifically for rank and file disambiguation and to pass check or
            checkmate flag.

    Returns: A possibly ambiguous string describing the move in algebraic notation.
    """
    if move.type in (LONG_CASTLING, SHORT_CASTLING):
        return _get_castling_identifer(move=move)

    try:
        check_or_checkmate_identifer = kwargs["check_or_checkmate"]
    except KeyError:
        check_or_checkmate_identifer = ""

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
