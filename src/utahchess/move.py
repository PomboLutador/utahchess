from __future__ import annotations

from dataclasses import dataclass

from utahchess.board import Board
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


def make_move(board: Board, move: Move) -> Board:
    """Make a move on a given board.

    Args:
        board: Board on which to make the move.
        move: Move to make.

    Returns: A copy of the board after the move was made.
    """
    for piece_move in move.piece_moves:
        board = board.move_piece(from_position=piece_move[0], to_position=piece_move[1])
    for piece_to_delete in move.pieces_to_delete:
        board = board.delete_piece(position=piece_to_delete)
    return board
