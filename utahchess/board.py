from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Generator, Iterable, Optional

from utahchess.piece import Piece, create_piece_instance_from_string, get_initial_pieces
from utahchess.utils import get_unicode_character, x_index_to_file, y_index_to_rank

NO_RANKS_AND_FILES = 8


@dataclass(frozen=True)
class Board:
    _board: tuple[tuple[Optional[Piece], ...], ...]

    def __init__(self, pieces: Iterable[Piece] = [], board_string: str = "") -> None:
        """Container for chess pieces.

        If no arguments are provided a board containing the original 32 chess pieces
        will be initialized.

        Args:
            pieces: Pieces to initialize the board with.
            board_string: A string describing a board state to initialize board from.
                Example:
                >>    board_string = f'''br-oo-oo-wq-oo-bc-oo-br
                >>            oo-oo-oo-oo-bk-oo-bp-oo
                >>            oo-wb-oo-oo-wp-bp-oo-oo
                >>            oo-bp-oo-oo-oo-wp-wk-oo
                >>            bq-wp-oo-oo-wp-oo-oo-bp
                >>            bb-oo-wp-oo-oo-oo-oo-oo
                >>            oo-oo-oo-oo-oo-oo-oo-oo
                >>            oo-wk-oo-wb-oo-wk-oo-wr'''

        Raises:
            Exception: If both a board string and an iterable of pieces are provided.
        """
        if pieces and board_string:
            raise ValueError(
                "Cannot create board when both pieces and board string are provided."
            )

        if not board_string:
            if not pieces:
                pieces = get_initial_pieces()

            _board = [
                [None for _ in range(NO_RANKS_AND_FILES)]
                for _ in range(NO_RANKS_AND_FILES)
            ]
            for piece in pieces:
                x, y = piece.position
                _board[x][y] = piece  # type: ignore

        elif board_string:
            _board = self._initialize_from_string(
                board_string=board_string,
            )  # type: ignore

        object.__setattr__(self, "_board", tuple(tuple(column) for column in _board))

    def __getitem__(self, indices: tuple[int, int]) -> Optional[Piece]:
        x, y = indices
        return self._board[x][y]

    def all_pieces(self) -> Generator[Piece, None, None]:
        """Get all current pieces on the board.

        Yields:
            All pieces on the board.
        """
        for x in range(NO_RANKS_AND_FILES):
            for y in range(NO_RANKS_AND_FILES):
                item = self._board[x][y]
                if item is not None:
                    yield item

    def copy(self) -> Board:
        """Create a copy of the board."""
        return Board(pieces=tuple(piece for piece in self.all_pieces()))

    def move_piece(
        self, from_position: tuple[int, int], to_position: tuple[int, int]
    ) -> Board:
        """Get a new board with one piece moved to a new position.

        If the destination is already occupied, the piece will be lost / captured.
        """
        if from_position == to_position:
            return self.copy()

        pieces = self.all_pieces()
        new_pieces = tuple(
            piece
            if piece.position != from_position
            else replace(
                piece,
                position=to_position,
                is_in_start_position=False,
                color=piece.color,
            )
            for piece in pieces
            if piece.position != to_position
        )
        return Board(pieces=new_pieces)

    def delete_piece(self, position: tuple[int, int]) -> Board:
        """Get a new board with one piece deleted."""
        return Board(
            pieces=tuple(
                piece for piece in self.all_pieces() if piece.position != position
            )
        )

    def to_string(self) -> str:
        """Get string representation of the board to use for initialization.

        Returns:
            A representation of the board that can be used to initialize a board.
            Example:
            >>    f'''oo-oo-oo-oo-oo-oo-oo-oo
            >>    oo-oo-oo-oo-bk-oo-oo-oo
            >>    oo-oo-oo-oo-oo-oo-oo-oo
            >>    wp-bp-wp-oo-oo-oo-oo-oo
            >>    oo-oo-oo-oo-oo-oo-oo-oo
            >>    oo-oo-oo-oo-oo-oo-oo-oo
            >>    oo-oo-oo-oo-oo-oo-oo-oo
            >>    oo-oo-oo-oo-wk-oo-oo-oo'''
        """
        board_string = "\n".join(
            [
                "-".join(
                    [
                        self[x, y].to_string() if self[x, y] is not None else "oo"  # type: ignore # noqa
                        for x in range(NO_RANKS_AND_FILES)
                    ]
                )
                for y in range(NO_RANKS_AND_FILES)
            ]
        )
        return board_string

    def __repr__(self) -> str:
        representation = (
            "          "
            + "".join(
                [f"     {x_index_to_file(i)}    " for i in range(NO_RANKS_AND_FILES)]
            )
            + "\n"
        )
        for y_coord in range(NO_RANKS_AND_FILES):
            row = "  " + "--------  " * (NO_RANKS_AND_FILES + 1) + "\n"
            row += f"    {y_index_to_rank(y_coord)}    | "
            for x_coord in range(NO_RANKS_AND_FILES):
                piece = self[(x_coord, y_coord)]
                row += get_unicode_character(piece=piece)
            representation += row + "\n"
        representation + "  " + "--------  " * (NO_RANKS_AND_FILES + 1)
        return representation

    def _initialize_from_string(
        self, board_string: str
    ) -> tuple[tuple[Piece, ...], ...]:
        """Initialize a board from a string."""
        _board = [
            [None for x_ in range(NO_RANKS_AND_FILES)]
            for _ in range(NO_RANKS_AND_FILES)
        ]
        row_string = board_string.replace(" ", "").split("\n")
        for y, row in enumerate(row_string):
            column_split_string = row.split("-")
            for x, tile_content in enumerate(column_split_string):
                piece = create_piece_instance_from_string((x, y), tile_content)
                _board[x][y] = piece  # type: ignore
        return tuple(tuple(column) for column in _board)  # type: ignore


def is_edible(board: Board, position: tuple[int, int], friendly_color: str) -> bool:
    """Get if a position on the board is edible.

    Edible is defined as the position on the board being both occupied as well as
    the piece on it from an enemy color.

    Args:
        board: Board to check.
        position: Position on the board to check.
        friendly_color: Color of pieces which are considered friendly.

    Returns:
        A flag indicating whether the position is edible or not.
    """
    if not is_occupied(board=board, position=position):
        return False
    return board[position].color != friendly_color  # type: ignore


def is_occupied(board: Board, position: tuple[int, int]) -> bool:
    """Get if a position on the board is occupied.

    Args:
        board: Board to check.
        position: Position on the board to check.

    Returns:
        A flag indicating whether the position is occupied or not.
    """
    return board[position] is not None
