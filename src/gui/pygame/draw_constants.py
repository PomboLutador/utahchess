from __future__ import annotations

import pygame

from gui.constants import (
    AI_MOVE_BUTTON_COLOR,
    BACKGROUND_COLOR,
    BLACK_TILE_COLOR,
    BORDER_X_OFFSET,
    BORDER_Y_OFFSET,
    BUTTON_FONT_COLOR,
    COLUMNS,
    CONTROLS_BOX_COLOR,
    FILE_FONT_COLOR,
    LAST_MOVE_FONT_COLOR,
    NEW_GAME_BUTTON_COLOR,
    OFFSET_FOR_BUTTONS,
    RANK_FONT_COLOR,
    ROWS,
    TILE_HEIGHT,
    TILE_WIDTH,
    UNDO_MOVE_BUTTON_COLOR,
    WHITE_TILE_COLOR,
)
from gui.pygame.buttons import (
    AI_MOVE_BUTTON,
    CURRENT_PLAYER_FAKE_BUTTON,
    LAST_MOVE_FAKE_BUTTON,
    NEW_GAME_BUTTON,
    UNDO_MOVE_BUTTON,
)
from utahchess import BLACK, WHITE


def draw_empty_board(screen: pygame.Surface) -> None:
    screen.fill(BACKGROUND_COLOR)
    _draw_squares(screen=screen)


def draw_rank_and_file(screen: pygame.Surface, font: pygame.font.Font) -> None:

    # Above board
    for idx, rank in enumerate("abcdefgh"):
        x, y = (BORDER_X_OFFSET + (idx + 0.5) * TILE_WIDTH, 0)
        text_rect = font.render(rank, True, RANK_FONT_COLOR)
        screen.blit(text_rect, (x, y))

    # Below board
    for idx, rank in enumerate("abcdefgh"):
        x, y = (
            BORDER_X_OFFSET + (idx + 0.5) * TILE_WIDTH,
            TILE_HEIGHT * 8 + BORDER_Y_OFFSET,
        )
        text_rect = font.render(rank, True, RANK_FONT_COLOR)
        screen.blit(text_rect, (x, y))

    # Left of board
    for idx, file in enumerate(reversed(range(1, 9))):
        x, y = (
            BORDER_X_OFFSET / 4,
            BORDER_Y_OFFSET + (idx + 0.5) * TILE_HEIGHT,  # type: ignore
        )
        text_rect = font.render(str(file), True, FILE_FONT_COLOR)
        screen.blit(text_rect, (x, y))

    # Right of board
    for idx, file in enumerate(reversed(range(1, 9))):
        x, y = (
            BORDER_X_OFFSET * 1.25 + TILE_WIDTH * 8,
            BORDER_Y_OFFSET + (idx + 0.5) * TILE_HEIGHT,  # type: ignore
        )
        text_rect = font.render(str(file), True, FILE_FONT_COLOR)
        screen.blit(text_rect, (x, y))


def draw_controls(
    screen: pygame.Surface,
    font: pygame.font.Font,
    current_player: str = None,
    last_move: str = None,
) -> tuple[pygame.Rect, ...]:

    # Draw background for controls
    _draw_controls_background(screen=screen)
    new_game_button = _draw_new_game_button(screen=screen, font=font)
    undo_move_button = _draw_undo_move_button(screen=screen, font=font)
    ai_move_button = _draw_ai_move_button(screen=screen, font=font)
    _draw_current_player(screen=screen, font=font, current_player=current_player)
    _draw_last_move(screen=screen, font=font, last_move=last_move)

    return (new_game_button, undo_move_button, ai_move_button)


def _draw_squares(screen: pygame.Surface) -> None:
    for x in range(1, COLUMNS + 1):
        for y in range(1, ROWS + 1):
            rect = (
                BORDER_X_OFFSET + ((x - 1) * TILE_WIDTH),
                BORDER_Y_OFFSET + ((y - 1) * TILE_HEIGHT),
                TILE_WIDTH,
                TILE_HEIGHT,
            )
            pygame.draw.rect(
                screen,
                WHITE_TILE_COLOR if (x + y) % 2 == 0 else BLACK_TILE_COLOR,
                rect,
            )


def _draw_controls_background(screen: pygame.Surface) -> None:
    rect = (
        BORDER_X_OFFSET,
        BORDER_Y_OFFSET * 2 + (COLUMNS * TILE_HEIGHT),
        TILE_WIDTH * 8,
        OFFSET_FOR_BUTTONS,
    )
    pygame.draw.rect(
        screen,
        CONTROLS_BOX_COLOR,
        rect,
    )


def _draw_new_game_button(
    screen: pygame.Surface, font: pygame.font.Font
) -> pygame.Rect:
    pygame.draw.rect(
        screen,
        NEW_GAME_BUTTON_COLOR,
        NEW_GAME_BUTTON,
    )

    text_rect = font.render("New Game", True, BUTTON_FONT_COLOR)
    button_center = NEW_GAME_BUTTON.center
    new_x = button_center[0] - text_rect.get_rect().width / 2
    new_y = button_center[1] - text_rect.get_rect().height / 2
    screen.blit(text_rect, (new_x, new_y))
    return NEW_GAME_BUTTON


def _draw_undo_move_button(
    screen: pygame.Surface, font: pygame.font.Font
) -> pygame.Rect:
    pygame.draw.rect(
        screen,
        UNDO_MOVE_BUTTON_COLOR,
        UNDO_MOVE_BUTTON,
    )

    text_rect = font.render("Undo Move", True, BUTTON_FONT_COLOR)
    button_center = UNDO_MOVE_BUTTON.center
    new_x = button_center[0] - text_rect.get_rect().width / 2
    new_y = button_center[1] - text_rect.get_rect().height / 2
    screen.blit(text_rect, (new_x, new_y))
    return UNDO_MOVE_BUTTON


def _draw_ai_move_button(screen: pygame.Surface, font: pygame.font.Font) -> pygame.Rect:
    pygame.draw.rect(
        screen,
        AI_MOVE_BUTTON_COLOR,
        AI_MOVE_BUTTON,
    )
    text_rect = font.render("AI Move", True, BUTTON_FONT_COLOR)
    button_center = AI_MOVE_BUTTON.center
    new_x = button_center[0] - text_rect.get_rect().width / 2
    new_y = button_center[1] - text_rect.get_rect().height / 2
    screen.blit(text_rect, (new_x, new_y))
    return AI_MOVE_BUTTON


def _draw_current_player(
    screen: pygame.Surface, font: pygame.font.Font, current_player: str = None
) -> pygame.Rect:
    pygame.draw.rect(
        screen,
        CONTROLS_BOX_COLOR,
        CURRENT_PLAYER_FAKE_BUTTON,
    )
    if not current_player:
        text_to_display = ""
    elif current_player == WHITE:
        text_to_display = f"It's your turn!"
    elif current_player == BLACK:
        text_to_display = f"It's the AI's turn! Press the button to the left!"

    text_rect = font.render(text_to_display, True, BUTTON_FONT_COLOR)
    button_center = CURRENT_PLAYER_FAKE_BUTTON.center
    new_x = button_center[0] - text_rect.get_rect().width / 2
    new_y = button_center[1] - text_rect.get_rect().height / 2
    screen.blit(text_rect, (new_x, new_y))
    return CURRENT_PLAYER_FAKE_BUTTON


def _draw_last_move(
    screen: pygame.Surface, font: pygame.font.Font, last_move: str = None
) -> pygame.Rect:
    pygame.draw.rect(
        screen,
        BACKGROUND_COLOR,
        LAST_MOVE_FAKE_BUTTON,
    )
    if not last_move:
        text_to_display = ""
    else:
        text_to_display = "Last move:  " + last_move

    text_rect = font.render(text_to_display, True, LAST_MOVE_FONT_COLOR)
    button_center = LAST_MOVE_FAKE_BUTTON.center
    new_x = button_center[0] - text_rect.get_rect().width / 2
    new_y = button_center[1] - text_rect.get_rect().height / 2
    screen.blit(text_rect, (new_x, new_y))
    return LAST_MOVE_FAKE_BUTTON
