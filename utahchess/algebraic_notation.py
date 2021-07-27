from __future__ import annotations

import string
from dataclasses import dataclass, field

from utahchess.board import Board
from utahchess.castling import CASTLING_MOVE, LONG_CASTLING, SHORT_CASTLING
from utahchess.en_passant import EN_PASSANT_MOVE
from utahchess.legal_moves import get_all_legal_moves
from utahchess.move import Move
from utahchess.move_validation import REGULAR_MOVE

FILE_POSSIBILITIES = "abcdefgh"
RANK_POSSIBILITIES = "87654321"


@dataclass(frozen=True)
class AmbiguousAlgebraicNotation:
    castling_identifier: str
    en_passant_identifer: str
    piece: str
    destination_tile: str
    capturing_flag: str

    def to_string(self) -> str:
        if self.castling_identifier:
            return self.castling_identifier
        return f"{self.piece}{self.capturing_flag}{self.destination_tile}{self.en_passant_identifer}"

    def __repr__(self) -> str:
        return self.to_string()


def x_index_to_file(x: int) -> str:
    return FILE_POSSIBILITIES[x]


def y_index_to_rank(y: int) -> str:
    return RANK_POSSIBILITIES[y]


def rank_to_y_index(rank: str) -> int:
    return 8 - int(rank)


def file_to_x_index(file: str) -> int:
    return string.ascii_lowercase.index(file)


def get_algebraic_notation_mapping(
    board: Board, current_player: str, last_move: Move
) -> dict[str, Move]:
    ambiguous_mapping = _get_ambiguous_algebraic_notation_mapping(
        board=board, current_player=current_player, last_move=last_move
    )
    mapping: dict[str, Move] = {}
    for algebraic_identifer, moves in ambiguous_mapping.items():
        mapping = {
            **_disambiguate_moves(
                ambiguous_identifier=algebraic_identifer, moves_to_disambiguate=moves
            ),
            **mapping,
        }
    return mapping


def _get_ambiguous_algebraic_notation_mapping(
    board: Board, current_player: str, last_move: Move
) -> dict[AmbiguousAlgebraicNotation, list[Move]]:

    mapping: dict[AmbiguousAlgebraicNotation, list[Move]] = {}
    for legal_move in get_all_legal_moves(
        board=board, current_player=current_player, last_move=last_move
    ):
        ambiguous_identifer = AmbiguousAlgebraicNotation(
            castling_identifier=_get_castling_move_algebraic_notation(move=legal_move),
            en_passant_identifer=_get_en_passant_identifier(move=legal_move),
            piece=_get_moving_piece_signifier(move=legal_move),
            destination_tile=_get_destination_tile(move=legal_move),
            capturing_flag=_get_capturing_flag(move=legal_move),
        )
        mapping.setdefault(ambiguous_identifer, []).append(legal_move)
    return mapping


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


def _get_castling_move_algebraic_notation(move: Move) -> str:
    if not move.type == CASTLING_MOVE:
        return ""
    if move.castling_type == SHORT_CASTLING:
        return "O-O"
    elif move.castling_type == LONG_CASTLING:
        return "O-O-O"
    raise Exception(f"{move} is not a valid Castling Move")


def _disambiguate_moves(
    ambiguous_identifier: AmbiguousAlgebraicNotation, moves_to_disambiguate: list[Move]
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
            _add_file_to_ambiguous_identifier(
                ambiguous_identifier=ambiguous_identifier, file=file1
            ): move1,
            _add_file_to_ambiguous_identifier(
                ambiguous_identifier=ambiguous_identifier, file=file2
            ): move2,
        }
    elif not rank1 == rank2:
        return {
            _add_rank_to_ambiguous_identifier(
                ambiguous_identifier=ambiguous_identifier, rank=rank1
            ): move1,
            _add_rank_to_ambiguous_identifier(
                ambiguous_identifier=ambiguous_identifier, rank=rank2
            ): move2,
        }
    raise Exception(
        f"Moves {moves_to_disambiguate} with ambiguous identifier {ambiguous_identifier} could not be disambiguated with just rank and file."
    )


def _add_file_to_ambiguous_identifier(
    ambiguous_identifier: AmbiguousAlgebraicNotation, file: str
) -> str:
    return f"{ambiguous_identifier.piece}{file}{ambiguous_identifier.capturing_flag}{ambiguous_identifier.destination_tile}{ambiguous_identifier.en_passant_identifer}"


def _add_rank_to_ambiguous_identifier(
    ambiguous_identifier: AmbiguousAlgebraicNotation, rank: str
) -> str:
    return f"{ambiguous_identifier.piece}{rank}{ambiguous_identifier.capturing_flag}{ambiguous_identifier.destination_tile}{ambiguous_identifier.en_passant_identifer}"


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
