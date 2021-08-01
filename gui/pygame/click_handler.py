from __future__ import annotations

from math import floor

import pygame

from gui.constants import BORDER_X_OFFSET, BORDER_Y_OFFSET, TILE_HEIGHT, TILE_WIDTH


def get_user_input() -> tuple[int, int]:
    """Get click position in pixels relative to top-left corner."""
    return pygame.mouse.get_pos()


def get_tile_indices_from_user_input() -> tuple[int, int]:
    """Get click position in board indices."""
    return convert_pixel_coordinates_to_indices(pixel_coordinates=get_user_input())


def get_pixel_coordinates_from_integer_coordinates(x: int, y: int) -> tuple[int, int]:
    x_pixel = (x * TILE_WIDTH) + BORDER_X_OFFSET
    y_pixel = (y * TILE_HEIGHT) + BORDER_Y_OFFSET
    return (x_pixel, y_pixel)


def convert_pixel_coordinates_to_indices(
    pixel_coordinates: tuple[int, int]
) -> tuple[int, int]:
    x_pixel, y_pixel = pixel_coordinates
    x_integer = (x_pixel - BORDER_X_OFFSET) / TILE_WIDTH
    y_integer = (y_pixel - BORDER_Y_OFFSET) / TILE_HEIGHT
    return (floor(x_integer), floor(y_integer))
