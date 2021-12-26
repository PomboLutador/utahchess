from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence

from utahchess.board import Board
from utahchess.legal_moves import get_move_per_algebraic_identifier
from utahchess.move import Move, make_move
from utahchess.move_validation import is_check, is_checkmate


class ChessGame:
    current_game_state: GameState
    previous_game_states: list[GameState] = []

    def new_game(self) -> None:
        """Initialize a new game of chess."""
        board = Board()
        current_player = "white"
        turn = 1
        legal_moves = get_move_per_algebraic_identifier(
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
        """Try out move in algebraic notation on the current board.

        Current game state is replaced with the game state after the move, if it was
        successful. The game state prior to the move is appended to the previous game
        states. Legal moves on the board after the successful move are computed.

        Args:
            move_in_algebraic_notation: Move which will be tried out.

        Returns: True if the move was allowed, otherwise False.
        """
        board_after_move, successful_move, last_move = _try_move(
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
                turn=self._increment_turn(
                    turn=self.current_game_state.turn,
                    current_player=self.current_game_state.current_player,
                ),
                legal_moves=get_move_per_algebraic_identifier(
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
        """Get whether game is either in checkmate or stalemate."""
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

    def undo_move(self) -> None:
        """Revert game state back to previous game state."""
        self.current_game_state = self.previous_game_states.pop()

    def get_current_player(self) -> str:
        return self.current_game_state.current_player

    def get_legal_moves(self) -> tuple[str, ...]:
        """Get all legal moves in the current game state in algebraic notation."""
        return tuple(self.current_game_state.legal_moves.keys())

    def get_legal_destinations_for_piece(
        self, position: tuple[int, int]
    ) -> tuple[tuple[int, int], ...]:
        """Get all possible destinations for a piece.
        
        Castling moves are considered king moves and so the legal destination of a
        castling move will show up as a legal destination of the king, never the rook.
        """
        return tuple(
            legal_move.piece_moves[0][1]
            for legal_move in self.current_game_state.legal_moves.values()
            if legal_move.piece_moves[0][0] == position
        )

    def __repr__(self) -> str:
        return self.current_game_state.__repr__()

    def _increment_turn(self, turn: int, current_player: str) -> int:
        if current_player == "black":
            return turn + 1
        else:
            return turn


@dataclass(frozen=True)
class GameState:
    """Game state within the context of a chess game."""

    board: Board
    current_player: str
    turn: int
    legal_moves: dict[str, Move]
    last_move: Optional[Move] = None

    def __repr__(self) -> str:
        return (
            self.board.__repr__()
            + f"\n Current player: {self.current_player}."
            + f"\n It's turn {self.turn}."
        )


def _try_move(
    board: Board,
    legal_moves: dict[str, Move],
    move_in_algebraic_notation: str,
) -> tuple[Board, bool, Optional[Move]]:
    """Try to make a move on a given board.

    Args:
        board: Board on which move is tried on.
        legal_moves: A mapping of legal moves in algebraic notation to moves.
        move_in_algebraic_notation: Move in algebraic notation which will be tried.

    Returns:
            If the given move was legal this returns the board after the move, a
            boolean indicating success and the last move that was just executed.
            In case the move was not legal initial board, a boolean indicating
            failure and None are returned.
    """
    try:
        return (
            make_move(board=board, move=legal_moves[move_in_algebraic_notation]),
            True,
            legal_moves[move_in_algebraic_notation],
        )
    except KeyError:
        return board, False, None


def is_stalemate(
    board: Board,
    current_player: str,
    legal_moves_for_current_player: Sequence[str],
) -> bool:
    """Get whether a board is in stalemate or not.

    Stalemate is defined as a player not being in check but also having no moves
    available.
    """
    return (
        not is_check(board=board, current_player=current_player)
        and len(legal_moves_for_current_player) == 0
    )


if __name__ == "__main__":
    game = ChessGame()
    game.new_game()

    while not game.is_game_over():
        print(game)
        game.make_move(move_in_algebraic_notation=input("Please enter a move: \n"))
    else:
        print(f"Game over! The winner is {game.get_next_player()}!")
