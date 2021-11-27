from __future__ import annotations

from collections import OrderedDict
from itertools import product
from typing import Callable, Generator

import numpy as np
from anytree import Node  # type: ignore

from utahchess.board import Board
from utahchess.legal_moves import get_algebraic_notation_mapping, make_move
from utahchess.move import Move
from utahchess.move_validation import is_checkmate

# TODO: We can just replace Node with a little dict containing the necessary
# TODO: fields. We are not actually making use of any Node properties.


PAWN_VALUE = 1
BISHOP_VALUE = 3
KNIGHT_VALUE = 3
ROOK_VALUE = 5
QUEEN_VALUE = 9
CHECKMATE_VALUE = np.inf

CENTER_OF_BOARD_POSITIONS = tuple(product((2, 3, 4, 5), (2, 3, 4, 5)))
CENTER_OF_BOARD_VALUE = 0.25

EDGE_POSITIONS = tuple(product((0, 1, 6, 7), (0, 1, 6, 7))) + tuple(
    product((0, 1, 2, 3, 4, 5, 6, 7), (0, 1, 6, 7))
)
EDGE_VALUE = -0.25


def minimax(
    parent_node: Node,
    value_function: Callable,
    get_children: Callable,
    depth: int,
    maximizing_player: bool,
    alpha: float,
    beta: float,
    prune: bool = True,
) -> tuple[Node, float]:
    if (
        depth == 0
    ):  # Do we need to also add a condition when node is terminal (i.e. checkmate)?
        # Or is this handled by the fact that get_children won't produce any new nodes?
        return parent_node, value_function(node=parent_node)

    best_move = None
    if maximizing_player:
        best_value = -np.inf
        for child_node in get_children(parent_node=parent_node):
            _, eval = minimax(
                parent_node=child_node,
                value_function=value_function,
                get_children=get_children,
                depth=depth - 1,
                maximizing_player=False,
                alpha=alpha,
                beta=beta,
                prune=prune,
            )
            if eval > best_value:
                best_value = eval
                best_move = child_node
            alpha = max(alpha, best_value)
            if alpha >= beta:
                if prune:
                    break

    else:
        best_value = +np.inf
        for child_node in get_children(parent_node=parent_node):
            _, eval = minimax(
                parent_node=child_node,
                value_function=value_function,
                get_children=get_children,
                depth=depth - 1,
                maximizing_player=True,
                alpha=alpha,
                beta=beta,
                prune=prune,
            )
            if eval < best_value:
                best_value = eval
                best_move = child_node
            beta = min(beta, best_value)
            if alpha >= beta:
                if prune:
                    break
    return best_move, best_value


def _order_moves_by_potential(moves_mapping: dict[str, Move]) -> OrderedDict[str, Move]:
    checkmate_moves = []
    pawn_captures = []
    other_captures = []
    rest = []

    for algebraic_identifier, move in moves_mapping.items():
        # Checkmate moves
        if algebraic_identifier[-1] == "#":
            checkmate_moves.append((algebraic_identifier, move))

        # Pawn captures
        elif algebraic_identifier[0] == "x":
            pawn_captures.append((algebraic_identifier, move))

        # Other captures
        elif algebraic_identifier[0] != "x" and "x" in algebraic_identifier:
            other_captures.append((algebraic_identifier, move))

        # Leftovers
        else:
            rest.append((algebraic_identifier, move))

    ordered_moves = checkmate_moves + pawn_captures + other_captures + rest
    return OrderedDict(ordered_moves)


def create_children_from_parent(
    parent_node: Node, ordered: bool
) -> Generator[Node, None, None]:
    parent_board = parent_node.board
    parent_last_move = parent_node.last_move
    parent_player = parent_node.player
    if ordered:
        return (
            Node(
                algebraic_identifier,
                parent=parent_node,
                board=make_move(board=parent_board, move=legal_move),
                last_move=legal_move,
                player=_get_enemy_color(friendly_color=parent_player),
            )
            for algebraic_identifier, legal_move in _order_moves_by_potential(
                get_algebraic_notation_mapping(
                    board=parent_board,
                    current_player=parent_player,
                    last_move=parent_last_move,
                )
            ).items()
        )
    else:
        return (
            Node(
                algebraic_identifier,
                parent=parent_node,
                board=make_move(board=parent_board, move=legal_move),
                last_move=legal_move,
                player=_get_enemy_color(friendly_color=parent_player),
            )
            for algebraic_identifier, legal_move in get_algebraic_notation_mapping(
                board=parent_board,
                current_player=parent_player,
                last_move=parent_last_move,
            ).items()
        )


def get_board_value(board: Board, player_that_just_made_the_move: str) -> float:
    if is_checkmate(
        board=board,
        current_player=_get_enemy_color(friendly_color=player_that_just_made_the_move),
    ):
        return +CHECKMATE_VALUE
    elif is_checkmate(board=board, current_player=player_that_just_made_the_move):
        return -CHECKMATE_VALUE

    value: float = 0
    for piece in board.all_pieces():
        add_or_subtract = 1 if piece.color == player_that_just_made_the_move else -1
        if piece.piece_type == "Pawn":
            value += add_or_subtract * PAWN_VALUE
        if piece.piece_type == "Bishop":
            value += add_or_subtract * BISHOP_VALUE
        if piece.piece_type == "Knight":
            value += add_or_subtract * KNIGHT_VALUE
        if piece.piece_type == "Rook":
            value += add_or_subtract * ROOK_VALUE
        if piece.piece_type == "Queen":
            value += add_or_subtract * QUEEN_VALUE
        if piece.position in CENTER_OF_BOARD_POSITIONS:
            value += add_or_subtract * CENTER_OF_BOARD_VALUE
        if piece.position in EDGE_POSITIONS:
            value += add_or_subtract * EDGE_VALUE

    return value


def _get_enemy_color(friendly_color: str) -> str:
    return "white" if friendly_color == "black" else "black"


get_node_value = lambda node: get_board_value(
    board=node.board,
    player_that_just_made_the_move=_get_enemy_color(friendly_color=node.player),
)


if __name__ == "__main__":

    fools_mate = Board(
        board_string=f"""br-bn-bb-bq-bk-bb-bn-br
            bp-bp-bp-bp-oo-bp-bp-bp
            oo-oo-oo-oo-oo-oo-oo-oo
            oo-oo-oo-oo-bp-oo-oo-oo
            oo-oo-oo-oo-oo-oo-wp-oo
            oo-oo-oo-oo-oo-wp-oo-oo
            wp-wp-wp-wp-wp-oo-oo-wp
            wr-wn-wb-wq-wk-wb-wn-wr"""
    )
    parent_node = Node("initial_node", board=fools_mate, last_move=None, player="black")

    suggested_node, value = minimax(
        parent_node=parent_node,
        value_function=get_node_value,
        get_children=create_children_from_parent,
        depth=5,
        alpha=-np.inf,
        beta=np.inf,
        maximizing_player=True,
    )
    print(suggested_node, value)
