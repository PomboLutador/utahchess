from __future__ import annotations

from typing import Optional

import pygame

from gui.constants import FONT, HEIGHT, WIDTH
from gui.pygame.click_handler import (
    convert_pixel_coordinates_to_indices,
    get_tile_indices_from_user_input,
    get_user_input,
)
from gui.pygame.draw_constants import (
    draw_controls,
    draw_empty_board,
    draw_rank_and_file,
)
from gui.pygame.draw_current_game_state import (
    draw_pieces,
    highlight_legal_destinations,
    notify_checkmate,
)
from utahchess import BLACK, WHITE
from utahchess.board import Board, is_edible, is_occupied
from utahchess.chess import ChessGame
from utahchess.minimax import Node, create_children_from_parent, get_node_value, minimax
from utahchess.tile_movement_utils import is_in_bounds


class PygameGUI:
    game: ChessGame = ChessGame()

    def __init__(self):
        pygame.init()
        self.font = FONT
        self.running = True
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.last_mouse_click_indices = None
        self.game_started = False

        draw_empty_board(screen=self.screen)
        (
            self.new_game_button,
            self.undo_move_button,
            self.ai_move_button,
        ) = draw_controls(screen=self.screen, font=self.font)

        draw_rank_and_file(screen=self.screen, font=self.font)
        while self.running:
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.visualize_current_game_state()

                    x_pixel, y_pixel = get_user_input()
                    x_index, y_index = get_tile_indices_from_user_input()

                    # Handle button clicks on buttons
                    if self.new_game_button.collidepoint(x_pixel, y_pixel):
                        self.new_game()
                        continue
                    if self.undo_move_button.collidepoint(x_pixel, y_pixel):
                        self.undo_move()
                        continue
                    if self.ai_move_button.collidepoint(x_pixel, y_pixel):
                        self.make_ai_move()
                        continue

                    if self.game.get_current_player() == WHITE:
                        # No button clicked and click is outside of board bounds, skip
                        if not is_in_bounds(position=(x_index, y_index)):
                            continue

                        # Click lands on an occupied tile, highlight legal destinations
                        self._highlight_legal_destinations(x=x_index, y=y_index)

                        # Clicked tile not occupied or enemy color, try to make a move
                        self._make_move(x=x_index, y=y_index)

                elif event.type == pygame.MOUSEBUTTONUP:
                    # On release of mouse button if the click was in bounds, it is saved
                    last_mouse_click_indices = convert_pixel_coordinates_to_indices(
                        pixel_coordinates=pygame.mouse.get_pos()
                    )
                    if is_in_bounds(position=last_mouse_click_indices):
                        self.last_mouse_click_indices = last_mouse_click_indices

    def new_game(self) -> None:
        self.game.new_game()
        self.game_started = True
        self.visualize_current_game_state()

    def undo_move(self) -> None:
        self.game.undo_move()
        self.visualize_current_game_state()

    def make_ai_move(self) -> None:
        if self.game.get_current_player() == BLACK:
            parent_node = Node(
                name="initial_node",
                parent=None,
                board=self.get_current_board(),
                last_move=None,
                player=BLACK,
            )

            suggested_node, value = minimax(
                parent_node=parent_node,
                value_function=get_node_value,
                get_children=create_children_from_parent,
                depth=3,
                alpha=-float("inf"),
                beta=float("inf"),
                maximizing_player=True,
            )
            print(suggested_node, value)
            self.game.make_move(move_in_algebraic_notation=suggested_node.name)
            self.visualize_current_game_state()

    def get_current_board(self) -> Board:
        return self.game.current_game_state.board

    def get_last_move(self) -> Optional[str]:
        return self.game.current_game_state.last_move_algebraic

    def get_current_player(self) -> str:
        return self.game.get_current_player()

    def visualize_current_game_state(self) -> None:
        draw_empty_board(screen=self.screen)
        (
            self.new_game_button,
            self.undo_move_button,
            self.ai_move_button,
        ) = draw_controls(
            screen=self.screen,
            font=self.font,
            current_player=self.get_current_player() if self.game_started else None,
            last_move=self.get_last_move() if self.game_started else None,
        )
        if self.game_started:
            draw_pieces(screen=self.screen, board=self.get_current_board())
            notify_checkmate(
                screen=self.screen,
                board=self.get_current_board(),
                player_in_checkmate=self.get_current_player(),
                winning_player=self.get_opposite_player(),
                font=self.font,
                last_move=self.game.current_game_state.last_move,
            )
        draw_rank_and_file(screen=self.screen, font=self.font)

    def get_opposite_player(self) -> str:
        return BLACK if self.get_current_player() == WHITE else WHITE

    def _highlight_legal_destinations(self, x, y) -> None:
        if is_occupied(self.get_current_board(), position=(x, y)):
            legal_destinations = self.game.get_legal_destinations_for_piece(
                position=(x, y)
            )
            highlight_legal_destinations(
                screen=self.screen,
                legal_destinations=legal_destinations,
                x=x,
                y=y,
            )

    def _make_move(self, x, y) -> None:
        if not is_occupied(self.get_current_board(), (x, y)) or is_edible(
            board=self.get_current_board(),
            position=(x, y),
            friendly_color=self.get_current_player(),
        ):
            if self.last_mouse_click_indices:
                potential_algebraic_move, _ = None, None
                for (
                    algebraic_move,
                    move,
                ) in self.game.current_game_state.legal_moves.items():
                    if (
                        move.piece_moves[0][1] == (x, y)
                        and move.piece_moves[0][0] == self.last_mouse_click_indices
                    ):
                        potential_algebraic_move, _ = algebraic_move, move
                if potential_algebraic_move:
                    self.game.make_move(
                        move_in_algebraic_notation=potential_algebraic_move
                    )

                self.visualize_current_game_state()


if __name__ == "__main__":
    gui = PygameGUI()
