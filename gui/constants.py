import pygame

from utahchess import BLACK, WHITE

pygame.init()

FONT = pygame.font.SysFont("Arial", 15)
BUTTON_FONT_COLOR = "#000000"
RANK_FONT_COLOR = "#FFFFFF"
FILE_FONT_COLOR = "#FFFFFF"
LAST_MOVE_FONT_COLOR = "#FFFFFF"
CHECKMATE_FONT_COLOR = "#000000"
NEW_GAME_BUTTON_COLOR = "#BBBBBB"
UNDO_MOVE_BUTTON_COLOR = "#999999"
AI_MOVE_BUTTON_COLOR = "#777777"
BORDER_X_OFFSET = 20
BORDER_Y_OFFSET = 20
TILE_WIDTH = 80
TILE_HEIGHT = 80
ROWS = 8
COLUMNS = 8
ASSET_SIZE = 60
WHITE_TILE_COLOR = "#FFFFFF"
BLACK_TILE_COLOR = "#AACCCC"
HIGHLIGHT_THICKNESS = 5
HIGHLIGHT_COLOR = "#cca9cc"
PIECE_ASSET_HEIGHT = 60
PIECE_ASSET_WIDTH = 60
BACKGROUND_COLOR = "#000000"
PLAYERS = [WHITE, BLACK]

CONTROLS_BOX_COLOR = "#DDFFFF"
CONTROLS_BOX_OFFSET = 5
OFFSET_FOR_BUTTONS = 80
HALF_SPACE_BETWEEN_BUTTONS = 1

WIDTH = BORDER_X_OFFSET * 2 + 8 * TILE_WIDTH
HEIGHT = BORDER_Y_OFFSET * 3 + 8 * TILE_HEIGHT + OFFSET_FOR_BUTTONS

MIDDLE_OF_BOARD_X = BORDER_X_OFFSET + (COLUMNS / 2) * TILE_WIDTH
MIDDLE_OF_BOARD_Y = BORDER_Y_OFFSET + (ROWS / 2) * TILE_HEIGHT
