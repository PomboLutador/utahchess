from __future__ import annotations

from itertools import chain
from typing import Callable, Generator

from utahchess.board import Board, is_edible, is_occupied
from utahchess.piece import Piece
from utahchess.tile_movement_utils import apply_movement_vector, is_in_bounds

KNIGHT_MOVEMENT_VECTORS = (
    (1, 2),
    (-1, 2),
    (-1, -2),
    (1, -2),
    (2, 1),
    (-2, 1),
    (2, -1),
    (-2, -1),
)

KING_MOVEMENT_VECTORS = (
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
    (1, 1),
    (-1, -1),
    (1, -1),
    (-1, 1),
)


def get_all_move_candidates(
    board: Board,
    current_player: str,
) -> Generator[tuple[tuple[int, int], tuple[int, int]], None, None]:
    """Get all move candidates for the current player on the given board.

    A move candidate is a tuple of an initial- and a destination tile.

    Args:
        board: Board on which to get all move candidates.
        current_player: Player for which to get move candidates.

    Returns: All move candidates for the current player.
    """
    return chain(
        *tuple(
            _get_move_candidate_function(piece=piece)(
                board=board, position=piece.position
            )
            for piece in board.all_pieces()
            if piece.color == current_player
        )
    )  # type: ignore


def get_pawn_move_candidates(
    board: Board, position: tuple[int, int]
) -> Generator[tuple[tuple[int, int], tuple[int, int]], None, None]:
    """Get all move candidates for a specific pawn."""
    pawn = board[position]
    if pawn is None:
        raise Exception(
            f"Piece at position {position} is None when it should be a Pawn."
        )
    movement_direction = -1 if pawn.color == "white" else 1
    movement_vector = (0, movement_direction)

    tile_in_front = apply_movement_vector(
        position=pawn.position, movement_vector=movement_vector
    )
    if not is_in_bounds(position=tile_in_front):
        return

    if not is_occupied(board=board, position=tile_in_front):
        yield (pawn.position, tile_in_front)

        if pawn.is_in_start_position:  # check two in front if in front is not occupied
            tile_two_in_front = apply_movement_vector(
                position=tile_in_front, movement_vector=movement_vector
            )
            if not is_occupied(board=board, position=tile_two_in_front):
                yield (pawn.position, tile_two_in_front)

    # Check if there's something to eat in the diagonals
    tiles_to_check = [
        apply_movement_vector(
            position=pawn.position, movement_vector=(1, 1 * movement_direction)
        ),
        apply_movement_vector(
            position=pawn.position,
            movement_vector=(-1, 1 * movement_direction),
        ),
    ]
    for tile_to_check in tiles_to_check:
        if is_in_bounds(position=tile_to_check):
            if is_edible(
                board=board, position=tile_to_check, friendly_color=pawn.color
            ):
                yield (pawn.position, tile_to_check)


def get_knight_move_candidates(
    board: Board, position: tuple[int, int]
) -> Generator[tuple[tuple[int, int], tuple[int, int]], None, None]:
    """Get all move candidates for a specific knight."""
    knight = board[position]
    if knight is None:
        raise Exception(
            f"Piece at position {position} is None when it should be a Knight."
        )
    friendly_color = knight.color
    for movement_vector in KNIGHT_MOVEMENT_VECTORS:

        tile_to_check = apply_movement_vector(
            position=position, movement_vector=movement_vector
        )
        if is_in_bounds(position=tile_to_check):
            if not is_occupied(board=board, position=tile_to_check) or is_edible(
                board=board,
                position=tile_to_check,
                friendly_color=friendly_color,
            ):
                yield (position, tile_to_check)


def get_rook_move_candidates(
    board: Board, position: tuple[int, int]
) -> Generator[tuple[tuple[int, int], tuple[int, int]], None, None]:
    """Get all move candidates for a specific rook."""
    if board[position] is None:
        raise Exception(
            f"Piece at position {position} is None when it should be a Rook."
        )
    return chain(
        _get_horizontal_moves(board=board, initial_position=position),
        _get_vertical_moves(board=board, initial_position=position),
    )  # type: ignore


def get_bishop_move_candidates(
    board: Board, position: tuple[int, int]
) -> Generator[tuple[tuple[int, int], tuple[int, int]], None, None]:
    """Get all move candidates for a specific bishop."""
    if board[position] is None:
        raise Exception(
            f"Piece at position {position} is None when it should be a Bishop."
        )
    return _get_diagonal_moves(board=board, initial_position=position)


def get_queen_move_candidates(
    board: Board, position: tuple[int, int]
) -> Generator[tuple[tuple[int, int], tuple[int, int]], None, None]:
    """Get all move candidates for a specific queen."""
    if board[position] is None:
        raise Exception(
            f"Piece at position {position} is None when it should be a Queen."
        )
    return chain(
        _get_diagonal_moves(board=board, initial_position=position),
        _get_horizontal_moves(board=board, initial_position=position),
        _get_vertical_moves(board=board, initial_position=position),
    )  # type: ignore


def get_king_move_candidates(
    board: Board, position: tuple[int, int]
) -> Generator[tuple[tuple[int, int], tuple[int, int]], None, None]:
    """Get all move candidates for a specific king."""
    king = board[position]
    if king is None:
        raise Exception(
            f"Piece at position {position} is None when it should be a King."
        )
    for movement_vector in KING_MOVEMENT_VECTORS:

        tile_to_check = apply_movement_vector(
            position=position, movement_vector=movement_vector
        )
        if is_in_bounds(position=tile_to_check):
            if not is_occupied(board=board, position=tile_to_check) or is_edible(
                board=board, position=tile_to_check, friendly_color=king.color
            ):
                yield (position, tile_to_check)


def _get_straight_line_moves(
    board: Board,
    initial_position: tuple[int, int],
    movement_vector: tuple[int, int],
) -> Generator[tuple[tuple[int, int], tuple[int, int]], None, None]:
    piece = board[initial_position]
    if piece is None:
        raise Exception(
            f"Piece at position {initial_position} is None when it should not be."
        )
    next_tile = apply_movement_vector(
        position=initial_position, movement_vector=movement_vector
    )

    if not is_in_bounds(position=next_tile):
        return

    while is_edible(
        board=board, position=next_tile, friendly_color=piece.color
    ) or not is_occupied(board=board, position=next_tile):

        yield (piece.position, next_tile)

        if is_edible(board=board, position=next_tile, friendly_color=piece.color):
            break

        next_tile = apply_movement_vector(
            position=next_tile, movement_vector=movement_vector
        )
        if not is_in_bounds(position=next_tile):
            break


def _get_horizontal_moves(
    board: Board, initial_position: tuple[int, int]
) -> Generator[tuple[tuple[int, int], tuple[int, int]], None, None]:
    piece = board[initial_position]
    if piece is None:
        raise Exception(
            f"Piece at position {initial_position} is None when it should not be."
        )
    left_side_moves = _get_straight_line_moves(
        board=board,
        initial_position=initial_position,
        movement_vector=(-1, 0),
    )
    right_side_moves = _get_straight_line_moves(
        board=board,
        initial_position=initial_position,
        movement_vector=(1, 0),
    )
    return chain(left_side_moves, right_side_moves)  # type: ignore


def _get_vertical_moves(
    board: Board, initial_position: tuple[int, int]
) -> Generator[tuple[tuple[int, int], tuple[int, int]], None, None]:
    piece = board[initial_position]
    if piece is None:
        raise Exception(
            f"Piece at position {initial_position} is None when it should not be."
        )
    upwards_moves = _get_straight_line_moves(
        board=board,
        initial_position=initial_position,
        movement_vector=(0, -1),
    )
    downwards_moves = _get_straight_line_moves(
        board=board,
        initial_position=initial_position,
        movement_vector=(0, 1),
    )
    return chain(upwards_moves, downwards_moves)  # type: ignore


def _get_diagonal_moves(
    board: Board, initial_position: tuple[int, int]
) -> Generator[tuple[tuple[int, int], tuple[int, int]], None, None]:
    piece = board[initial_position]
    if piece is None:
        raise Exception(
            f"Piece at position {initial_position} is None when it should not be."
        )
    upper_right_diagonal_moves = _get_straight_line_moves(
        board=board,
        initial_position=initial_position,
        movement_vector=(1, 1),
    )
    upper_left_diagonal_moves = _get_straight_line_moves(
        board=board,
        initial_position=initial_position,
        movement_vector=(-1, 1),
    )
    lower_right_diagonal_moves = _get_straight_line_moves(
        board=board,
        initial_position=initial_position,
        movement_vector=(1, -1),
    )
    lower_left_diagonal_moves = _get_straight_line_moves(
        board=board,
        initial_position=initial_position,
        movement_vector=(-1, -1),
    )

    return chain(
        upper_right_diagonal_moves,
        upper_left_diagonal_moves,
        lower_right_diagonal_moves,
        lower_left_diagonal_moves,
    )  # type: ignore


def _get_move_candidate_function(piece: Piece) -> Callable:
    if piece.piece_type == "Pawn":
        return get_pawn_move_candidates
    elif piece.piece_type == "Knight":
        return get_knight_move_candidates
    elif piece.piece_type == "Bishop":
        return get_bishop_move_candidates
    elif piece.piece_type == "Rook":
        return get_rook_move_candidates
    elif piece.piece_type == "Queen":
        return get_queen_move_candidates
    elif piece.piece_type == "King":
        return get_king_move_candidates
    raise Exception(f"Piece {piece} did not correspond to any piece type.")
