from __future__ import annotations

from typing import Generator

from utahchess.board import Board


def get_all_move_candidates(
    board: Board,
) -> Generator[tuple[tuple[int, int], tuple[int, int]], None, None]:
    pass


def is_check(board: Board) -> bool:
    pass


def is_checkmate(board: Board) -> bool:
    pass


def validate_move_candidates(
    move_candidates: Generator[tuple[tuple[int, int], tuple[int, int]], None, None]
) -> Generator[tuple[tuple[int, int], tuple[int, int]], None, None]:
    pass
