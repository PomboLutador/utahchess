from __future__ import annotations

from dataclasses import dataclass

from utahchess.board import Board
from utahchess.piece import Piece

SHORT_CASTLING = "Short Castling Move"
LONG_CASTLING = "Long Castling Move"
EN_PASSANT_MOVE = "En Passant Move"
REGULAR_MOVE = "Regular Move"


@dataclass(frozen=True)
class Move:
    type: str
    piece_moves: tuple[tuple[tuple[int, int], tuple[int, int]], ...]
    moving_pieces: tuple[Piece, ...]
    is_capturing_move: bool
    allows_en_passant: bool
    pieces_to_delete: tuple[tuple[int, int], ...] = ()


def make_move(board: Board, move: Move) -> Board:
    board_after_move = board.copy()
    for piece_move in move.piece_moves:
        board_after_move = board_after_move.move_piece(
            from_position=piece_move[0], to_position=piece_move[1]
        )
    for piece_to_delete in move.pieces_to_delete:
        board_after_move = board_after_move.delete_piece(position=piece_to_delete)
    return board_after_move
    # def to_string(self, **kwargs) -> str:
    #     pass


#     def to_string(self) -> str:
#         if self.type in (LONG_CASTLING, SHORT_CASTLING):
#             return self._get_castling_identifer()
#         return (
#             f"{self._get_moving_piece()}{self._get_capturing_flag()}{self._get_destination_tile()}"
#             f"{self._get_en_passant_identifier()}{self.check_or_checkmate_flag}"
#         )


#     def _get_castling_identifer(self) -> str:
#         if self.type == SHORT_CASTLING:
#             return "O-O"
#         elif self.type == LONG_CASTLING:
#             return "O-O-O"
#         else:
#             return ""

#     def _get_moving_piece(self) -> Piece:
#         return self.moving_pieces[0]

#     def _get_capturing_flag(self) -> str:
#         return "x" if self.is_capturing_move else ""

#     def _get_destination_tile(self) -> str:
#         return self.piece_moves[0][1]

#     def _get_en_passant_identifier(self) -> str:
#         if self.type == EN_PASSANT_MOVE:
#             return " e.p."
#         return ""

#     def _get_check_or_checkmate_identifier(
#     board: Board, move: Move, current_player: str
# ) -> str:
#         if is_checkmate(
#             board=make_move(board=board, move=move),
#             current_player=_get_opposite_player(current_player=current_player),
#         ):
#             return "#"
#         elif is_check(
#             board=make_move(board=board, move=move),
#             current_player=_get_opposite_player(current_player=current_player),
#         ):
#             return "+"
#         else:
#             return ""
