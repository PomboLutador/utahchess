from __future__ import annotations

from typing import Generator, Optional

from utahchess.board import Board
from utahchess.move import EN_PASSANT_MOVE, Move
from utahchess.move_validation import is_valid_move
from utahchess.tile_movement_utils import apply_movement_vector, is_in_bounds


def get_en_passant_moves(
    board: Board, last_move: Optional[Move]
) -> Generator[Move, None, None]:
    """Get all legal En Passant moves for current player.

    En passant moves are only possibly legal if the last move was a pawn moving two
    tiles from starting position. Current player can be inferred from the last move
    and thus does not have to be provided to this function.

    Args:
        board: Board on which to get en passant moves.
        last_move: Last move that was executed on the board. Has to be an enemy move.
            Can possibly be None if it's the first turn of the game.

    Returns: All possible en passant moves on the given board for current player.
    """
    if last_move is None:
        return None

    current_player = "white" if last_move.moving_pieces[0].color == "black" else "black"
    move_direction = 1 if current_player == "black" else -1
    if not last_move.allows_en_passant:
        return None

    for x_offset in [1, -1]:

        initial_tile = apply_movement_vector(
            # Initial tile for the potential en passant move's moving piece
            position=last_move.piece_moves[0][1],
            movement_vector=(x_offset, 0),
        )
        destination_tile = apply_movement_vector(
            position=last_move.piece_moves[0][1],
            movement_vector=(0, move_direction),
        )

        if not is_in_bounds(position=initial_tile) or not is_in_bounds(
            destination_tile
        ):
            continue

        opponent_piece = board[last_move.piece_moves[0][1]]

        if opponent_piece is None:
            raise Exception(
                (
                    f"Piece at position "
                    f"{last_move.piece_moves[0][1]} is None when it should be a Pawn."
                )
            )

        from_piece = board[initial_tile]
        if from_piece is None:  # No pawn in place to take advantage of last move's pawn
            continue

        if from_piece.piece_type == "Pawn" and opponent_piece.color != from_piece.color:
            potential_move = Move(
                type=EN_PASSANT_MOVE,
                piece_moves=((initial_tile, destination_tile),),
                moving_pieces=(from_piece,),
                pieces_to_delete=(
                    _get_piece_to_delete(piece_move=(initial_tile, destination_tile))
                ),
                is_capturing_move=True,
                allows_en_passant=False,
            )
            if is_valid_move(board=board, move=potential_move):
                yield potential_move


def _get_piece_to_delete(
    piece_move: tuple[tuple[int, int], tuple[int, int]]
) -> tuple[tuple[int, int], ...]:
    movement_direction = piece_move[1][1] - piece_move[0][1]
    return (
        apply_movement_vector(
            position=piece_move[1], movement_vector=(0, -movement_direction)
        ),
    )
