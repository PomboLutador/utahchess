from __future__ import annotations

from typing import Generator, Optional

from utahchess.board import Board, is_occupied
from utahchess.move import LONG_CASTLING, SHORT_CASTLING, Move
from utahchess.move_validation import find_current_players_king_position, is_check
from utahchess.tile_movement_utils import (
    apply_movement_vector,
    apply_movement_vector_n_times,
    is_in_bounds,
)


def get_castling_moves(
    board: Board, current_player: str
) -> Generator[Move, None, None]:
    """Get all castling moves for the current player."""
    king_position = find_current_players_king_position(
        board=board, current_player=current_player
    )
    king = board[king_position]
    if king is None:
        raise Exception(
            f"Piece at position {king_position} is None when it should be a King."
        )
    if not king.is_in_start_position:
        return

    if is_check(board=board, current_player=current_player):
        return  # Cant castle out of check

    for movement_vector in [(1, 0), (-1, 0)]:
        rook_tile = _find_rook_for_castling(
            board=board,
            current_player=current_player,
            movement_vector=movement_vector,
        )
        if rook_tile is None:
            continue

        castling_move = _get_castling_move(
            board=board,
            movement_vector=movement_vector,
            king_position=king_position,
            rook_position=rook_tile,
        )

        if is_check(
            board=board.move_piece(
                from_position=get_king_move(move=castling_move)[0],
                to_position=get_king_move(move=castling_move)[1],
            ),
            current_player=current_player,
        ):
            break
        yield castling_move


def get_rook_move(move: Move) -> tuple[tuple[int, int], tuple[int, int]]:
    return move.piece_moves[1]


def get_king_move(move: Move) -> tuple[tuple[int, int], tuple[int, int]]:
    return move.piece_moves[0]


def _get_castling_type(movement_vector: tuple[int, int]) -> str:
    return SHORT_CASTLING if movement_vector[0] == 1 else LONG_CASTLING


def _get_castling_move(
    board: Board,
    movement_vector: tuple[int, int],
    king_position: tuple[int, int],
    rook_position: tuple[int, int],
) -> Move:
    """Gather description of castling move."""
    castling_type = _get_castling_type(movement_vector=movement_vector)
    if castling_type == SHORT_CASTLING:
        king_destination_tile = apply_movement_vector(
            position=rook_position, movement_vector=(-movement_vector[0], 0)
        )
    elif castling_type == LONG_CASTLING:
        king_destination_tile = apply_movement_vector_n_times(
            position=rook_position,
            movement_vector=(-movement_vector[0], 0),
            n=2,
        )

    rook_destination_tile = apply_movement_vector(
        position=king_position, movement_vector=movement_vector
    )

    rook_move, king_move = (rook_position, rook_destination_tile), (
        king_position,
        king_destination_tile,
    )
    king, rook = board[king_position], board[rook_position]
    castling_move = Move(
        type=castling_type,
        piece_moves=(king_move, rook_move),
        moving_pieces=(king, rook),  # type: ignore
        is_capturing_move=False,
        allows_en_passant=False,
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
    if not is_in_bounds(position=next_tile):
        return None
    while True:
        next_piece = board[next_tile]
        if not is_occupied(board=board, position=next_tile):
            if is_check(
                board=board.move_piece(
                    from_position=king_position, to_position=next_tile
                ),
                current_player=current_player,
            ):
                return None  # Cant castle through check
        elif (  # If next tile is occupied, it has to be a friendly rook
            next_piece.piece_type == "Rook"  # type: ignore
            and next_piece.color == current_player  # type: ignore
            and next_piece.is_in_start_position  # type: ignore
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
