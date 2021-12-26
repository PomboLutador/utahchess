from __future__ import annotations

from itertools import chain
from typing import Generator, Optional

from utahchess.algebraic_notation import get_algebraic_identifer
from utahchess.board import Board
from utahchess.castling import get_castling_moves
from utahchess.en_passant import get_en_passant_moves
from utahchess.move import Move
from utahchess.regular_move import get_regular_moves
from utahchess.utils import x_index_to_file, y_index_to_rank


def get_move_per_algebraic_identifier(
    board: Board, current_player: str, last_move: Optional[Move] = None
) -> dict[str, Move]:
    """Get a map of algebraic identifiers to moves for current player.

    Args:
        board: Board on which to compute all legal moves.
        current_player: Player for which to get all legal moves.
        last_move: Last move that was executed on the board.

    Returns: A map from algebraic identifiers to each legal move possible on the board.
    """
    ambiguous_mapping = _get_ambiguous_algebraic_notation_mapping(
        board=board, current_player=current_player, last_move=last_move
    )
    mapping: dict[str, Move] = {}
    for algebraic_identifer, moves in ambiguous_mapping.items():
        mapping = {
            **_disambiguate_moves(
                board=board,
                ambiguous_identifier=algebraic_identifer,
                moves_to_disambiguate=moves,
            ),
            **mapping,
        }
    return mapping


def _get_all_legal_moves(
    board: Board, current_player: str, last_move: Optional[Move]
) -> Generator[Move, None, None]:
    regular_moves = get_regular_moves(board=board, current_player=current_player)
    castling_moves = get_castling_moves(board=board, current_player=current_player)
    en_passant_moves = get_en_passant_moves(board=board, last_move=last_move)
    return chain(regular_moves, en_passant_moves, castling_moves)  # type: ignore


def _get_ambiguous_algebraic_notation_mapping(
    board: Board, current_player: str, last_move: Optional[Move]
) -> dict[str, list[Move]]:
    """Get a map of algebraic identifiers to lists of moves.

    All moves with the same algebraic identifier (without rank or file) are mapped to
    the same key in the mapping.
    """
    mapping: dict[str, list[Move]] = {}
    for legal_move in _get_all_legal_moves(
        board=board, current_player=current_player, last_move=last_move
    ):
        ambiguous_identifer = get_algebraic_identifer(move=legal_move, board=board)
        mapping.setdefault(ambiguous_identifer, []).append(legal_move)
    return mapping


def _disambiguate_moves(
    board: Board, ambiguous_identifier: str, moves_to_disambiguate: list[Move]
) -> dict[str, Move]:
    """Get unambiguous algebraic notation for ambiguous identifiers.

    If two pieces of the same kind would end up in the same spot, without considering
    rank or file, the move will have the same algebraic identifier. To disambiguate
    such moves either rank or file will be added to each move's identifier to arrive at
    unambiguous algebraic identifiers.
    """
    if len(moves_to_disambiguate) == 1:
        return {ambiguous_identifier: moves_to_disambiguate[0]}

    if len(moves_to_disambiguate) > 2:
        raise NotImplementedError(
            "Functionality to disambiguate more than 2 moves not yet implemented."
        )

    move1, move2 = moves_to_disambiguate
    file1, rank1 = (
        _get_moving_piece_file(move=move1),
        _get_moving_piece_rank(move=move1),
    )
    file2, rank2, = (
        _get_moving_piece_file(move=move2),
        _get_moving_piece_rank(move=move2),
    )

    if not file1 == file2:
        return {
            get_algebraic_identifer(board=board, move=move1, file=file1): move1,
            get_algebraic_identifer(board=board, move=move2, file=file2): move2,
        }
    elif not rank1 == rank2:
        return {
            get_algebraic_identifer(board=board, move=move1, rank=rank1): move1,
            get_algebraic_identifer(board=board, move=move2, rank=rank2): move2,
        }
    raise Exception(
        f"Moves {moves_to_disambiguate} with ambiguous identifier "
        f"{ambiguous_identifier} could not be disambiguated with just rank and file."
    )


def _get_moving_piece_file(move: Move) -> str:
    x_from, y_from = move.piece_moves[0][0]
    return x_index_to_file(x=x_from)


def _get_moving_piece_rank(move: Move) -> str:
    x_from, y_from = move.piece_moves[0][0]
    return y_index_to_rank(y=y_from)
