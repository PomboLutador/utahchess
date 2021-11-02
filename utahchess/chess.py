from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from utahchess.board import Board
from utahchess.legal_moves import (
    get_algebraic_notation_mapping,
    is_stalemate,
    make_move,
)
from utahchess.move import Move
from utahchess.move_validation import is_checkmate


@dataclass(frozen=True)
class GameState:
    board: Board
    current_player: str
    turn: int
    legal_moves: dict[str, Move]
    last_move: Optional[Move] = None

    def __repr__(self) -> str:
        representation = self.board.__repr__()
        representation += f"\n Current player: {self.current_player}."
        representation += f"\n It's turn {self.turn}."
        return representation


class ChessGame:
    current_game_state: GameState
    previous_game_states: list[GameState] = []

    def new_game(self) -> None:
        board = Board()
        current_player = "white"
        turn = 1
        legal_moves = get_algebraic_notation_mapping(
            board=board, current_player=current_player
        )
        self.current_game_state = GameState(
            board=board,
            current_player=current_player,
            turn=turn,
            legal_moves=legal_moves,
        )
        return

    def make_move(self, move_in_algebraic_notation: str) -> bool:
        board_after_move, successful_move, last_move = try_move(
            board=self.current_game_state.board,
            legal_moves=self.current_game_state.legal_moves,
            move_in_algebraic_notation=move_in_algebraic_notation,
        )
        if successful_move:
            next_player = self.get_next_player()
            self.previous_game_states.append(self.current_game_state)
            self.current_game_state = GameState(
                board=board_after_move,
                last_move=last_move,
                current_player=next_player,
                turn=self.increment_turn(
                    turn=self.current_game_state.turn,
                    current_player=self.current_game_state.current_player,
                ),
                legal_moves=get_algebraic_notation_mapping(
                    board=board_after_move,
                    current_player=next_player,
                    last_move=last_move,
                ),
            )
            return successful_move
        return False

    def get_next_player(self) -> str:
        return "white" if self.get_current_player() == "black" else "black"

    def is_game_over(self) -> bool:
        return is_checkmate(
            board=self.current_game_state.board,
            current_player=self.get_current_player(),
        ) or is_stalemate(
            board=self.current_game_state.board,
            current_player=self.get_current_player(),
            legal_moves_for_current_player=tuple(
                self.current_game_state.legal_moves.keys()
            ),
        )

    def __repr__(self) -> str:
        return self.current_game_state.__repr__()

    def increment_turn(self, turn: int, current_player: str) -> int:
        if current_player == "black":
            return turn + 1
        else:
            return turn

    def undo_move(self) -> None:
        self.current_game_state = self.previous_game_states.pop()

    def get_current_player(self) -> str:
        return self.current_game_state.current_player

    def get_legal_moves(self) -> tuple[str, ...]:
        return tuple(self.current_game_state.legal_moves.keys())

    def get_legal_destinations_for_piece(
        self, position: tuple[int, int]
    ) -> tuple[tuple[int, int], ...]:
        return tuple(
            legal_move.piece_moves[0][1]
            for legal_move in self.current_game_state.legal_moves.values()
            if legal_move.piece_moves[0][0] == position
        )

    def get_move_from_positions(
        self, from_position: tuple[int, int], to_position: tuple[int, int]
    ) -> Optional[tuple[str, Move]]:
        for (
            algebraic_move,
            move,
        ) in self.current_game_state.legal_moves.items():
            if (
                move.piece_moves[0][1] == to_position
                and move.piece_moves[0][0] == from_position
            ):
                return algebraic_move, move
        return None


def try_move(
    board: Board,
    legal_moves: dict[str, Move],
    move_in_algebraic_notation: str,
) -> tuple[Board, bool, Optional[Move]]:
    """Try to make a move on a given board.

    Args:
        board: Board on which move is tried on.
        legal_moves: A mapping of legal moves in algebraic notation to instances of the
            Move class and its inherited classes.
        move_in_algebraic_notation: Description of the move that should be tried in
            algebraic notation.

    Returns:
        tuple[Board, bool, Move]: If the given move was legal this returns a tuple
            containing the board after the move, a boolean indicating success and
            the last move that was just executed. In case the move was not legal the
            tuple will contain the initial board, a boolean indicating failure and None
            for the last move.
    """
    try:
        return (
            make_move(board=board, move=legal_moves[move_in_algebraic_notation]),
            True,
            legal_moves[move_in_algebraic_notation],
        )
    except KeyError:
        return board, False, None


if __name__ == "__main__":
    game = ChessGame()
    game.new_game()

    while not game.is_game_over():
        print(game)
        game.make_move(move_in_algebraic_notation=input("Please enter a move: \n"))
    else:
        print(f"Game over! The winner is {game.get_next_player()}!")
