from __future__ import annotations

from utahchess import BLACK, WHITE
from utahchess.board import Board
from utahchess.move import Move
from utahchess.move_candidates import get_all_move_candidates


def is_check(board: Board, current_player: str) -> bool:
    """Checks if current player is in check.

    En Passant and Castling moves do not have to be considered
    as those are incapable of eating the current player's king.

    Args:
        board: Board on which to check whether current player is in check or not.
        current_player: Player for which the check is done.

    Returns: Flag indicating whether the current player is in check or not.
    """
    enemy_color = WHITE if current_player == BLACK else BLACK
    return find_current_players_king_position(
        board=board, current_player=current_player
    ) in [
        move[1]
        for move in get_all_move_candidates(board=board, current_player=enemy_color)
    ]


def is_valid_move(board: Board, move: Move) -> bool:
    """Get whether move is valid given the board.

    Checks whether the move would leave the king of the player executing
    the move in check, which is not allowed.

    Args:
        board: Board on which move would be executed.
        move: Move which is checked.

    Returns: Flag indicating whether the move is valid or not.
    """
    board_after_move = board.copy()
    current_player = board[move.piece_moves[0][0]].color  # type: ignore
    for piece_move in move.piece_moves:
        board_after_move = board_after_move.move_piece(
            from_position=piece_move[0], to_position=piece_move[1]
        )
    for piece_to_delete in move.pieces_to_delete:
        board_after_move = board_after_move.delete_piece(position=piece_to_delete)
    return not is_check(board=board_after_move, current_player=current_player)


def find_current_players_king_position(
    board: Board, current_player: str
) -> tuple[int, int]:
    """Get the position of the current player's king."""
    for piece in board.all_pieces():
        if piece.piece_type == "King" and piece.color == current_player:
            return piece.position
    raise Exception(f"No King found for {current_player}")
