from __future__ import annotations

from typing import Optional

import pygame

from gui.constants import (
    BORDER_X_OFFSET,
    BORDER_Y_OFFSET,
    CHECKMATE_FONT_COLOR,
    HIGHLIGHT_COLOR,
    HIGHLIGHT_THICKNESS,
    MIDDLE_OF_BOARD_X,
    MIDDLE_OF_BOARD_Y,
    PIECE_ASSET_HEIGHT,
    PIECE_ASSET_WIDTH,
    TILE_HEIGHT,
    TILE_WIDTH,
)
from gui.piece_to_assetname import piece_to_assetname
from gui.pygame.click_handler import get_pixel_coordinates_from_integer_coordinates
from utahchess.board import Board
from utahchess.legal_moves import is_checkmate
from utahchess.move import Move


def draw_pieces(screen: pygame.Surface, board: Board):
    for piece in board.all_pieces():
        current_tile = piece.position
        x = current_tile[0]
        y = current_tile[1]
        (
            x_pixel,
            y_pixel,
        ) = get_pixel_coordinates_from_integer_coordinates(x=x, y=y)

        assetname = piece_to_assetname(piece)
        img = pygame.image.load(f"src\\gui\\assets\\{assetname}")
        screen.blit(
            img,
            (
                x_pixel + (TILE_WIDTH - PIECE_ASSET_WIDTH) / 2,
                y_pixel + (TILE_HEIGHT - PIECE_ASSET_HEIGHT) / 2,
            ),
        )


def highlight_legal_destinations(
    screen: pygame.Surface,
    legal_destinations: tuple[tuple[int, int], ...],
    x: int,
    y: int,
) -> None:
    """"""
    for destination_tile in legal_destinations:
        _highlight_rectangle(screen, destination_tile[0], destination_tile[1])


def notify_checkmate(
    screen: pygame.Surface,
    board: Board,
    player_in_checkmate: str,
    winning_player: str,
    font: pygame.font.Font,
    last_move: Optional[Move],
):
    if is_checkmate(
        board=board, current_player=player_in_checkmate, last_move=last_move
    ):
        text_rect = font.render(
            f"{player_in_checkmate} is in checkmate - {winning_player} wins!",
            True,
            CHECKMATE_FONT_COLOR,
        )
        screen_center = (MIDDLE_OF_BOARD_X, MIDDLE_OF_BOARD_Y)
        new_x = screen_center[0] - text_rect.get_rect().width / 2
        new_y = screen_center[1] - text_rect.get_rect().height / 2
        screen.blit(text_rect, (new_x, new_y))


def _highlight_rectangle(screen: pygame.Surface, x: int, y: int):
    """Draws a border around the rectangle indexed by x and y."""
    rect = pygame.Rect(
        x * TILE_WIDTH + BORDER_X_OFFSET,
        y * TILE_HEIGHT + BORDER_Y_OFFSET,
        TILE_WIDTH,
        TILE_HEIGHT,
    )
    pygame.draw.rect(screen, HIGHLIGHT_COLOR, rect, HIGHLIGHT_THICKNESS)
    pygame.display.flip()
