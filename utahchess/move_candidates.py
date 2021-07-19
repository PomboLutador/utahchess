from __future__ import annotations

import abc
from itertools import chain
from typing import Generator

from utahchess.board import Board, is_edible, is_occupied
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


class Piece(abc.ABC):
    def __init__(
        self,
        position: tuple[int, int],
        color: str,
        is_in_start_position: bool,
    ) -> None:
        self.position = position
        self.color = color
        self.is_in_start_position = is_in_start_position

    @abc.abstractmethod
    def get_move_candidates(
        self, board: Board
    ) -> Generator[tuple[tuple[int, int], tuple[int, int]], None, None]:
        """
        Get possible move candidates for the piece given a board.
        """
        pass

    def set_position(self, position: tuple[int, int]) -> None:
        self.position = position
        self.is_in_start_position = False

    def get_position(self) -> tuple[int, int]:
        return self.position


def get_pawn_move_candidates(
    board: Board, pawn_position: tuple[int, int]
) -> Generator[tuple[tuple[int, int], tuple[int, int]], None, None]:
    pawn = board[pawn_position]
    if pawn is None:
        return
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
            position=pawn.position, movement_vector=(-1, 1 * movement_direction)
        ),
    ]
    for tile_to_check in tiles_to_check:
        if is_in_bounds(position=tile_to_check):
            if is_edible(
                board=board, position=tile_to_check, friendly_color=pawn.color
            ):
                yield (pawn.position, tile_to_check)


def get_knight_move_candidates(
    self, board: Board
) -> Generator[tuple[tuple[int, int], tuple[int, int]], None, None]:

    for movement_vector in KNIGHT_MOVEMENT_VECTORS:

        tile_to_check = apply_movement_vector(
            position=self.position, movement_vector=movement_vector
        )
        if is_in_bounds(position=tile_to_check):
            if is_occupied(board=board, position=tile_to_check) or is_edible(
                board=board, position=tile_to_check, friendly_color=self.color
            ):
                yield (self.position, tile_to_check)


def get_rook_move_candidates(
    board: Board, rook_position: tuple[int, int]
) -> Generator[tuple[tuple[int, int], tuple[int, int]], None, None]:

    horizontal_move_candidates = _get_horizontal_moves(
        board=board, initial_position=rook_position
    )
    vertical_move_candidates = _get_vertical_moves(
        board=board, initial_position=rook_position
    )

    return chain(horizontal_move_candidates, vertical_move_candidates)  # type: ignore


def get_bishop_move_candidates(
    self, board: Board
) -> Generator[tuple[tuple[int, int], tuple[int, int]], None, None]:

    return self._get_diagonal_moves(board)


def get_queen_move_candidates(
    board: Board, initial_position: tuple[int, int]
) -> Generator[tuple[tuple[int, int], tuple[int, int]], None, None]:

    diagonal_move_candidates = _get_diagonal_moves(
        board=board, initial_position=initial_position
    )
    horizontal_move_candidates = _get_horizontal_moves(
        board=board, initial_position=initial_position
    )
    vertical_move_candidates = _get_vertical_moves(
        board=board, initial_position=initial_position
    )

    return chain(
        diagonal_move_candidates,
        horizontal_move_candidates,
        vertical_move_candidates,
    )  # type: ignore


def get_king_move_candidates(
    board: Board, initial_position: tuple[int, int]
) -> Generator[tuple[tuple[int, int], tuple[int, int]], None, None]:
    king = board[initial_position]
    if king is None:
        return
    for movement_vector in KING_MOVEMENT_VECTORS:

        tile_to_check = apply_movement_vector(
            position=initial_position, movement_vector=movement_vector
        )
        if is_in_bounds(position=tile_to_check):
            if not is_occupied(board=board, position=tile_to_check) or is_edible(
                board=board, position=tile_to_check, friendly_color=king.color
            ):
                yield (initial_position, tile_to_check)


def _get_straight_line_moves(
    board: Board, initial_position: tuple[int, int], movement_vector: tuple[int, int]
) -> Generator[tuple[tuple[int, int], tuple[int, int]], None, None]:
    piece = board[initial_position]
    if piece is None:
        return
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
