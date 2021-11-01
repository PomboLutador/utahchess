from __future__ import annotations

from dataclasses import dataclass
from typing import Generator, Optional

from utahchess.board import Board, is_occupied
from utahchess.move import Move
from utahchess.move_validation import is_check
from utahchess.piece import Piece
from utahchess.tile_movement_utils import apply_movement_vector, is_in_bounds

EN_PASSANT_MOVE = "En Passant Move"


@dataclass(frozen=True)
class EnPassantMove(Move):
    type = EN_PASSANT_MOVE
    piece_moves: tuple[tuple[tuple[int, int], tuple[int, int]]]
    moving_pieces: tuple[Piece]
    is_capturing_move = True
    allows_en_passant = False


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

        opponent_piece = board[last_move.piece_moves[0][1]]
        if opponent_piece is None:
            raise Exception(
                f"Piece at position {last_move.piece_moves[0][1]} is None when it should be a Pawn."
            )

        from_piece = board[initial_tile]
        if from_piece is None:
            continue

        if from_piece.piece_type == "Pawn" and opponent_piece.color != from_piece.color:
            potential_move = EnPassantMove(
                piece_moves=((initial_tile, destination_tile),),
                moving_pieces=(from_piece,),
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


def make_en_passant_move(board: Board, move: EnPassantMove) -> Board:
    piece_move = move.piece_moves[0]
    board = board.move_piece(from_position=piece_move[0], to_position=piece_move[1])
    board = _complete_en_passant_move(board=board, en_passant_move=move)
    return board


def _is_valid_en_passant_move(board: Board, en_passant_move: EnPassantMove) -> bool:
    current_player = en_passant_move.moving_pieces[0].color
    board_after_move = make_en_passant_move(board=board, move=en_passant_move)
    return not is_check(board=board_after_move, current_player=current_player)
