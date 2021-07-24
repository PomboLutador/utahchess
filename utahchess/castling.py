from __future__ import annotations

from dataclasses import dataclass
from typing import Generator, Optional

from utahchess.board import Board, is_edible, is_occupied
from utahchess.move import Move
from utahchess.move_validation import find_current_players_king_position, is_check
from utahchess.piece import Piece
from utahchess.tile_movement_utils import (
    apply_movement_vector,
    apply_movement_vector_n_times,
    is_in_bounds,
)

SHORT_CASTLING = "Short Castling"
LONG_CASTLING = "Long Castling"


@dataclass
class CastlingMove(Move):
    type = "Castling Move"
    piece_moves: tuple[tuple[tuple[int, int], tuple[int, int]], ...]
    moving_pieces: tuple[Piece, ...]
    is_capturing_move = False
    castling_type: str
    allows_en_passant = False

    def __init__(
        self,
        piece_moves: tuple[
            tuple[tuple[int, int], tuple[int, int]],
            tuple[tuple[int, int], tuple[int, int]],
        ],
        moving_pieces: tuple[Piece, Piece],
        castling_type: str,
    ) -> None:
        self.piece_moves = piece_moves
        self.moving_pieces = moving_pieces
        self.castling_type = castling_type

    def get_rook_move(self) -> tuple[tuple[int, int], tuple[int, int]]:
        return self.piece_moves[0]

    def get_king_move(self) -> tuple[tuple[int, int], tuple[int, int]]:
        return self.piece_moves[1]


def get_castling_moves(
    board: Board, current_player: str
) -> Generator[CastlingMove, None, None]:
    """Get all castling moves for the current player."""
    king_position = find_current_players_king_position(
        board=board, current_player=current_player
    )

    if not board[king_position].is_in_start_position:
        return

    # Cant castle out of check
    if is_check(board=board, current_player=current_player):
        return

    for movement_vector in [(1, 0), (-1, 0)]:
        rook_tile = _find_rook_for_castling(
            board=board, current_player=current_player, movement_vector=movement_vector
        )
        if rook_tile is None:
            continue

        castling_move = _make_castling_move(
            board=board,
            movement_vector=movement_vector,
            king_position=king_position,
            rook_position=rook_tile,
        )

        if is_check(
            board=board.move_piece(
                from_position=castling_move.get_king_move()[0],
                to_position=castling_move.get_king_move()[1],
            ),
            current_player=current_player,
        ):
            break
        yield castling_move


def _get_castling_type(movement_vector: tuple[int, int]) -> str:
    return SHORT_CASTLING if movement_vector[0] == 1 else LONG_CASTLING


def _make_castling_move(
    board: Board,
    movement_vector: tuple[int, int],
    king_position: tuple[int, int],
    rook_position: tuple[int, int],
) -> CastlingMove:
    """Gather description of castling move."""
    castling_type = _get_castling_type(movement_vector=movement_vector)
    if castling_type == SHORT_CASTLING:
        king_destination_tile = apply_movement_vector(
            position=rook_position, movement_vector=(-movement_vector[0], 0)
        )
    elif castling_type == LONG_CASTLING:
        king_destination_tile = apply_movement_vector_n_times(
            position=rook_position, movement_vector=(-movement_vector[0], 0), n=2
        )

    rook_destination_tile = apply_movement_vector(
        position=king_position, movement_vector=movement_vector
    )

    rook_move = (rook_position, rook_destination_tile)
    king_move = (king_position, king_destination_tile)
    castling_move = CastlingMove(
        piece_moves=(rook_move, king_move),
        moving_pieces=(board[rook_position], board[king_position]),
        castling_type=castling_type,
    )

    return castling_move


def _find_rook_for_castling(
    board: Board, current_player: str, movement_vector: tuple[int, int]
) -> Optional[tuple[int, int]]:
    """Find rook in direction of movement vector starting from friendly King."""
    king_position = find_current_players_king_position(
        board=board, current_player=current_player
    )
    next_tile = apply_movement_vector(
        position=king_position, movement_vector=movement_vector
    )
    while True:
        if not is_occupied(board=board, position=next_tile):
            if is_check(
                board=board.move_piece(
                    from_position=king_position, to_position=next_tile
                ),
                current_player=current_player,
            ):
                return None  # Cant castle through check
        elif (
            board[next_tile].piece_type == "Rook"
            and board[next_tile].color == current_player
            and board[next_tile].is_in_start_position
        ):
            pass
        else:  # If the path to the rook is obstructed
            return None

        if is_in_bounds(position=next_tile) and is_occupied(
            board=board, position=next_tile
        ):
            return next_tile

        next_tile = apply_movement_vector(
            position=next_tile, movement_vector=movement_vector
        )
        if not is_in_bounds(position=next_tile):
            break
    return None
