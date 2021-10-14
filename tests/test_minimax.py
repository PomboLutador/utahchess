from functools import partial

import numpy as np
import pytest
from anytree import Node

from utahchess.board import Board
from utahchess.legal_moves import get_algebraic_notation_mapping, make_move
from utahchess.minimax import (
    create_children_from_parent,
    get_board_value,
    get_node_value,
    minimax,
)
from utahchess.move_validation import is_checkmate


def test_get_board_value_on_symmetric_board():
    # given
    board = Board()

    # when
    result1 = get_board_value(board=board, player_that_just_made_the_move="white")
    result2 = get_board_value(board=board, player_that_just_made_the_move="black")

    # then
    assert result1 == result2


def test_get_board_value_better_if_middle_is_occupied():
    # given
    board_string = f"""br-bn-bb-bq-bk-bb-bn-br
            bp-bp-bp-bp-oo-bp-bp-bp
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-oo-oo-oo-oo
            wp-wp-wp-wp-wp-wp-wp-wp
            wr-wn-wb-wq-wk-wb-wn-wr"""
    board1 = Board(board_string=board_string)
    board2 = Board()

    # when
    result1 = get_board_value(board=board1, player_that_just_made_the_move="black")
    result2 = get_board_value(board=board2, player_that_just_made_the_move="black")

    # then
    assert result1 >= result2


def test_get_board_value_is_infinite_when_in_checkmate():
    # given
    board_string = f"""br-bn-bb-oo-bk-bb-bn-br
            bp-bp-bp-bp-oo-bp-bp-bp
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-oo-oo-oo-wp-bq
            oo-oo-oo-oo-oo-wp-oo-oo
            wp-wp-wp-wp-wp-oo-oo-wp
            wr-wn-wb-wq-wk-wb-wn-wr"""
    board = Board(board_string=board_string)

    # when
    result_black = get_board_value(board=board, player_that_just_made_the_move="black")
    result_white = get_board_value(board=board, player_that_just_made_the_move="white")

    # then
    assert is_checkmate(board=board, current_player="white")
    assert result_black == np.inf
    assert result_black == -result_white


@pytest.mark.parametrize(
    ("current_player", "opposite_player"), [("white", "black"), ("black", "white")]
)
def test_get_board_value_is_symmetric(current_player, opposite_player):
    # given
    board = Board()
    for move in list(
        get_algebraic_notation_mapping(
            board=board, current_player=current_player, last_move=None
        ).values()
    ):
        board_after_move = make_move(board=board, move=move)

        # when
        result1 = get_board_value(
            board=board_after_move, player_that_just_made_the_move=current_player
        )
        result2 = get_board_value(
            board=board_after_move, player_that_just_made_the_move=opposite_player
        )

        # then
        assert result1 == -result2


@pytest.mark.parametrize(("ordered"), [True, False])
@pytest.mark.parametrize(("depth"), [1, 2, 3])
def test_minimax_finds_checkmate_in_fools_mate(depth, ordered):
    # given
    children_function = partial(create_children_from_parent, ordered=ordered)
    board = Board(
        board_string=f"""br-bn-bb-bq-bk-bb-bn-br
            bp-bp-bp-bp-oo-bp-bp-bp
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-oo-oo-oo-wp-oo
            oo-oo-oo-oo-oo-wp-oo-oo
            wp-wp-wp-wp-wp-oo-oo-wp
            wr-wn-wb-wq-wk-wb-wn-wr"""
    )
    parent_node = Node(name="parent", board=board, last_move=None, player="black")

    # when
    resulting_node, resulting_value = minimax(
        parent_node=parent_node,
        value_function=get_node_value,
        get_children=children_function,
        depth=depth,
        alpha=-np.inf,
        beta=np.inf,
        maximizing_player=True,
    )

    # then
    assert resulting_node.name == "Qh4#"
    assert resulting_value == np.inf


def test_minimax_with_dummy_game():
    # given

    parent_node = Node(name="parent", value=3, depth=0)
    children_nodes_function = lambda parent_node: [
        Node(
            name=f"child_with_value_{i+1}_depth_{parent_node.depth+1}",
            parent=parent_node,
            value=(i + 1),
            depth=parent_node.depth + 1,
        )
        for i in range(4)
    ]
    node_value_function = lambda node: node.value

    # when
    result_node, result_value = minimax(
        parent_node=parent_node,
        value_function=node_value_function,
        get_children=children_nodes_function,
        depth=3,
        maximizing_player=True,
        alpha=-np.inf,
        beta=np.inf,
    )

    # then
    assert result_value == 4
    assert result_node.name == "child_with_value_1_depth_1"
