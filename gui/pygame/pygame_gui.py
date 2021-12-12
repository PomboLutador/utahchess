from __future__ import annotations

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
from utahchess.board import Board, is_edible, is_occupied
from utahchess.chess import ChessGame
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
        self.new_game_button, self.undo_move_button = draw_controls(
            screen=self.screen, font=self.font
        )

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
                    if self.undo_move_button.collidepoint(x_pixel, y_pixel):
                        self.undo_move()

                    # If no button is clicked and click is outside of board bounds, skip
                    if not is_in_bounds(position=(x_index, y_index)):
                        continue

                    # If click lands on an occupied tile, highlight legal destinations
                    self._highlight_legal_destinations(x=x_index, y=y_index)

                    # If clicked tile not occupied or enemy color, try to make a move
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

    def get_current_board(self) -> Board:
        return self.game.current_game_state.board

    def get_current_player(self) -> str:
        return self.game.get_current_player()

    def visualize_current_game_state(self) -> None:
        draw_empty_board(screen=self.screen)
        self.new_game_button, self.undo_move_button = draw_controls(
            screen=self.screen, font=self.font
        )
        if self.game_started:
            draw_pieces(screen=self.screen, board=self.get_current_board())
            notify_checkmate(
                screen=self.screen,
                board=self.get_current_board(),
                player_in_checkmate=self.get_current_player(),
                winning_player=self.get_opposite_player(),
                font=self.font,
            )
        draw_rank_and_file(screen=self.screen, font=self.font)

    def get_opposite_player(self) -> str:
        return "black" if self.get_current_player() == "white" else "white"

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
                # Make Move here
                potential_move = self.game.get_move_from_positions(
                    from_position=self.last_mouse_click_indices,
                    to_position=(x, y),
                )
                if potential_move:
                    algebraic_move, _ = potential_move
                _ = self.game.make_move(move_in_algebraic_notation=algebraic_move)

                self.visualize_current_game_state()


if __name__ == "__main__":
    gui = PygameGUI()
