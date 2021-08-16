from __future__ import annotations

from itertools import product

import numpy as np

from utahchess.board import Board
from utahchess.move_validation import is_check, is_checkmate
from utahchess.piece import Bishop, King, Knight, Pawn, Piece, Queen, Rook

ALL_POSITIONS = tuple(product((0, 1, 2, 3, 4, 5, 6, 7), (0, 1, 2, 3, 4, 5, 6, 7)))
NUMBER_OF_TOTAL_POSITIONS = len(ALL_POSITIONS)
POSSIBLE_INDICES = list(range(NUMBER_OF_TOTAL_POSITIONS))

IMBALANCE_RANGE_LOW = 0.3
IMBALANCE_RANGE_HIGH = 0.7


def sample_n_positions(n: int) -> list[tuple[int, int]]:
    np.random.shuffle(POSSIBLE_INDICES)
    return list(ALL_POSITIONS[i] for i in POSSIBLE_INDICES[:n])


def sample_random_board(n_pieces: int) -> Board:
    board_pieces = []
    positions_to_fill = sample_n_positions(n=n_pieces)
    # place two kings
    board_pieces.append(
        King(
            position=positions_to_fill.pop(), color="white", is_in_start_position=False
        )
    )
    board_pieces.append(
        King(
            position=positions_to_fill.pop(), color="black", is_in_start_position=False
        )
    )

    pieces_left = n_pieces - 2
    white_number_of_pieces = int(
        np.random.uniform(IMBALANCE_RANGE_LOW, IMBALANCE_RANGE_HIGH) * pieces_left
    )
    black_number_of_pieces = pieces_left - white_number_of_pieces

    for color, number_of_pieces in zip(
        ("white", "black"), (white_number_of_pieces, black_number_of_pieces)
    ):
        pawn_counter = 0
        bishop_counter = 0
        knight_counter = 0
        rook_counter = 0
        queen_counter = 0
        valid_choices: tuple[Piece, ...] = (Pawn, Bishop, Knight, Rook, Queen)
        for _ in range(number_of_pieces):
            class_to_instantiate = np.random.choice(valid_choices)
            board_pieces.append(
                class_to_instantiate(
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

    if is_checkmate(board=board, current_player="black") or is_checkmate(
        board=board, current_player="white"
    ):
        return None
    if is_check(board=board, current_player="black") or is_check(
        board=board, current_player="white"
    ):
        return None
    return board


if __name__ == "__main__":
    NUM_BOARDS = 1000
    count = 0
    while count < NUM_BOARDS:
        num_pieces = int(np.random.uniform(3, 20))
        board = sample_random_board(n_pieces=num_pieces)
        if board is not None:
            count += 1
            if count % 10 == 0:
                print(f"Saving board {count}")
            with open(
                f"analyses/alpha_beta_performance_increase/board_strings/board_{count}.txt",
                "w",
            ) as file:
                file.write(board.to_string())
