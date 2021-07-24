from __future__ import annotations

from dataclasses import dataclass
from typing import Generator, Optional

from utahchess.board import Board, is_occupied
from utahchess.move import Move
from utahchess.move_validation import is_check
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
            potential_move = EnPassantMove(
                piece_moves=((initial_tile, destination_tile),),
                moving_pieces=(board[initial_tile],),
            )
            if _is_valid_en_passant_move(board=board, en_passant_move=potential_move):
                yield potential_move


def _complete_en_passant_move(board: Board, en_passant_move: EnPassantMove) -> Board:
    """Completes the capturing part of an en passant move."""
    piece_move = en_passant_move.piece_moves[0]
    movement_direction = piece_move[1][1] - piece_move[0][1]
    tile_to_delete = apply_movement_vector(
        position=piece_move[1], movement_vector=(0, -movement_direction)
    )
    return board.delete_piece(position=tile_to_delete)


def make_en_passant_move(board: Board, en_passant_move: EnPassantMove) -> Board:
    piece_move = en_passant_move.piece_moves[0]
    board = board.move_piece(from_position=piece_move[0], to_position=piece_move[1])
    board = _complete_en_passant_move(board=board, en_passant_move=en_passant_move)
    return board


def _is_valid_en_passant_move(board: Board, en_passant_move: EnPassantMove) -> bool:
    current_player = en_passant_move.moving_pieces[0].color
    board_after_move = make_en_passant_move(
        board=board, en_passant_move=en_passant_move
    )
    return not is_check(board=board_after_move, current_player=current_player)
