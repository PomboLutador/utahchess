from __future__ import annotations

import time
from functools import partial
from os import walk
from typing import Generator, Sequence

from utahchess import WHITE
from utahchess.board import Board
from utahchess.minimax import Node, create_children_from_parent, get_node_value, minimax


def generate_dataset(
    dataset_path: str, num_boards: int
) -> Generator[tuple[Board, str], None, None]:
    """Read and yield a number of board strings read from files."""
    for root, _, filenames in walk(dataset_path):
        for count, filename in enumerate(filenames):
            if count == num_boards:
                break
            with open(f"{root}/{filename}", "r") as file:
                yield Board(board_string=file.read()), filename


def run_experiment(
    dataset: Sequence[tuple[Board, str]], depth: int, order: bool, prune: bool
) -> tuple[float, list[float], list[str], list[str]]:
    """Run minimax algorithm at given depth for all boards in the dataset."""
    start = time.time()
    found_values = []
    found_nodes = []
    filenames = []
    for board, filename in dataset:

        parent_node = Node(
            name="initial_node",
            parent=None,
            board=board,
            last_move=None,
            player=WHITE,
        )
        suggested_node, value = minimax(
            parent_node=parent_node,
            value_function=get_node_value,
            get_children=partial(create_children_from_parent, ordered=order),
            depth=depth,
            alpha=-float("inf"),
            beta=float("inf"),
            maximizing_player=True,
            prune=prune,
        )
        found_values.append(value)
        found_nodes.append(suggested_node.name)
        filenames.append(filename)
    return time.time() - start, found_values, found_nodes, filenames


def report_results(time: float, type: str, num_boards: int) -> None:
    print(
        f"Experiment of type '{type}' took {time:.2f} seconds to run. "
        f"This implies each board took {time/num_boards:.2f} seconds to process."
    )


if __name__ == "__main__":

    for DEPTH, NUM_BOARDS in zip((1, 2, 3, 4, 5), (100, 50, 50, 50, 50)):
        print("=====================================================================")
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
            f"{sum(len(tuple(board.all_pieces())) for board, _ in dataset)/len(dataset)} "
            f"pieces. \nWith a maximum of "
            f"{max(len(tuple(board.all_pieces())) for board, _ in dataset)} pieces "
            f"and a minimum of "
            f"{min(len(tuple(board.all_pieces())) for board, _ in dataset)} pieces."
        )

        (
            ordered_and_pruned_time,
            ordered_and_pruned_values,
            ordered_and_pruned_node_names,
            ordered_and_pruned_node_filenames,
        ) = run_experiment(dataset=dataset, depth=DEPTH, order=True, prune=True)
        (
            just_pruned_time,
            just_pruned_values,
            just_pruned_node_names,
            just_pruned_filenames,
        ) = run_experiment(dataset=dataset, depth=DEPTH, order=False, prune=True)

        # Assert all algorithms found the same values
        assert ordered_and_pruned_values == just_pruned_values
        for experiment_time, type in zip(
            (ordered_and_pruned_time, just_pruned_time),
            ("ordered and pruned", "only pruned"),
        ):
            report_results(time=experiment_time, type=type, num_boards=NUM_BOARDS)

        if DEPTH < 4:
            (
                baseline_time,
                baseline_values,
                baseline_node_names,
                baseline_filenames,
            ) = run_experiment(dataset=dataset, depth=DEPTH, order=False, prune=False)
            assert just_pruned_values == baseline_values
            assert baseline_values == ordered_and_pruned_values
            report_results(time=baseline_time, type="baseline", num_boards=NUM_BOARDS)
