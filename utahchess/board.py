from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Generator, Iterable, Optional

from utahchess._board_repr import representation
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
        """Get a new board with one piece moved to a new position.

        If the to_position is occupied already, the piece there will be lost.
        """
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

    def delete_piece(self, position: tuple[int, int]) -> Board:
        """Get a new board with one piece deleted."""
        new_pieces = tuple(
            piece for piece in self.all_pieces() if piece.position != position
        )
        return Board(pieces=new_pieces)

    def __repr__(self) -> str:
        return representation(self._board)


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
