from __future__ import annotations

from typing import Generator

from utahchess.board import Board
from utahchess.move import Move
from utahchess.move_candidates import get_all_move_candidates
from utahchess.piece import Piece

REGULAR_MOVE = "Regular Move"


def _set_allows_en_passant_flag(
    moving_pieces: tuple[Piece],
    piece_moves: tuple[tuple[tuple[int, int], tuple[int, int]]],
) -> bool:
    return (
        moving_pieces[0].piece_type == "Pawn"
        and abs(_get_distance_moved_in_y_direction(piece_moves[0])) == 2
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
) -> Generator[Move, None, None]:
    """Filter move candidates based on whether they leave king unprotected."""

    for move_candidate in move_candidates:
        from_position, to_position = move_candidate
        board_after_move = board.move_piece(
            from_position=from_position, to_position=to_position
        )
        from_piece = board[from_position]
        if from_piece is None:
            raise Exception(
                f"Piece at position {from_position} is None when the position should be occupied."
            )

        current_player = from_piece.color
        destination = board[to_position]
        is_capturing_move = False if destination is None else True
        if not is_check(board=board_after_move, current_player=current_player):
            yield Move(
                type=REGULAR_MOVE,
                piece_moves=(move_candidate,),
                moving_pieces=(from_piece,),
                is_capturing_move=is_capturing_move,
                allows_en_passant=_set_allows_en_passant_flag(
                    piece_moves=(move_candidate,), moving_pieces=(from_piece,)
                ),
            )


def get_legal_regular_moves(
    board: Board, current_player: str
) -> Generator[Move, None, None]:
    all_move_candidates = get_all_move_candidates(
        board=board, current_player=current_player
    )
    return validate_move_candidates(board=board, move_candidates=all_move_candidates)


def make_regular_move(board: Board, move: Move) -> Board:
    from_position, to_position = move.piece_moves[0]
    return board.move_piece(from_position=from_position, to_position=to_position)
