from __future__ import annotations

import random
from itertools import product
from typing import Type

from utahchess import BLACK, WHITE
from utahchess.board import Board
from utahchess.legal_moves import is_checkmate
from utahchess.move_validation import is_check
from utahchess.piece import Bishop, King, Knight, Pawn, Piece, Queen, Rook

ALL_POSITIONS = tuple(product((0, 1, 2, 3, 4, 5, 6, 7), (0, 1, 2, 3, 4, 5, 6, 7)))
NUMBER_OF_TOTAL_POSITIONS = len(ALL_POSITIONS)
POSSIBLE_INDICES = list(range(NUMBER_OF_TOTAL_POSITIONS))

IMBALANCE_RANGE_LOW = 0.3
IMBALANCE_RANGE_HIGH = 0.7


def sample_n_positions(n: int) -> list[tuple[int, int]]:
    """Generate n positions on a chess board at random."""
    random.shuffle(POSSIBLE_INDICES)
    return list(ALL_POSITIONS[i] for i in POSSIBLE_INDICES[:n])


def sample_random_board(n_pieces: int) -> Board:
    """Generate semi-random chess board.

    The board is configured by first placing the king of each color.
    The amount of pieces left to distribute are allocated at random between 30% white
    and 70% white.
    Types of pieces are randomly sampled according to their occurence. This means a
    white rook is twice as likely to appear than a white queen but is four time less
    like to appear than a white pawn.
    In the end the procedure is repeated if the resulting board is arleady in check or
    checkmate.

    Args:
        n_pieces: Number of pieces to distribute on the board.

    Returns: A board with randomly distributed pieces placed on it. Always contains
        each color's king and is never in check or checkmate.
    """
    board_pieces: list[Piece] = []
    positions_to_fill = sample_n_positions(n=n_pieces)
    # place two kings
    board_pieces.append(
        King(
            position=positions_to_fill.pop(),
            color=WHITE,
            is_in_start_position=False,
        )
    )
    board_pieces.append(
        King(
            position=positions_to_fill.pop(),
            color=BLACK,
            is_in_start_position=False,
        )
    )

    pieces_left = n_pieces - 2
    white_number_of_pieces = int(
        random.uniform(IMBALANCE_RANGE_LOW, IMBALANCE_RANGE_HIGH) * pieces_left
    )
    black_number_of_pieces = pieces_left - white_number_of_pieces

    for color, number_of_pieces in zip(
        (WHITE, BLACK), (white_number_of_pieces, black_number_of_pieces)
    ):
        pawn_counter = 0
        bishop_counter = 0
        knight_counter = 0
        rook_counter = 0
        queen_counter = 0
        valid_choices: tuple[Type[Piece], ...] = (
            Pawn,
            Bishop,
            Knight,
            Rook,
            Queen,
        )
        for _ in range(number_of_pieces):
            class_to_instantiate = random.choice(valid_choices)  # type: ignore
            board_pieces.append(
                class_to_instantiate(  # type: ignore
                    position=positions_to_fill.pop(),
                    color=color,
                    is_in_start_position=False,
                )
            )
            if class_to_instantiate == Pawn:
                pawn_counter += 1
                if pawn_counter == 8:
                    valid_choices = tuple(
                        valid_choice
                        for valid_choice in valid_choices
                        if valid_choice != Pawn
                    )
            elif class_to_instantiate == Bishop:
                bishop_counter += 1
                if bishop_counter == 2:
                    valid_choices = tuple(
                        valid_choice
                        for valid_choice in valid_choices
                        if valid_choice != Bishop
                    )
            elif class_to_instantiate == Knight:
                knight_counter += 1
                if knight_counter == 2:
                    valid_choices = tuple(
                        valid_choice
                        for valid_choice in valid_choices
                        if valid_choice != Knight
                    )
            elif class_to_instantiate == Rook:
                rook_counter += 1
                if rook_counter == 2:
                    valid_choices = tuple(
                        valid_choice
                        for valid_choice in valid_choices
                        if valid_choice != Rook
                    )
            elif class_to_instantiate == Queen:
                queen_counter += 1
                valid_choices = tuple(
                    valid_choice
                    for valid_choice in valid_choices
                    if valid_choice != Queen
                )

    board = Board(pieces=board_pieces)

    if is_checkmate(board=board, current_player=BLACK, last_move=None) or is_checkmate(
        board=board, current_player=WHITE, last_move=None
    ):
        return sample_random_board(n_pieces=n_pieces)
    if is_check(board=board, current_player=BLACK) or is_check(
        board=board, current_player=WHITE
    ):
        return sample_random_board(n_pieces=n_pieces)
    return board


if __name__ == "__main__":
    NUM_BOARDS = 1000
    count = 0
    while count < NUM_BOARDS:
        num_pieces = int(random.uniform(6, 20))
        board = sample_random_board(n_pieces=num_pieces)
        count += 1
        if count % 10 == 0:
            print(f"Saving board {count}")
        with open(
            f"analyses"
            f"/alpha_beta_performance_increase/board_strings/board_{count}.txt",
            "w",
        ) as file:
            file.write(board.to_string())
