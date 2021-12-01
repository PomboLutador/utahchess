from __future__ import annotations

import time
from functools import partial
from os import walk
from typing import Generator, Sequence

import numpy as np
from anytree import Node  # type: ignore

from utahchess.board import Board
from utahchess.minimax import create_children_from_parent, get_node_value, minimax


def generate_dataset(
    dataset_path: str, num_boards: int
) -> Generator[Board, None, None]:
    for root, _, filenames in walk(dataset_path):
        for count, filename in enumerate(filenames):
            if count == num_boards:
                break
            with open(f"{root}/{filename}", "r") as file:
                yield Board(board_string=file.read())


def run_experiment(
    dataset: Sequence[Board], depth: int, order: bool, prune: bool
) -> tuple[float, list[float]]:

    start = time.time()
    found_values = []
    for board in dataset:

        parent_node = Node("initial_node", board=board, last_move=None, player="white")
        suggested_node, value = minimax(
            parent_node=parent_node,
            value_function=get_node_value,
            get_children=partial(create_children_from_parent, ordered=order),
            depth=depth,
            alpha=-np.inf,
            beta=np.inf,
            maximizing_player=True,
            prune=prune,
        )
        found_values.append(value)
    return time.time() - start, found_values


if __name__ == "__main__":

    for DEPTH, NUM_BOARDS in zip((1, 2, 3, 4, 5), (100, 50, 10, 10, 10)):
        print("DEPTH:", DEPTH)
        print("NUM_BOARDS:", NUM_BOARDS)
        dataset = tuple(
            generate_dataset(
                dataset_path="analyses/alpha_beta_performance_increase/board_strings/",
                num_boards=NUM_BOARDS,
            )
        )
        print(
            f"Loaded dataset with {len(dataset)} boards. "
            f"On average these boards contain "
            f"{sum(len(tuple(board.all_pieces())) for board in dataset)/len(dataset)} "
            f"pieces. \nWith a maximum of "
            f"{max(len(tuple(board.all_pieces())) for board in dataset)} pieces "
            f"and a minimum of "
            f" {min(len(tuple(board.all_pieces())) for board in dataset)} pieces."
        )

        print("Working on ordered and pruned experiment...")
        ordered_and_pruned_time, ordered_and_pruned_values = run_experiment(
            dataset=dataset, depth=DEPTH, order=True, prune=True
        )
        print(
            "Ordered and pruned finished after",
            ordered_and_pruned_time,
            "seconds",
        )
        print("Working on just pruned experiment...")
        just_pruned_time, just_pruned_values = run_experiment(
            dataset=dataset, depth=DEPTH, order=False, prune=True
        )
        print("Just pruned finished after", just_pruned_time, "seconds")
        if DEPTH <= 4:
            print("Working on baseline experiment...")
            baseline_time, baseline_values = run_experiment(
                dataset=dataset, depth=DEPTH, order=False, prune=False
            )
            print("Baseline finished after", baseline_time, "seconds")

        print("\n")
        print("Times:")
        print(ordered_and_pruned_time)
        print(just_pruned_time)
        if DEPTH <= 4:
            print(baseline_time)

        print(ordered_and_pruned_values)
        print(just_pruned_values)
        if DEPTH <= 4:
            print(baseline_values)
        print("\n")
        print("-------------------------------------------------")
        print("-------------------------------------------------")
        print("-------------------------------------------------")
        print("\n")

        assert ordered_and_pruned_values == just_pruned_values
        if DEPTH <= 4:
            assert just_pruned_values == baseline_values
            assert baseline_values == ordered_and_pruned_values
