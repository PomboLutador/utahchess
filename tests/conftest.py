import pytest

from utahchess.board import Board
from utahchess.piece import (
    INITIAL_BISHOPS,
    INITIAL_KINGS,
    INITIAL_QUEENS,
    INITIAL_ROOKS,
)


@pytest.fixture
def initial_board_with_only_rooks():
    return Board(pieces=INITIAL_ROOKS)


@pytest.fixture
def initial_board_with_only_bishops():
    return Board(pieces=INITIAL_BISHOPS)


@pytest.fixture
def initial_board_with_only_queens():
    return Board(pieces=INITIAL_QUEENS)


@pytest.fixture
def initial_board_with_only_kings():
    return Board(pieces=INITIAL_KINGS)
