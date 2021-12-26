from __future__ import annotations

from collections import OrderedDict
from itertools import product
from typing import Any, Callable, Generator, Iterable, Optional

from utahchess.board import Board
from utahchess.legal_moves import get_move_per_algebraic_identifier, is_checkmate
from utahchess.move import Move, make_move

PAWN_VALUE = 1
BISHOP_VALUE = 3
KNIGHT_VALUE = 3
ROOK_VALUE = 5
QUEEN_VALUE = 9
CHECKMATE_VALUE = float("inf")

CENTER_OF_BOARD_POSITIONS = tuple(product((2, 3, 4, 5), (2, 3, 4, 5)))
CENTER_OF_BOARD_VALUE = 0.25

EDGE_POSITIONS = tuple(product((0, 1, 6, 7), (0, 1, 6, 7))) + tuple(
    product((0, 1, 2, 3, 4, 5, 6, 7), (0, 1, 6, 7))
)
EDGE_VALUE = -0.25


class Node:
    def __init__(self, parent: Optional[Node], name: str, **kwargs):
        self.parent = parent
        self.name = name
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return self.name

    def __getattr__(self, attribute_name: str) -> Any:
        return getattr(self, attribute_name)


def minimax(
    parent_node: Node,
    value_function: Callable[..., float],
    get_children: Callable[..., Iterable[Node]],
    depth: int,
    maximizing_player: bool,
    alpha: float,
    beta: float,
    prune: bool = True,
) -> tuple[Node, float]:
    """Get the optimal course of action for a given parent and value function.

    General purpose implementation of the minimax algorithm with alpha-beta pruning.
    For more information see here:
        https://en.wikipedia.org/wiki/Minimax
        https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning

    Args:
        parent_node: Initial node.
        value_function: Function to evaluate the value of a node.
        get_children: Function which creates all children for a node.
        depth: How deep to look for optimal course of action for.
        maximizing_player: If the algorithm is trying to maximize or minimize the
            value function for the current player.
        alpha: Alpha parameter for alpha-beta pruning.
        beta: Beta parameter for alpha-beta pruning.
        prune: Whether to use alpha-beta pruning or not.

    Returns: The optimal course of action, i.e. the child which should be considered
        and the associated optimal node value.
    """
    if depth == 0:
        return parent_node, value_function(node=parent_node)

    best_move: Any = None
    if maximizing_player:
        best_value = -float("inf")
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
        best_value = +float("inf")
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


def create_children_from_parent(
    parent_node: Node, ordered: bool = True
) -> Generator[Node, None, None]:
    """Create all possible child boards for a given parent board.

    Args:
        parent_node: Parent node containing its board, the last move that was executed
            on that board and the current player.
        ordered: Whether or not to order the children by their potential. Generally
            when alpha-beta pruning it is better to look at nodes that are potentially
            high value first to decrease computation time.

    Returns: All possible boards for the given parent board, potentially ordered by
        their individual potential.
    """
    parent_board = parent_node.board
    parent_last_move = parent_node.last_move
    parent_player = parent_node.player
    if ordered:
        return (
            Node(
                parent=parent_node,
                name=algebraic_identifier,
                board=make_move(board=parent_board, move=legal_move),
                last_move=legal_move,
                player=_get_enemy_color(friendly_color=parent_player),
            )
            for algebraic_identifier, legal_move in _order_moves_by_potential(
                get_move_per_algebraic_identifier(
                    board=parent_board,
                    current_player=parent_player,
                    last_move=parent_last_move,
                )
            ).items()
        )
    else:
        return (
            Node(
                parent=parent_node,
                name=algebraic_identifier,
                board=make_move(board=parent_board, move=legal_move),
                last_move=legal_move,
                player=_get_enemy_color(friendly_color=parent_player),
            )
            for algebraic_identifier, legal_move in get_move_per_algebraic_identifier(
                board=parent_board,
                current_player=parent_player,
                last_move=parent_last_move,
            ).items()
        )


def get_board_value(board: Board, player_that_just_made_the_move: str) -> float:
    """Get ad-hoc evaluation of a board.

    This function gets the value of the board to the player that just made the move.
    That means if 'player_that_just_made_the_move' is "black" and "white" is in
    checkmate on the board, then the value will be infinite, for example.

    Args:
        board: Board to evaluate.
        player_that_just_made_the_move: Player that made the move to arrive at the
            current board configuration.

    Returns: The value of the board to the player that just made the move.
    """
    if is_checkmate(
        board=board,
        current_player=_get_enemy_color(friendly_color=player_that_just_made_the_move),
    ):
        return +CHECKMATE_VALUE
    elif is_checkmate(board=board, current_player=player_that_just_made_the_move):
        return -CHECKMATE_VALUE

    value: float = 0.0
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


def get_node_value(node: Node):
    """Get ad-hoc evaluation of a given node containing a chess board."""
    return get_board_value(
        board=node.board,
        player_that_just_made_the_move=_get_enemy_color(friendly_color=node.player),
    )


def _order_moves_by_potential(moves_mapping: dict[str, Move]) -> OrderedDict[str, Move]:
    """Get ad-hoc ordering of moves mapping to process high-potential moves first."""
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


def _get_enemy_color(friendly_color: str) -> str:
    return "white" if friendly_color == "black" else "black"


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
    parent_node = Node(
        name="initial_node",
        parent=None,
        board=fools_mate,
        last_move=None,
        player="black",
    )

    suggested_node, value = minimax(
        parent_node=parent_node,
        value_function=get_node_value,
        get_children=create_children_from_parent,
        depth=4,
        alpha=-float("inf"),
        beta=float("inf"),
        maximizing_player=True,
    )
    print(suggested_node, value)
