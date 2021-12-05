from __future__ import annotations

import string
from itertools import chain
from typing import Generator, Optional, Sequence

from utahchess.algebraic_notation import AlgebraicNotation
from utahchess.board import Board
from utahchess.castling import get_castling_moves
from utahchess.en_passant import get_en_passant_moves
from utahchess.move import EN_PASSANT_MOVE, LONG_CASTLING, SHORT_CASTLING, Move
from utahchess.move_validation import is_check, is_checkmate
from utahchess.regular_move import get_regular_moves

FILE_POSSIBILITIES = "abcdefgh"
RANK_POSSIBILITIES = "87654321"


def get_algebraic_notation_mapping(
    board: Board, current_player: str, last_move: Optional[Move] = None
) -> dict[str, Move]:
    ambiguous_mapping = _get_ambiguous_algebraic_notation_mapping(
        board=board, current_player=current_player, last_move=last_move
    )
    mapping: dict[str, Move] = {}
    for algebraic_identifer, moves in ambiguous_mapping.items():
        mapping = {
            **_disambiguate_moves(
                ambiguous_identifier=algebraic_identifer,
                moves_to_disambiguate=moves,
            ),
            **mapping,
        }
    return mapping


def make_move(board: Board, move: Move) -> Board:
    board_after_move = board.copy()
    for piece_move in move.piece_moves:
        board_after_move = board_after_move.move_piece(
            from_position=piece_move[0], to_position=piece_move[1]
        )
    for piece_to_delete in move.pieces_to_delete:
        board_after_move = board_after_move.delete_piece(position=piece_to_delete)
    return board_after_move


def x_index_to_file(x: int) -> str:
    return FILE_POSSIBILITIES[x]


def y_index_to_rank(y: int) -> str:
    return RANK_POSSIBILITIES[y]


def rank_to_y_index(rank: str) -> int:
    return 8 - int(rank)


def file_to_x_index(file: str) -> int:
    return string.ascii_lowercase.index(file)


def is_stalemate(
    board: Board,
    current_player: str,
    legal_moves_for_current_player: Sequence[str],
) -> bool:

    return (
        not is_check(board=board, current_player=current_player)
        and len(legal_moves_for_current_player) == 0
    )


def _get_ambiguous_algebraic_notation_mapping(
    board: Board, current_player: str, last_move: Optional[Move]
) -> dict[AlgebraicNotation, list[Move]]:

    mapping: dict[AlgebraicNotation, list[Move]] = {}
    for legal_move in _get_all_legal_moves(
        board=board, current_player=current_player, last_move=last_move
    ):
        ambiguous_identifer = AlgebraicNotation(
            castling_identifier=_get_castling_identifer(
                move=legal_move,
            ),  # type: ignore
            en_passant_identifer=_get_en_passant_identifier(move=legal_move),
            piece=_get_moving_piece_signifier(move=legal_move),
            destination_tile=_get_destination_tile(move=legal_move),
            capturing_flag=_get_capturing_flag(move=legal_move),
            check_or_checkmate_flag=_get_check_or_checkmate_identifier(
                board=board, move=legal_move, current_player=current_player
            ),
        )
        mapping.setdefault(ambiguous_identifer, []).append(legal_move)
    return mapping


def _get_all_legal_moves(
    board: Board, current_player: str, last_move: Optional[Move]
) -> Generator[Move, None, None]:
    regular_moves = get_regular_moves(board=board, current_player=current_player)
    castling_moves = get_castling_moves(board=board, current_player=current_player)
    en_passant_moves = get_en_passant_moves(board=board, last_move=last_move)
    return chain(regular_moves, en_passant_moves, castling_moves)  # type: ignore


def _get_moving_piece_signifier(move: Move) -> str:
    piece = move.moving_pieces[0]
    if piece.piece_type == "Pawn":
        return ""
    elif piece.piece_type == "King":
        return "K"
    elif piece.piece_type == "Bishop":
        return "B"
    elif piece.piece_type == "Queen":
        return "Q"
    elif piece.piece_type == "Knight":
        return "N"
    elif piece.piece_type == "Rook":
        return "R"
    raise Exception(f"Unrecognized piece type: {piece.piece_type}")


def _get_destination_tile(move: Move) -> str:
    x, y = move.piece_moves[0][1]
    return f"{x_index_to_file(x=x)}{y_index_to_rank(y=y)}"


def _get_capturing_flag(move: Move) -> str:
    return "x" if move.is_capturing_move else ""


def _get_castling_identifer(move: Move) -> str:
    if move.type == SHORT_CASTLING:
        return "O-O"
    elif move.type == LONG_CASTLING:
        return "O-O-O"
    else:
        return ""


def _disambiguate_moves(
    ambiguous_identifier: AlgebraicNotation, moves_to_disambiguate: list[Move]
) -> dict[str, Move]:
    """Get unambiguous algebraic notation for ambigious identifiers."""
    if len(moves_to_disambiguate) == 1:
        return {ambiguous_identifier.to_string(): moves_to_disambiguate[0]}

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
            ambiguous_identifier.to_string_with_file(file=file1): move1,
            ambiguous_identifier.to_string_with_file(file=file2): move2,
        }
    elif not rank1 == rank2:
        return {
            ambiguous_identifier.to_string_with_rank(rank=rank1): move1,
            ambiguous_identifier.to_string_with_rank(rank=rank2): move2,
        }
    raise Exception(
        f"Moves {moves_to_disambiguate} with ambiguous identifier "
        f"{ambiguous_identifier} could not be disambiguated with just rank and file."
    )


def _get_en_passant_identifier(move: Move) -> str:
    if move.type == EN_PASSANT_MOVE:
        return " e.p."
    return ""


def _get_moving_piece_file(move: Move) -> str:
    x_from, y_from = move.piece_moves[0][0]
    return x_index_to_file(x=x_from)


def _get_moving_piece_rank(move: Move) -> str:
    x_from, y_from = move.piece_moves[0][0]
    return y_index_to_rank(y=y_from)


def _get_check_or_checkmate_identifier(
    board: Board, move: Move, current_player: str
) -> str:

    if is_checkmate(
        board=make_move(board=board, move=move),
        current_player=_get_opposite_player(current_player=current_player),
    ):
        return "#"
    elif is_check(
        board=make_move(board=board, move=move),
        current_player=_get_opposite_player(current_player=current_player),
    ):
        return "+"
    else:
        return ""


def _get_opposite_player(current_player: str) -> str:
    return "black" if current_player == "white" else "white"
