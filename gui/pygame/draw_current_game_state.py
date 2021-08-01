from __future__ import annotations

import pygame

from gui.constants import (
    BORDER_X_OFFSET,
    BORDER_Y_OFFSET,
    HIGHLIGHT_COLOR,
    HIGHLIGHT_THICKNESS,
    PIECE_ASSET_HEIGHT,
    PIECE_ASSET_WIDTH,
    TILE_HEIGHT,
    TILE_WIDTH,
)
from gui.piece_to_assetname import piece_to_assetname
from gui.pygame.click_handler import get_pixel_coordinates_from_integer_coordinates
from utahchess.board import Board


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
        img = pygame.image.load(f"GUI\\assets\\{assetname}")
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
