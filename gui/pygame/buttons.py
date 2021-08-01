import pygame

from gui.constants import (
    BORDER_X_OFFSET,
    BORDER_Y_OFFSET,
    COLUMNS,
    CONTROLS_BOX_OFFSET,
    HALF_SPACE_BETWEEN_BUTTONS,
    OFFSET_FOR_BUTTONS,
    TILE_HEIGHT,
    TILE_WIDTH,
)

NEW_GAME_BUTTON = pygame.Rect(
    BORDER_X_OFFSET + CONTROLS_BOX_OFFSET,
    BORDER_Y_OFFSET * 2 + (COLUMNS * TILE_HEIGHT) + CONTROLS_BOX_OFFSET,
    (TILE_WIDTH * 8 - 2 * CONTROLS_BOX_OFFSET) / 2 - 2 * HALF_SPACE_BETWEEN_BUTTONS,
    (OFFSET_FOR_BUTTONS - 2 * CONTROLS_BOX_OFFSET - 2 * HALF_SPACE_BETWEEN_BUTTONS) / 2,
)

UNDO_MOVE_BUTTON = pygame.Rect(
    BORDER_X_OFFSET
    + CONTROLS_BOX_OFFSET
    + (TILE_WIDTH * 8 - 2 * CONTROLS_BOX_OFFSET) / 2
    + 2 * HALF_SPACE_BETWEEN_BUTTONS,
    BORDER_Y_OFFSET * 2 + (COLUMNS * TILE_HEIGHT) + CONTROLS_BOX_OFFSET,
    (TILE_WIDTH * 8 - 2 * CONTROLS_BOX_OFFSET) / 2 - 2 * HALF_SPACE_BETWEEN_BUTTONS,
    (OFFSET_FOR_BUTTONS - 2 * CONTROLS_BOX_OFFSET - 2 * HALF_SPACE_BETWEEN_BUTTONS) / 2,
)
