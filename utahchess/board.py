from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Generator, Iterable, Optional

from utahchess.piece import Piece, get_initial_pieces


@dataclass(frozen=True)
class Board:
    _board: tuple[tuple[Piece, ...], ...]

    def __init__(self, pieces: Iterable[Piece] = []) -> None:
        if not pieces:
            pieces = get_initial_pieces()

        _board = [[None for x in range(8)] for y in range(8)]
        for piece in pieces:
            x, y = piece.position
            _board[x][y] = piece  # type: ignore

        object.__setattr__(self, "_board", tuple(tuple(column) for column in _board))

    def __getitem__(self, indices: tuple[int, int]) -> Optional[Piece]:
        x, y = indices
        return self._board[x][y]

    def all_pieces(self) -> Generator[Piece, None, None]:
        for x in range(8):
            for y in range(8):
                item = self._board[x][y]
                if item is not None:
                    yield item

    def copy(self) -> Board:
        new_pieces = tuple(piece for piece in self.all_pieces())
        return Board(pieces=new_pieces)

    def move_piece(
        self, from_position: tuple[int, int], to_position: tuple[int, int]
    ) -> Board:
        if from_position == to_position:
            return self.copy()
        pieces = self.all_pieces()
        new_pieces = tuple(
            piece
            if piece.position != from_position
            else replace(piece, position=to_position, color=piece.color)
            for piece in pieces
            if piece.position != to_position
        )
        return Board(pieces=new_pieces)

    def __repr__(self) -> str:
        representation = ""
        row = "          "
        for i in range(8):
            row += f"     {i}    "
        representation += row + "\n"
        for y_coord in range(8):
            row = "  "
            row += "--------  " * 9 + "\n"
            for x_coord in range(9):
                if x_coord == 0:
                    row += f"    {y_coord}    | "
                    continue
                else:
                    x_coord -= 1
                if self._board[x_coord][y_coord] is None:
                    row += "|       | "
                    continue
                if self._board[x_coord][y_coord].piece_type == "Pawn":
                    if self._board[x_coord][y_coord].color == "black":
                        row += f"|   \u265F   | "
                    if self._board[x_coord][y_coord].color == "white":
                        row += f"|   \u2659   | "
                if self._board[x_coord][y_coord].piece_type == "Knight":
                    if self._board[x_coord][y_coord].color == "black":
                        row += f"|   \u265E   | "
                    if self._board[x_coord][y_coord].color == "white":
                        row += f"|   \u2658   | "
                if self._board[x_coord][y_coord].piece_type == "Rook":
                    if self._board[x_coord][y_coord].color == "black":
                        row += f"|   \u265C   | "
                    if self._board[x_coord][y_coord].color == "white":
                        row += f"|   \u2656   | "
                if self._board[x_coord][y_coord].piece_type == "Bishop":
                    if self._board[x_coord][y_coord].color == "black":
                        row += f"|   \u265D   | "
                    if self._board[x_coord][y_coord].color == "white":
                        row += f"|   \u2657   | "
                if self._board[x_coord][y_coord].piece_type == "Queen":
                    if self._board[x_coord][y_coord].color == "black":
                        row += f"|   \u265B   | "
                    if self._board[x_coord][y_coord].color == "white":
                        row += f"|   \u2655   | "

                if self._board[x_coord][y_coord].piece_type == "King":
                    if self._board[x_coord][y_coord].color == "black":
                        row += f"|   \u265A   | "
                    if self._board[x_coord][y_coord].color == "white":
                        row += f"|   \u2654   | "

            representation += row + "\n"
        representation + "  " + "--------  " * 9
        return representation


def is_edible(board: Board, position: tuple[int, int], friendly_color: str) -> bool:

    if not is_occupied(board=board, position=position):
        return False
    return board[position].color != friendly_color  # type: ignore


def is_occupied(board: Board, position: tuple[int, int]) -> bool:
    return board[position] is not None


if __name__ == "__main__":
    board = Board()
    print(board.move_piece((0, 0), (0, 1)))
    print(board.move_piece((0, 1), (0, 0)))
