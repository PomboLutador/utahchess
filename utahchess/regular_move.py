from __future__ import annotations

from typing import Generator

from utahchess.board import Board
from utahchess.move import REGULAR_MOVE, Move
from utahchess.move_candidates import get_all_move_candidates
from utahchess.move_validation import is_valid_move
from utahchess.piece import Piece


def get_regular_moves(board: Board, current_player: str) -> Generator[Move, None, None]:
    """Get all regular moves for the current player on the given board.

    A regular move is any move that is neither a castling- nor an en passant move.

    Args:
        board: Board on which to get regular moves.
        current_player: Player for which to get regular moves.

    Returns: All possible regular moves on the given board for current player.
    """
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
            allows_en_passant=_get_allows_en_passant_flag(
                piece_moves=(move_candidate,), moving_pieces=(from_piece,)
            ),
        )
        if is_valid_move(board=board, move=potential_move):
            yield potential_move


def _get_allows_en_passant_flag(
    moving_pieces: tuple[Piece],
    piece_moves: tuple[tuple[tuple[int, int], tuple[int, int]]],
) -> bool:
    """Get whether a move possibly allows an enemy en passant move on their next turn.

    Returns: True if the moving piece is a pawn and it moves by more than one tile and
        False otherwise.
    """
    return (
        moving_pieces[0].piece_type == "Pawn"
        and abs(_get_distance_moved_in_y_direction(piece_moves[0])) == 2
    )


def _get_distance_moved_in_y_direction(
    piece_move: tuple[tuple[int, int], tuple[int, int]]
) -> int:
    return piece_move[1][1] - piece_move[0][1]
