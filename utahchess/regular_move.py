from __future__ import annotations

from typing import Generator

from utahchess.board import Board
from utahchess.move import REGULAR_MOVE, Move
from utahchess.move_candidates import get_all_move_candidates
from utahchess.move_validation import is_valid_move
from utahchess.piece import Piece


def get_regular_moves(board: Board, current_player: str) -> Generator[Move, None, None]:
    for move_candidate in get_all_move_candidates(
        board=board, current_player=current_player
    ):
        from_position, to_position = move_candidate
        from_piece = board[from_position]
        if from_piece is None:
            raise Exception(f"Piece at {from_position} unexpectedly None.")
        potential_move = Move(
            type=REGULAR_MOVE,
            piece_moves=(move_candidate,),
            moving_pieces=(from_piece,),
            is_capturing_move=False if board[to_position] is None else True,
            allows_en_passant=_set_allows_en_passant_flag(
                piece_moves=(move_candidate,), moving_pieces=(from_piece,)
            ),
        )
        if is_valid_move(board=board, move=potential_move):
            yield potential_move


def _set_allows_en_passant_flag(
    moving_pieces: tuple[Piece],
    piece_moves: tuple[tuple[tuple[int, int], tuple[int, int]]],
) -> bool:
    return (
        moving_pieces[0].piece_type == "Pawn"
        and abs(_get_distance_moved_in_y_direction(piece_moves[0])) == 2
    )


def _get_distance_moved_in_y_direction(
    piece_move: tuple[tuple[int, int], tuple[int, int]]
) -> int:
    return piece_move[1][1] - piece_move[0][1]
