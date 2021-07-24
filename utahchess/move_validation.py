from __future__ import annotations

from dataclasses import dataclass
from typing import Generator

from utahchess.board import Board
from utahchess.move import Move
from utahchess.move_candidates import get_all_move_candidates
from utahchess.piece import Piece


@dataclass
class RegularMove(Move):
    type = "Regular Move"
    piece_moves: tuple[tuple[tuple[int, int], tuple[int, int]], ...]
    moving_pieces: tuple[Piece, ...]
    is_capturing_move: bool

    def __init__(
        self,
        piece_moves: tuple[tuple[tuple[int, int], tuple[int, int]]],
        moving_pieces: tuple[Piece],
        is_capturing_move: bool,
    ) -> None:
        self.piece_moves = piece_moves
        self.moving_pieces = moving_pieces
        self.is_capturing_move = is_capturing_move
        self.allows_en_passant = self._set_allows_en_passant_flag()

    def _set_allows_en_passant_flag(self) -> bool:
        return (
            self.moving_pieces[0].piece_type == "Pawn"
            and abs(_get_distance_moved_in_y_direction(self.piece_moves[0])) == 2
        )


def _get_distance_moved_in_y_direction(
    piece_move: tuple[tuple[int, int], tuple[int, int]]
) -> int:
    return piece_move[1][1] - piece_move[0][1]


def is_check(board: Board, current_player: str) -> bool:
    """Checks if current_player is in check.

    En Passant and Castling moves do not have to be considered
    as those are incapable of eating the current player's king.
    """
    enemy_color = "white" if current_player == "black" else "black"
    current_player_king_position = find_current_players_king_position(
        board=board, current_player=current_player
    )
    all_possible_enemy_move_candidates = get_all_move_candidates(
        board=board, current_player=enemy_color
    )

    all_possible_enemy_destinations = [
        move[1] for move in all_possible_enemy_move_candidates
    ]

    return current_player_king_position in all_possible_enemy_destinations


def find_current_players_king_position(
    board: Board, current_player: str
) -> tuple[int, int]:
    for piece in board.all_pieces():
        if piece.piece_type == "King" and piece.color == current_player:
            return piece.position
    raise Exception(f"No King found for {current_player}")


def is_checkmate(board: Board, current_player: str) -> bool:
    """Check if current player is in checkmate."""

    def all_possible_boards():
        all_move_candidates = get_all_move_candidates(
            board=board, current_player=current_player
        )
        for move_candidate in all_move_candidates:
            from_position, to_position = move_candidate
            yield board.move_piece(from_position=from_position, to_position=to_position)

    for possible_board in all_possible_boards():
        if not is_check(board=possible_board, current_player=current_player):
            return False
    return is_check(board=board, current_player=current_player)


def validate_move_candidates(
    board: Board,
    move_candidates: Generator[tuple[tuple[int, int], tuple[int, int]], None, None],
) -> Generator[RegularMove, None, None]:
    """Filter move candidates based on whether they leave king unprotected."""

    for move_candidate in move_candidates:
        from_position, to_position = move_candidate
        board_after_move = board.move_piece(
            from_position=from_position, to_position=to_position
        )

        current_player = board[from_position].color
        destination = board[to_position]
        is_capturing_move = False if destination is None else True
        if not is_check(board=board_after_move, current_player=current_player):
            yield RegularMove(
                piece_moves=(move_candidate,),
                moving_pieces=(board[from_position],),
                is_capturing_move=is_capturing_move,
            )
