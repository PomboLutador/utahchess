from __future__ import annotations

from itertools import chain
from typing import Generator

from utahchess.board import Board
from utahchess.castling import CastlingMove, get_castling_moves
from utahchess.en_passant import EnPassantMove, get_en_passant_moves
from utahchess.move import Move
from utahchess.move_validation import RegularMove, get_legal_regular_moves


def get_all_legal_moves(
    board: Board, current_player: str, last_move: Move
) -> Generator[Move, None, None]:
    regular_moves = get_legal_regular_moves(board=board, current_player=current_player)
    en_passant_moves = get_en_passant_moves(board=board, last_move=last_move)
    castling_moves = get_castling_moves(board=board, current_player=current_player)
    return chain(regular_moves, en_passant_moves, castling_moves)  # type: ignore
