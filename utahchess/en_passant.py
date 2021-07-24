from __future__ import annotations

from dataclasses import dataclass
from typing import Generator, Optional

from utahchess.board import Board, is_occupied
from utahchess.move import Move
from utahchess.move_validation import RegularMove
from utahchess.piece import Piece
from utahchess.tile_movement_utils import apply_movement_vector, is_in_bounds


@dataclass
class EnPassantMove(Move):
    type = "En Passant Move"
    piece_moves: tuple[tuple[tuple[int, int], tuple[int, int]]]
    moving_pieces: tuple[Piece, ...]
    is_capturing_move = True
    allows_en_passant = False

    def __init__(
        self,
        piece_moves: tuple[tuple[tuple[int, int], tuple[int, int]]],
        moving_pieces: tuple[Piece],
    ) -> None:
        self.piece_moves = piece_moves
        self.moving_pieces = moving_pieces

    def get_position_of_piece_to_remove(self) -> tuple[int, int]:
        pass


def get_en_passant_moves(
    board: Board, last_move: Optional[Move]
) -> Generator[EnPassantMove, None, None]:
    """Returns all legal En Passant moves for current player."""
    if last_move is None:
        return None

    current_player = "white" if last_move.moving_pieces[0].color == "black" else "black"
    move_direction = 1 if current_player == "black" else -1
    if not last_move.allows_en_passant:
        return None

    for x_offset in [1, -1]:

        initial_tile = apply_movement_vector(
            position=last_move.piece_moves[0][1], movement_vector=(x_offset, 0)
        )
        destination_tile = apply_movement_vector(
            position=last_move.piece_moves[0][1], movement_vector=(0, move_direction)
        )

        if not is_in_bounds(position=initial_tile) or not is_in_bounds(
            destination_tile
        ):
            continue

        if not is_occupied(board=board, position=initial_tile):
            continue

        if (
            board[initial_tile].piece_type == "Pawn"
            and board[last_move.piece_moves[0][1]].color != board[initial_tile].color
        ):
            yield EnPassantMove(
                piece_moves=((initial_tile, destination_tile),),
                moving_pieces=(board[initial_tile],),
            )


def complete_en_passant_move(board: Board, en_passant_move: EnPassantMove) -> Board:
    """Completes the capturing part of an en passant move."""
    pass


def _get_piece_move_for_en_passant(
    board: Board, last_move: Optional[Move]
) -> tuple[tuple[int, int], tuple[int, int]]:
    pass
